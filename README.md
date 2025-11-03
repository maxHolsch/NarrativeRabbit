# Narrative Knowledge Graph

An advanced system for capturing, analyzing, and querying organizational stories with their multi-perspective tellings and contextual relationships.

## 🎯 Overview

The Narrative Knowledge Graph transforms organizational stories from scattered anecdotes into queryable knowledge. It captures:

- **Stories** with multi-layered structure (content, actors, themes, context)
- **Multiple Perspectives** showing how different groups tell the same story
- **Causal Relationships** linking events and outcomes
- **Cultural Patterns** revealing group values and narrative tendencies
- **Historical Precedents** for informed decision-making

## 🏗️ Architecture

### Backend (Python + FastAPI)
- **FastAPI REST API** for data access
- **Neo4j Graph Database** for relationship modeling
- **Claude API Integration** for LLM-powered narrative extraction
- **Pydantic Models** for data validation
- **Synthetic Data Generator** for demonstration

### Frontend (React + TypeScript + D3.js)
- **React 18** with TypeScript
- **D3.js Force-Directed Graph** for network visualization
- **Tanstack Query** for state management
- **Vite** for fast development and building

### Database (Neo4j)
- **Graph Schema** with 8+ node types and 10+ relationship types
- **Cypher Queries** for pattern matching and analysis
- **Indexes** for performance optimization

## 🚀 Quick Start

### Prerequisites

- **Docker & Docker Compose** (for Neo4j)
- **Python 3.10+**
- **Node.js 18+**
- **Anthropic API Key** (for LLM extraction)

### 1. Clone and Setup

```bash
cd NarrativeAnalysisTool

# Copy environment file
cp .env.example .env

# Edit .env and add your Anthropic API key
# ANTHROPIC_API_KEY=your_key_here
```

### 2. Start Neo4j Database

```bash
cd docker
docker-compose up -d

# Wait ~30 seconds for Neo4j to fully start
# Verify at http://localhost:7474 (neo4j/narrativegraph123)
```

### 3. Set Up Python Backend

```bash
cd ../backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database with sample data
python scripts/init_database.py

# Start API server
python main.py
```

API will be available at http://localhost:8000
API docs at http://localhost:8000/docs

### 4. Set Up Frontend

```bash
cd ../frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Dashboard will be available at http://localhost:5173

## 📊 Features

### 1. Interactive Graph Visualization

Explore the narrative network with D3.js force-directed graph:
- **Color-coded nodes**: Stories (blue), People (green), Groups (orange), Themes (purple), Events (red)
- **Interactive**: Zoom, pan, drag nodes
- **Click nodes** for detailed information

### 2. Story Browser

Browse organizational narratives with:
- **Type filtering**: Success, failure, learning, decision, crisis
- **Theme tags** for categorization
- **Lessons learned** from each story
- **Temporal context**

### 3. Perspective Analysis

Compare how different groups tell stories:
- **Group-specific framing** of events
- **Value emphasis** patterns
- **Narrative frequency** by department

### 4. Cultural Insights

Understand organizational culture through:
- **Theme distribution** across stories
- **Story type patterns** (success vs. failure narratives)
- **Group narrative activity**
- **Value alignment** across departments

### 5. Advanced Queries

Powered by sophisticated Cypher queries:
- Find stories by group and topic
- Compare event narratives across perspectives
- Identify similar patterns and precedents
- Trace causal chains
- Get cautionary tales by theme

## 🔍 Example Use Cases

### Use Case 1: New PM Making a Decision

**Query**: Find precedents for product prioritization decisions

```bash
curl "http://localhost:8000/api/patterns/precedents?themes=prioritization&themes=technical-debt&limit=5"
```

**Insight**: See how similar decisions played out, learn from multiple perspectives

### Use Case 2: Post-Incident Review

**Query**: How have similar incidents been handled?

```bash
curl "http://localhost:8000/api/patterns/cautionary?themes=reliability&themes=incident%20response"
```

**Insight**: Identify successful response patterns and common pitfalls

### Use Case 3: Cultural Assessment

**Query**: What values does each group emphasize?

```bash
curl "http://localhost:8000/api/analysis/values/Engineering%20Team"
```

**Insight**: Understand cultural alignment and gaps across organization

### Use Case 4: Onboarding

**Query**: What are the foundational stories?

```bash
curl "http://localhost:8000/api/index/theme"
```

**Insight**: New hires understand culture through actual narratives

## 📡 API Endpoints

### Stories
- `GET /api/stories/search` - Search stories by criteria
- `GET /api/stories/{id}` - Get specific story

### Perspectives
- `GET /api/perspectives/group/{name}` - Get group perspective
- `GET /api/perspectives/compare/{event}` - Compare perspectives

### Patterns
- `GET /api/patterns/precedents` - Find similar situations
- `GET /api/patterns/similar/{id}` - Find similar stories
- `GET /api/patterns/cautionary` - Get cautionary tales

### Analysis
- `GET /api/analysis/causality/{id}` - Trace causal chain
- `GET /api/analysis/values/{group}` - Group value emphasis

### Graph
- `GET /api/graph/data` - Get visualization data

### Extraction
- `POST /api/extract/narrative` - Extract narrative from text

### Index
- `GET /api/index/{dimension}` - Browse by theme/group/type/value

## 🎨 Data Model

### Core Entities (Nodes)

- **Story**: Multi-layered narrative with content, structure, actors, themes, context
- **Person**: Individual actors and storytellers
- **Group**: Teams, departments, organizational units
- **Event**: Specific occurrences referenced in stories
- **Theme**: Recurring concepts (innovation, reliability, etc.)
- **Decision**: Key choice points
- **Value**: Organizational values expressed
- **Outcome**: Results and consequences

### Relationships (Edges)

- **TELLS**: Person → Story (with framing, context)
- **ABOUT**: Story → Event
- **INVOLVES**: Story → Person (with role)
- **BELONGS_TO**: Person → Group
- **EXEMPLIFIES**: Story → Theme/Value
- **LED_TO**: Event → Event (causal)
- **ECHOES**: Story → Story (similar patterns)
- **CONTRADICTS**: Story → Story (different versions)

## 🛠️ Development

### Adding Real Data Sources

Replace the synthetic data generator with actual integrations:

1. **Slack**: Use Slack API to pull channel messages
2. **Email**: Parse email threads for narratives
3. **Wiki**: Extract project histories and case studies
4. **Interviews**: Transcribe and process interview recordings

Example integration:

```python
# backend/src/services/integrations/slack_connector.py
from slack_sdk import WebClient

