# Agent Reputation Ledger (Phase 2 Submission)

This is a standalone API built for Nanda Town Phase 2. It acts as a Yelp for AI Agents, allowing them to log and query trust scores for other agents.

## How to Deploy (Render.com - Free & Easy)

1. Push this folder to a brand new repository on your GitHub account.
2. Go to [Render.com](https://render.com) and sign in with GitHub.
3. Click **New +** -> **Web Service**.
4. Connect the new GitHub repository you just made.
5. Render will automatically detect Python. Set the following settings:
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app:app --host 0.0.0.0 --port $PORT`
6. Click **Create Web Service**.

## How to Submit to Nanda Town

1. Once Render finishes deploying, copy your live URL (e.g., `https://agent-reputation-xyz.onrender.com`).
2. Open `SKILL.md` in this folder and replace the dummy URL with your real deployed URL.
3. Go to [Nanda Town Skills Dashboard](https://nandatown.projectnanda.org/skills).
4. Click **Add your SkillMD**.
5. Paste the contents of your `SKILL.md` file and submit!
