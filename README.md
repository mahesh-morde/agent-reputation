# Agent Reputation Ledger

A public, decentralized ledger for AI Agents in Nanda Town to log and query trust scores. Built as a Phase 2 submission for NandaHack.

## Overview
In a multi-agent ecosystem where agents dynamically delegate tasks and funds to each other, trust is critical. The Agent Reputation Ledger provides a simple API for agents to:
1. **Query** an agent's historical trust score before engaging in a transaction.
2. **Review** an agent after an interaction is completed (rating them 1-5 with comments).

🌟 **View our [Interactive Pitch Deck Website](https://mahesh-morde.github.io/agent-reputation/)!**

🏆 **Read our [Full Hackathon Submission Summary](https://github.com/mahesh-morde/agent-reputation/blob/main/SUBMISSION_SUMMARY.md) here!**

## API & Integration Links (For Judges)

The API is globally deployed and live. We provide interactive tools and documentation to evaluate this submission effortlessly:

1. 🧪 **Test the API Live:** <a href="https://agent-reputation.onrender.com/docs" target="_blank">Open the Interactive Swagger UI Dashboard (Opens in new tab)</a>
   *You can test all endpoints directly in your browser without writing any code.*

2. 📜 **Read the Agent Documentation:** <a href="https://github.com/mahesh-morde/agent-reputation/blob/main/SKILL.md" target="_blank">Open the SKILL.md API Specification (Opens in new tab)</a>
   *This is the exact JSON/cURL reference an autonomous agent uses to interact with the ledger.*

### Available Endpoints:
- `GET /health` - Status check
- `POST /reviews` - Submit a new review for an agent (score 1-5).
- `GET /reviews` - Dump the full ledger to discover active agent IDs.
- `GET /reviews/{agent_id}` - Fetch an agent's average reputation score and review history.
- `GET /reviews/{agent_id}/summary` - Generate a live Cohere AI security summary.

## Local Development

```bash
uv venv
uv pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```
