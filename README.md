# Drug Protocol Analytics Dashboard

Academic data engineering project — PostgreSQL + FastAPI + GitHub Pages.

## Live Demo
Frontend: `https://your-username.github.io/drug-analytics`
Backend API: `https://your-app-name.onrender.com`

## Project Structure
```
drug-analytics/
├── frontend/
│   └── index.html        ← GitHub Pages (the dashboard)
├── backend/
│   ├── main.py           ← FastAPI backend
│   ├── requirements.txt
│   └── render.yaml       ← Render deploy config
└── README.md
```

## Deploy Steps

### Step 1 — Push to GitHub
```bash
git init
git add .
git commit -m "initial commit"
git remote add origin https://github.com/your-username/drug-analytics.git
git push -u origin main
```

### Step 2 — Enable GitHub Pages (frontend)
1. Go to your repo on GitHub
2. Settings → Pages
3. Source: Deploy from branch → main → /frontend
4. Save — your URL will be: https://your-username.github.io/drug-analytics

### Step 3 — Deploy Backend on Render (free)
1. Go to https://render.com and sign up free
2. New → Web Service → connect your GitHub repo
3. Root directory: backend
4. Build command: pip install -r requirements.txt
5. Start command: uvicorn main:app --host 0.0.0.0 --port $PORT
6. Add environment variables for DB connection
7. Deploy — get your URL e.g. https://drug-protocol-api.onrender.com

### Step 4 — Update API URL in frontend
In frontend/index.html, find this line:
```js
const API_BASE = 'https://your-app-name.onrender.com';
```
Replace with your actual Render URL, commit and push.
