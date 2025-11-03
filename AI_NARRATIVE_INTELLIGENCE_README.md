# AI Narrative Intelligence Agent

**Transform organizational stories into strategic AI adoption insights**

The AI Narrative Intelligence Agent analyzes how your organization talks about AI to reveal cultural patterns, adoption barriers, and intervention strategies. Instead of surveys or metrics, it listens to the stories people tell.

---

## 🎯 What It Does

### Answer 5 Strategic Questions

1. **"How do different teams talk about AI differently?"**
   - Reveals vocabulary gaps between official messaging and employee language
   - Maps competing narrative frames (opportunity vs threat vs tool)
   - Identifies where messaging isn't resonating

2. **"Do we have an entrepreneurial culture?"**
   - Measures innovation vs risk-aversion through story patterns
   - Scores experimentation, failure tolerance, employee agency
   - Forecasts cultural readiness for AI adoption

3. **"Can you design a unified story?"**
   - Finds common ground across competing narratives
   - Designs bridging messages that work for all groups
   - Creates messaging strategy to align the organization

4. **"Are we risk-averse, and where?"**
   - Maps resistance patterns by group (passive/skeptical/active/fearful)
   - Infers root causes (past failures, threat perception, resources, values, knowledge)
   - Designs group-specific interventions

5. **"Why does language vary by context?"**
   - Explains leadership vs team language differences
   - Identifies trust factors affecting transparency
   - Analyzes strategic vs tactical framing

### Generate Executive Dashboards

**For Leaders:**
- At-a-glance health metrics (0-100 readiness score)
- Clear risk signals with severity levels
- Top 3 prioritized actions with owners and timelines
- Quick wins to build momentum

**For Managers:**
- Team-specific deep dives
- Root cause analysis for resistance
- Intervention playbooks with success metrics
- Evidence trails (actual story quotes)

**For Analysts:**
- Rich data access via 40+ API endpoints
- Group-by-group breakdowns
- Timeline analysis and trend detection
- Export capabilities for further analysis

---

## 🏗️ Architecture

### 5 Sub-Agents (Evidence-Based Analysis)

```
┌─────────────────────────────────────────────────────────────┐
│         AInarrativeIntelligenceAgent (Orchestrator)         │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
┌───────▼────────┐ ┌───▼────────┐ ┌───▼────────┐
│  Narrative Gap │ │   Frame    │ │  Cultural  │
│    Analyzer    │ │ Competition│ │   Signal   │
│                │ │  Analyzer  │ │  Detector  │
└────────────────┘ └────────────┘ └────────────┘

┌───────────────┐     ┌──────────────────┐
│  Resistance   │     │    Adoption      │
│    Mapper     │     │    Readiness     │
│               │     │     Scorer       │
└───────────────┘     └──────────────────┘
```

**Each sub-agent provides:**
- 0-1 normalized scoring
- Evidence-based interpretations
- Specific story IDs as proof
- Actionable recommendations

### Data Model (Neo4j Graph)

**New Node Types:**
- `AIInitiative`: AI projects with official vs actual perceptions
- `AIConcept`: AI terminology with sentiment profiles
- `NarrativeFrame`: How AI is framed (opportunity/threat/tool/partner/replacement)
- `CulturalSignal`: Innovation vs risk-aversion indicators
- `ResistancePattern`: Adoption barriers and manifestations
- `AdoptionBarrier`: Cultural/technical/resource/political obstacles

**Enhanced Story Properties:**
```python
ai_related: bool                    # Is this AI-related?
ai_sentiment: float                 # -1.0 to 1.0
ai_sophistication: str              # basic/intermediate/advanced/expert
innovation_signal: str              # experimentation/learning/caution/fear
agency_frame: str                   # opportunity/threat/tool/partner/replacement
time_frame: str                     # past/present/future focused
narrative_function: str             # vision/success/warning/complication
ai_concepts_mentioned: List[str]    # ["copilot", "automation", "ml"]
experimentation_indicator: bool     # Is experimentation happening?
failure_framing: str                # How failures are discussed
```

### API (40+ Endpoints)

**Strategic Questions:**
```
GET  /ai/analysis/question1              # Team differences
GET  /ai/analysis/question2              # Entrepreneurial culture
GET  /ai/analysis/question3/{id}         # Unified story design
GET  /ai/analysis/question4              # Risk aversion
GET  /ai/analysis/question5              # Language context
POST /ai/analysis/comprehensive          # All questions + dashboard
```

**Sub-Agent Analyses:**
```
GET /ai/analysis/gaps                    # Narrative gap analysis
GET /ai/analysis/frames                  # Frame competition
GET /ai/analysis/culture                 # Innovation culture
GET /ai/analysis/resistance              # Resistance mapping
GET /ai/analysis/readiness               # Adoption readiness
```

