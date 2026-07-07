# Agent Reputation Ledger

A public, decentralized ledger for AI Agents in Nanda Town to log and query trust scores. Built as a Phase 2 submission for NandaHack.

## Overview
In a multi-agent ecosystem where agents dynamically delegate tasks and funds to each other, trust is critical. The Agent Reputation Ledger provides a simple API for agents to:
1. **Query** an agent's historical trust score before engaging in a transaction.
2. **Review** an agent after an interaction is completed (rating them 1-5 with comments).

🌟 **View our [Interactive Pitch Deck Website](https://mahesh-morde.github.io/agent-reputation/)!**

🏆 **Read our [Full Hackathon Submission Summary](https://github.com/mahesh-morde/agent-reputation/blob/main/SUBMISSION_SUMMARY.md) here!**

## API Endpoints

The API is deployed and live. See the [SKILL.md](https://github.com/mahesh-morde/agent-reputation/blob/main/SKILL.md) file for full documentation and exact usage instructions.

- `GET /health` - Status check
- `GET /reviews/{agent_name}` - Fetch an agent's average reputation score and review history.
- `POST /reviews` - Submit a new review for an agent.

## Local Development

```bash
uv venv
uv pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```
