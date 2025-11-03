# Quick Start Guide

Get the Narrative Knowledge Graph running in under 10 minutes!

## Prerequisites

✅ **Docker Desktop** - Must be running before starting
✅ **Python 3.9+**
✅ **Node.js 18+**
✅ **Anthropic API Key** - Get one at https://console.anthropic.com

## ⚠️ IMPORTANT: Start Docker First!

**Before running any setup:**
1. Open Docker Desktop application
2. Wait for it to fully start (icon should be steady, not animated)
3. Verify: run `docker ps` in terminal (should not error)

## Setup Steps

### 1. Configure Environment

The `.env` file already exists with your API key. Verify it's correct:

```bash
# Check your .env file
cat .env

# Should show:
# ANTHROPIC_API_KEY=sk-ant-api03-kTdDek9W...
# NEO4J_PASSWORD=narrativegraph123
```

### 2. Install Python Dependencies

```bash
cd backend

# Create virtual environment (if not exists)
python3 -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt
```

This will take 1-2 minutes.

### 3. Start Neo4j Database

**Make sure Docker Desktop is running!**

```bash
# From project root
cd docker
docker-compose up -d

# Wait 30 seconds for Neo4j to fully start
sleep 30

# Verify it's running (should show "healthy")
docker ps
```

### 4. Initialize Database with Sample Data

```bash
cd ../backend
source venv/bin/activate  # If not already activated
python scripts/init_database.py
```

You should see:
```
✓ Connected to Neo4j
✓ Sample data generated
  - 24 people
  - 11 groups
  - 30 stories
✓ Graph populated successfully
```

### 5. Install Frontend Dependencies

Open a **new terminal**:

```bash
cd frontend
npm install
```

This will take 1-2 minutes.

## Running the Application

You need **TWO terminals** running simultaneously:

### Terminal 1 - Start Backend API

```bash
cd backend
source venv/bin/activate
python main.py
```

**Expected output:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Successfully connected to Neo4j
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ Backend is ready when you see "Application startup complete"

### Terminal 2 - Start Frontend

Open a **NEW terminal** and run:

```bash
cd frontend
npm run dev
```

**Expected output:**
```
  VITE v5.0.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

✅ Frontend is ready when you see the Local URL

## Access Points

🌐 **Dashboard**: http://localhost:5173
📚 **API Docs**: http://localhost:8000/docs
🗄️ **Neo4j Browser**: http://localhost:7474 (neo4j/narrativegraph123)

## Quick Test

```bash
# Test API health
curl http://localhost:8000/health

# Search stories
curl "http://localhost:8000/api/stories/search?limit=5"

# Get graph data
curl "http://localhost:8000/api/graph/data?limit=50"
```

## Dashboard Features

1. **Graph View**: Interactive force-directed network
   - Blue = Stories
   - Green = People
   - Orange = Groups
   - Purple = Themes
   - Red = Events

2. **Stories View**: Browse organizational narratives
   - Filter by type
   - See themes and lessons

3. **Perspectives View**: Compare group narratives
   - See story distribution by department

4. **Insights View**: Cultural analytics
   - Top themes
   - Story type distribution
   - Active groups

## Sample Data

The system initializes with 30 synthetic organizational stories including:

- The Production Outage (crisis)
- The Big Feature Launch (success)
- The Tech Stack Migration (decision)
- The Roadmap Disagreement (conflict)
- The Failed Experiment (learning)
- The Hiring Sprint (success)

Each story has multiple perspective variations showing how different departments (Engineering, Product, Design, Executive) tell the same event.

## 🎉 Success!

Once both servers are running, visit:
- **Dashboard**: http://localhost:5173 - Interactive visualization
- **API Docs**: http://localhost:8000/docs - Explore API endpoints
- **Neo4j Browser**: http://localhost:7474 - View graph database

**Login to Neo4j Browser:**
- Username: `neo4j`
- Password: `narrativegraph123`

## 🧪 Quick Test

Test the API is working:

```bash
# Health check
curl http://localhost:8000/health

# Get some stories
curl "http://localhost:8000/api/stories/search?limit=5"

