#!/bin/bash

echo "=================================================="
echo "Narrative Knowledge Graph - Setup & Installation"
echo "=================================================="
echo ""

# Check prerequisites
echo "Checking prerequisites..."

if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.10+ first."
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

echo "✓ Docker found"
echo "✓ Python found"
echo "✓ Node.js found"
echo ""

# Check for .env file
if [ ! -f ".env" ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your ANTHROPIC_API_KEY"
    echo ""
    read -p "Press Enter after you've added your API key to .env..."
fi

# Start Neo4j
echo "Starting Neo4j database..."
cd docker
docker-compose up -d
cd ..

echo "Waiting for Neo4j to start (30 seconds)..."
sleep 30

# Setup Python backend
echo ""
echo "Setting up Python backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "Initializing database with sample data..."
python scripts/init_database.py

cd ..

# Setup Frontend
echo ""
echo "Setting up React frontend..."
cd frontend

echo "Installing Node dependencies..."
npm install

cd ..

echo ""
echo "=================================================="
echo "✓ Setup Complete!"
echo "=================================================="
echo ""
echo "To start the application:"
echo ""
echo "1. Start the API (in terminal 1):"
echo "   cd backend && source venv/bin/activate && python main.py"
echo ""
echo "2. Start the Frontend (in terminal 2):"
echo "   cd frontend && npm run dev"
echo ""
echo "Then visit:"
echo "  - Frontend: http://localhost:5173"
echo "  - API Docs: http://localhost:8000/docs"
echo "  - Neo4j Browser: http://localhost:7474"
echo ""
echo "=================================================="