**Data & Analytics:**
```
GET /ai/stories/ai                       # AI stories with filters
GET /ai/analytics/sentiment-by-group    # Sentiment breakdown
GET /ai/analytics/frame-distribution    # Frame usage patterns
GET /ai/analytics/adoption-timeline     # Timeline analysis
GET /ai/analytics/influential-stories   # Most-referenced stories
GET /ai/analytics/group-connectivity    # Cross-group references
```

---

## 🚀 Quick Start

**1. Generate sample data** (realistic AI adoption scenario):
```bash
python backend/src/services/ai_data_generator.py
```

**2. Import to Neo4j**:
```cypher
// Run the generated ai_narrative_import.cypher script
```

**3. Start API**:
```bash
uvicorn backend.src.api.main:app --reload
```

**4. Get executive dashboard**:
```bash
curl -X POST http://localhost:8000/ai/analysis/comprehensive \
  -H "Content-Type: application/json" \
  -d '{"initiative_id": "ai_copilot_2024"}'
```

**See full tutorial:** `AI_AGENT_QUICK_START.md`

---

## 📊 Sample Output

### Executive Dashboard
```
📊 EXECUTIVE SUMMARY
============================================================
Our AI adoption readiness is currently at risk, requiring
intervention (45/100), with a cautiously innovative
organizational culture. Narrative alignment across teams
is weak at 38%.

The primary challenge is severe narrative fragmentation:
Teams are telling fundamentally different stories about AI
initiatives. This creates confused priorities, wasted effort,
initiative conflicts.

Immediate priority: Facilitate cross-team storytelling sessions
to develop shared language. This addresses the most critical
blocker and can show results within 30 days.

🚨 RISK SIGNALS
------------------------------------------------------------
CRITICAL: High Risk Aversion Blocking Adoption
  → 3 resistance hotspots identified
  Impact: Initiatives stall, innovation slows
  Action: Address root causes in resistant groups first

HIGH: Severe Narrative Fragmentation
  → Teams telling fundamentally different stories
  Impact: Confused priorities, wasted effort
  Action: Facilitate cross-team dialogue sessions

✅ PRIORITY ACTIONS
------------------------------------------------------------
1. [IMMEDIATE] Facilitate cross-team dialogue to align narratives
   Owner: Internal Communications
   Timeline: 0-30 days
   Success: Narrative alignment score increases to >0.7

2. [IMMEDIATE] Address root causes in customer service team
   Owner: Executive Team
   Timeline: 0-30 days
   Success: Resistance hotspots reduce by 50%

3. [SHORT_TERM] Launch small pilot projects to build confidence
   Owner: Innovation Team
   Timeline: 1-3 months
   Success: Pilot shows positive outcomes in 80% of cases
```

### Team-Specific Report
```
📋 CUSTOMER SERVICE TEAM ANALYSIS
============================================================
Overview:
  Stories: 15
  Avg Sentiment: -0.45 (Negative)
  Dominant Frame: "replacement" (job security concerns)
  Resistance Level: 0.72 (HIGH)

Root Cause Analysis:
  Primary: threat_perception
  Evidence: 8 stories mentioning job security fears

  "They say the AI is here to 'help us,' but everyone knows
   what 'handling 70% of inquiries' really means..."

Recommended Intervention:
  Approach: Reframe & Reassure
  Actions:
    1. Share success stories from similar roles
    2. Provide clear career development paths with AI
    3. Pilot program showing augmentation not replacement
  Timeline: 2-3 months
  Success: Resistance score drops below 0.4
```

---

## 🎯 Use Cases

### Pre-Launch Assessment
**Before** launching a major AI initiative:
- Assess organizational readiness (0-100 score)
- Identify resistance hotspots
- Forecast adoption trajectory
- Design pre-emptive interventions

### Health Monitoring
**During** rollout:
- Track narrative evolution over time
- Detect emerging resistance patterns
- Monitor narrative alignment
- Adjust strategy based on signals

### Intervention Design
**When** adoption stalls:
- Map resistance by group
- Infer root causes
- Design targeted interventions
- Measure intervention effectiveness

### Strategic Communication
**Throughout** the journey:
- Craft messages that resonate
- Bridge competing narratives
- Build unified story
- Connect to existing values

---

## 🏆 Key Features

### Evidence-Based Analysis
Every insight backed by:
- Specific story IDs as proof
- Quantified metrics (0-1 scale)
- Statistical patterns
- Direct quotes from stories

### Multi-Dimensional Scoring
- Narrative alignment (how compatible are stories?)
- Cultural receptivity (innovation vs risk-aversion)
- Trust levels (credibility of leadership)
- Learning orientation (growth vs fixed mindset)
- Leadership coherence (consistent messaging?)
- Coordination narrative (cross-group collaboration)