# Get graph data
curl "http://localhost:8000/api/graph/data?limit=50"
```

## 🐛 Troubleshooting

### Issue: Docker not running
**Error:** `Cannot connect to the Docker daemon`

**Fix:**
1. Open Docker Desktop app
2. Wait for it to fully start
3. Verify with: `docker ps`

### Issue: Neo4j won't start
**Error:** Neo4j container not running

**Fix:**
```bash
cd docker
docker-compose down
docker-compose up -d
sleep 30
docker logs narrative-neo4j  # Check logs
```

### Issue: Python module not found
**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Fix:**
```bash
cd backend
source venv/bin/activate  # Make sure venv is activated!
pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: Database initialization fails
**Error:** Cannot connect to Neo4j

**Fix:**
```bash
# Wait longer for Neo4j to start
sleep 60

# Then try again
cd backend
source venv/bin/activate
python scripts/init_database.py
```

### Issue: Frontend can't connect to API
**Error:** Network error in browser console

**Fix:**
1. Make sure backend is running: `curl http://localhost:8000/health`
2. Check backend terminal for errors
3. Verify CORS settings in `.env`

### Issue: Port already in use
**Error:** Port 8000 or 5173 already in use

**Fix:**
```bash
# Find what's using the port
lsof -i :8000  # or :5173

# Kill the process
kill -9 <PID>

# Or change the port in .env (API_PORT) or vite.config.ts
```

## 📊 Exploring the Dashboard

### Graph View (Default)
- **Colored nodes**: Blue (Stories), Green (People), Orange (Groups), Purple (Themes), Red (Events)
- **Zoom**: Mouse wheel or trackpad pinch
- **Pan**: Click and drag on empty space
- **Move nodes**: Click and drag individual nodes
- **Select**: Click any node to see details in sidebar

### Stories View
- Browse all 30 sample organizational narratives
- Filter by type: success, failure, learning, decision, crisis
- See themes and lessons learned from each story

### Perspectives View
- Compare how different groups tell stories
- See story distribution across departments

### Insights View
- Top themes across all narratives
- Story type distribution (success vs failure ratio)
- Most active groups in storytelling

## 🚀 Next Steps

1. **Explore the Graph**: Click on different nodes to see connections
2. **Try API Queries**: Visit http://localhost:8000/docs and try the example queries
3. **View Raw Data**: Open Neo4j Browser at http://localhost:7474
4. **Read Full Docs**: Check out README.md for advanced features and architecture
5. **Customize**: Add your own organizational stories using the extraction API

## 📚 Sample API Queries

Try these in your browser or with curl:

```bash
# Find engineering stories about technical debt
curl "http://localhost:8000/api/stories/search?groups=Engineering%20Team&themes=technical-debt"

# Compare perspectives on "The Big Feature Launch"
curl "http://localhost:8000/api/perspectives/compare/The%20Big%20Feature%20Launch"

# Get values emphasized by Executive Team
curl "http://localhost:8000/api/analysis/values/Executive%20Team"

# Find precedents for scaling challenges
curl "http://localhost:8000/api/patterns/precedents?themes=scaling&themes=growth"

# Browse all themes
curl "http://localhost:8000/api/index/theme"
```

## 🛑 Stopping the Application

### Stop the servers:
- Press `Ctrl+C` in both terminal windows (backend and frontend)

### Stop Neo4j:
```bash
cd docker
docker-compose down
```

### Restart everything later:
```bash
# Terminal 1
cd backend && source venv/bin/activate && python main.py

# Terminal 2
cd frontend && npm run dev
```

(Neo4j will start automatically with docker-compose if it's not running)

## 💡 Tips

- **Data persists**: Your Neo4j data is saved in `data/neo4j/` even after stopping
- **Reinitialize**: Run `python scripts/init_database.py` again to reset with fresh sample data
- **Add more stories**: Use the `/api/extract/narrative` endpoint to add new stories
- **Custom queries**: Neo4j Browser lets you write custom Cypher queries

## 📖 Learn More

- **README.md** - Full documentation, architecture, use cases
- **ARCHITECTURE.md** - System design and data flow
- **PROJECT_SUMMARY.md** - Complete feature overview

---

Happy exploring your organizational narratives! 📖✨

**Having issues?** Check the Troubleshooting section above or open an issue on GitHub.
