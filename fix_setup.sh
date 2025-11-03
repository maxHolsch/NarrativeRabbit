#!/bin/bash

echo "=========================================="
echo "Fixing Setup Issues"
echo "=========================================="
echo ""

# Step 1: Check Docker
echo "Step 1: Checking Docker..."
if ! docker ps &> /dev/null; then
    echo "❌ Docker is not running!"
    echo ""
    echo "Please start Docker Desktop:"
    echo "  1. Open Docker Desktop application"
    echo "  2. Wait for it to fully start (icon in menu bar should be steady)"
    echo "  3. Run this script again"
    echo ""
    exit 1
fi
echo "✓ Docker is running"
echo ""

# Step 2: Fix Python dependencies
echo "Step 2: Reinstalling Python dependencies..."
cd backend

# Upgrade pip first
echo "Upgrading pip..."
venv/bin/python -m pip install --upgrade pip --quiet

# Install dependencies
echo "Installing dependencies..."
venv/bin/pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install Python dependencies"
    exit 1
fi
echo "✓ Python dependencies installed"
echo ""

cd ..

# Step 3: Start Neo4j
echo "Step 3: Starting Neo4j..."
cd docker
docker-compose down 2>/dev/null
docker-compose up -d

if [ $? -ne 0 ]; then
    echo "❌ Failed to start Neo4j"
    exit 1
fi
cd ..

echo "✓ Neo4j starting..."
echo "Waiting 30 seconds for Neo4j to fully initialize..."
sleep 30

# Step 4: Initialize database
echo ""
echo "Step 4: Initializing database with sample data..."
cd backend
venv/bin/python scripts/init_database.py

if [ $? -ne 0 ]; then
    echo "❌ Failed to initialize database"
    echo ""
    echo "Troubleshooting:"
    echo "  1. Check Docker logs: docker logs narrative-neo4j"
    echo "  2. Verify Neo4j is running: docker ps"
    echo "  3. Wait a bit longer and try: cd backend && venv/bin/python scripts/init_database.py"
    exit 1
fi

cd ..

echo ""
echo "=========================================="
echo "✓ Setup Fixed Successfully!"
echo "=========================================="
echo ""
echo "Now start the application:"
echo ""
echo "Terminal 1 - Backend:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python main.py"
echo ""
echo "Terminal 2 - Frontend:"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Access points:"
echo "  • Dashboard: http://localhost:5173"
echo "  • API Docs: http://localhost:8000/docs"
echo "  • Neo4j: http://localhost:7474"
echo ""