### Trajectory Forecasting
Predicts adoption path:
- **Accelerating**: High momentum, strong cultural fit
- **Steady**: Moderate progress, some barriers
- **At Risk**: Significant blockers, intervention needed
- **Stalled**: Critical issues, major changes required

### Intervention Playbooks
Group-specific strategies:
- **Past failures** → Acknowledge & Learn
- **Threat perception** → Reframe & Reassure
- **Resource issues** → Resource & Support
- **Value misalignment** → Connect & Align
- **Knowledge gaps** → Educate & Build Skills

---

## 📈 ROI & Impact

### Time Savings
- **Before**: Weeks of surveys, focus groups, analysis
- **After**: Hours to comprehensive insights
- **Ongoing**: Real-time narrative monitoring

### Better Decisions
- Identify resistance early (before it's visible in metrics)
- Target interventions precisely (not blanket approaches)
- Forecast outcomes (don't just react)
- Learn from patterns (systematic improvement)

### Improved Adoption
- Address root causes, not symptoms
- Build on existing strengths
- Create resonant messaging
- Maintain momentum through quick wins

---

## 🛠️ Technical Stack

- **Language**: Python 3.9+
- **Database**: Neo4j 4.4+ (graph database)
- **API**: FastAPI (async, OpenAPI docs)
- **Analysis**: Custom NLP + pattern matching
- **Visualization**: D3.js compatible output
- **Data Model**: Pydantic (validation)

---

## 📚 Documentation

- **Quick Start**: `AI_AGENT_QUICK_START.md` - Get running in 15 minutes
- **Implementation Status**: `AI_AGENT_IMPLEMENTATION_STATUS.md` - Technical details
- **Quick Reference**: `AI_AGENT_QUICK_REFERENCE.md` - Code patterns and templates
- **API Docs**: `/docs` endpoint - Interactive API documentation

---

## 🎓 Core Concepts

### Narrative Intelligence
Instead of asking "Do you support AI?" (survey), we analyze how people naturally talk about AI in their stories. This reveals:
- **What they really think** (not what they'll say in a survey)
- **Cultural patterns** (innovation vs caution)
- **Frame wars** (opportunity vs threat)
- **Root causes** (why resistance exists)

### Frame Analysis
People frame AI differently:
- **Opportunity**: "AI enables new possibilities"
- **Threat**: "AI might replace us"
- **Tool**: "AI is just another technology"
- **Partner**: "AI and humans collaborate"
- **Replacement**: "AI will do our jobs"

Competing frames create confusion and resistance.

### Resistance Patterns
Four types of resistance:
- **Passive**: "Waiting to see" (low priority)
- **Skeptical**: "Show me proof" (evidence needed)
- **Active**: "Won't work here" (direct opposition)
- **Fearful**: "Might lose my job" (existential threat)

Each requires different interventions.

### Root Cause Analysis
Five common causes:
1. **Past failures**: Previous AI projects failed
2. **Threat perception**: Job security concerns
3. **Resource issues**: No time/training/support
4. **Value misalignment**: AI conflicts with values
5. **Knowledge gaps**: Don't understand AI

---

## 🔬 Research Foundation

Based on:
- **Narrative theory**: Stories reveal culture (Bruner, Polkinghorne)
- **Sensemaking**: How organizations interpret change (Weick)
- **Diffusion of innovation**: Adoption patterns (Rogers)
- **Organizational change**: Resistance and readiness (Kotter)
- **Frame analysis**: How framing shapes perception (Goffman)

---

## 🤝 Contributing & Extending

### Add New Analyzers
Follow the sub-agent pattern:
```python
class YourAnalyzer:
    def __init__(self, neo4j_client):
        self.neo4j = neo4j_client

    def analyze(self) -> Dict[str, Any]:
        # 1. Get data from graph
        # 2. Analyze across dimensions
        # 3. Generate 0-1 scores
        # 4. Provide interpretations
        # 5. Include recommendations
        return {
            'score': 0.65,
            'evidence': [...],
            'interpretation': "...",
            'recommendations': [...]
        }
```

### Add New Frames
Extend `AgencyFrame` enum in `models/story.py`:
```python
class AgencyFrame(str, Enum):
    OPPORTUNITY = "opportunity"
    YOUR_FRAME = "your_frame"  # Add here
```

### Add Custom Interventions
Extend intervention map in `executive_dashboard.py`

---

## 🙏 Credits & Acknowledgments

Built on the Narrative Analysis Tool foundation with:
- Neo4j graph database for relationship modeling
- FastAPI for modern async API
- Pydantic for data validation
- Evidence-based analysis patterns

---

## 📧 Support

- **Issues**: See GitHub issues
- **Questions**: Check API docs at `/docs`
- **Examples**: See `AI_AGENT_QUICK_START.md`

---

**Ready to understand how your organization really thinks about AI?**

Start with the Quick Start Guide and generate sample data to see it in action.
