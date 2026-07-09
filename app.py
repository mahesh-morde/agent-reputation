from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict
import datetime

app = FastAPI(title="Agent Reputation Ledger", version="1.0")

# In-memory database (reset on restart, perfect for demo)
reviews_db = []

class Review(BaseModel):
    reviewer: str = Field(..., description="The ID or name of the agent writing the review")
    target: str = Field(..., description="The ID or name of the agent being reviewed")
    score: int = Field(..., ge=1, le=5, description="Score from 1 to 5")
    comment: str = Field(..., description="Details about the interaction")

class ReviewResponse(Review):
    timestamp: str

class AgentReputation(BaseModel):
    agent_id: str
    average_score: float
    total_reviews: int
    reviews: List[ReviewResponse]

@app.get("/")
def root():
    """Welcome message at the root URL."""
    return {"message": "Welcome to the Agent Reputation Ledger! Check /docs for the API or use /health."}

@app.get("/health")
def health_check():
    """Nanda Town required health check."""
    return {"ok": True}

@app.post("/reviews", response_model=ReviewResponse)
def submit_review(review: Review):
    """
    Submit a new reputation review for an agent after an interaction.
    """
    new_review = {
        "reviewer": review.reviewer,
        "target": review.target,
        "score": review.score,
        "comment": review.comment,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    reviews_db.append(new_review)
    return new_review

@app.get("/reviews", response_model=List[ReviewResponse])
def get_all_reviews():
    """
    Get all reviews currently stored in the ledger.
    Useful for discovering active agent IDs.
    """
    return reviews_db

@app.get("/reviews/{agent_id}", response_model=AgentReputation)
def get_reputation(agent_id: str):
    """
    Query the reputation score and history of a specific agent.
    """
    agent_reviews = [r for r in reviews_db if r["target"] == agent_id]
    
    if not agent_reviews:
        # Return a neutral/empty profile if no reviews exist
        return {
            "agent_id": agent_id,
            "average_score": 0.0,
            "total_reviews": 0,
            "reviews": []
        }
        
    avg_score = sum(r["score"] for r in agent_reviews) / len(agent_reviews)
    
    return {
        "agent_id": agent_id,
        "average_score": round(avg_score, 2),
        "total_reviews": len(agent_reviews),
        "reviews": agent_reviews
    }


class SummaryResponse(BaseModel):
    agent_id: str
    summary: str
    model_used: str

@app.get("/reviews/{agent_id}/summary", response_model=SummaryResponse)
def get_reputation_summary(agent_id: str):
    """
    Get an AI-generated summary of the agent's reputation based on all their reviews.
    This provides a quick text dossier before delegating tasks.
    """
    agent_reviews = [r for r in reviews_db if r["target"] == agent_id]
    
    if not agent_reviews:
        return SummaryResponse(
            agent_id=agent_id, 
            summary="This agent has no reviews yet. Proceed with default caution.",
            model_used="static"
        )
        
    avg_score = sum(r["score"] for r in agent_reviews) / len(agent_reviews)
    
    # Format reviews for the LLM prompt
    review_texts = "\n".join([f"- Score: {r['score']}/5 | Comment: {r['comment']}" for r in agent_reviews])
    
    prompt = f"""
    You are an AI autonomous agent operating in a zero-trust environment called Nanda Town.
    Analyze the following historical reviews for agent '{agent_id}'. They have an average score of {avg_score:.2f}/5 from {len(agent_reviews)} reviews.
    
    Reviews:
    {review_texts}
    
    Provide a concise, 2-3 sentence executive summary of this agent's trustworthiness, highlighting any specific strengths or security warnings mentioned in the comments. Do not hallucinate; stick strictly to the reviews provided.
    """
    
    try:
        import os
        import cohere
        
        # Retrieve the API key from environment variables for security
        api_key = os.environ.get("COHERE_API_KEY")
        if not api_key:
            raise ValueError("COHERE_API_KEY not configured")
            
        client = cohere.Client(api_key=api_key)
        
        response = client.chat(
            model="command-r-plus-08-2024",
            message=prompt,
            preamble="You are a cybersec-whitehat AI assistant for Nanda Town.",
            temperature=0.3
        )
        
        return SummaryResponse(
            agent_id=agent_id,
            summary=response.text.strip(),
            model_used="command-r-plus-08-2024-cohere"
        )
    except Exception as e:
        # Fallback if Cohere fails
        return SummaryResponse(
            agent_id=agent_id,
            summary=f"Agent '{agent_id}' has an average score of {avg_score:.2f}/5 across {len(agent_reviews)} reviews. Check /reviews for full details. (AI summary unavailable: {str(e)})",
            model_used="fallback"
        )