class SlackNarrativeCollector:
    def __init__(self, token):
        self.client = WebClient(token=token)

    def collect_channel_stories(self, channel_id):
        # Fetch messages, identify narrative segments
        # Extract using Claude API
        # Return Story objects
        pass
```

### Extending the Graph Schema

Add new node types or relationships:

```python
# backend/src/models/entities.py
class Project(BaseNode):
    name: str
    description: str
    # ... additional fields
```

```cypher
// Create new relationship type
MATCH (s:Story), (p:Project)
WHERE s.project = p.name
CREATE (s)-[:PART_OF]->(p)
```

### Custom Visualizations

Add new D3.js visualizations:

```typescript
// frontend/src/visualizations/TimelineView.tsx
export const TimelineView = ({ stories }: Props) => {
  // D3 timeline implementation
};
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest tests/
```

### Frontend Tests

```bash
cd frontend
npm test
```

## 📈 Performance

- **Graph Database**: Indexed queries with O(log n) lookups
- **API**: FastAPI async for concurrent requests
- **Frontend**: React Query caching, lazy loading
- **Visualization**: D3 canvas fallback for >1000 nodes

## 🔐 Security

- **API Key Management**: Environment variables only
- **CORS**: Configured origins
- **Input Validation**: Pydantic models
- **Query Limits**: Prevent resource exhaustion

## 📝 License

MIT License - feel free to use and modify

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📚 Further Reading

- [Neo4j Graph Database](https://neo4j.com/docs/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [D3.js Force Simulation](https://d3js.org/d3-force)
- [Claude API](https://docs.anthropic.com/)

## 🐛 Troubleshooting

### Neo4j Connection Failed

```bash
# Check if Neo4j is running
docker ps

# View logs
docker logs narrative-neo4j

# Restart
docker-compose restart
```

### Frontend Can't Connect to API

```bash
# Verify API is running
curl http://localhost:8000/health

# Check CORS settings in .env
```

### Out of Memory

```bash
# Increase Neo4j heap size in docker-compose.yml
NEO4J_dbms_memory_heap_max__size=4G
```

## 🎯 Next Steps

1. **Integrate Real Data**: Connect to Slack, email, wiki
2. **Advanced Analytics**: ML for narrative clustering
3. **Sentiment Analysis**: Track emotional tone across stories
4. **Temporal Analysis**: Show narrative evolution over time
5. **Export Features**: Generate reports and presentations
6. **Mobile App**: iOS/Android for narrative capture

---

Built with ❤️ for better organizational storytelling
