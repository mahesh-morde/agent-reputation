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
