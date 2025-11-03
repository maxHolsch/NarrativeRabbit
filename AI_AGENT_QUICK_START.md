# AI Narrative Intelligence Agent - Quick Start Guide

Get up and running with the AI Narrative Intelligence Agent in 15 minutes.

## 🎯 What You Can Do

Answer 5 strategic questions about your organization's AI adoption:

1. **How do different teams talk about AI differently?**
   → Reveals vocabulary gaps, frame conflicts, and misalignment

2. **Do we have an entrepreneurial culture?**
   → Measures innovation vs risk-aversion, learning orientation

3. **Can you design a unified story?**
   → Creates messaging strategy that bridges competing narratives

4. **Are we risk-averse, and where?**
   → Maps resistance patterns, root causes, intervention strategies

5. **Why does language vary by context?**
   → Explains leadership vs team differences, trust factors

## 🚀 Quick Start

### Step 1: Generate Sample Data (2 minutes)

```bash
cd backend/src/services
python ai_data_generator.py
```

This creates:
- ✅ `ai_narrative_sample_data.json` - Realistic AI adoption stories
- ✅ `ai_narrative_import.cypher` - Neo4j import script

**What the data shows**: A mid-size tech company introducing GitHub Copilot and AI customer service, revealing tensions between innovation and caution.

### Step 2: Import to Neo4j (3 minutes)

```cypher
// In Neo4j Browser, run:
:play file:///path/to/ai_narrative_import.cypher
```

Or via Python:
```python
from backend.src.db.neo4j_client import Neo4jClient
from backend.src.services.ai_data_generator import AIDataGenerator

client = Neo4jClient()
generator = AIDataGenerator()
data = generator.generate_all_data()

# Import stories and initiatives
# (full import code in scripts/import_ai_data.py)
```

### Step 3: Start the API (2 minutes)

```bash
cd backend
uvicorn src.api.main:app --reload
```

Visit: http://localhost:8000/docs for interactive API documentation

### Step 4: Run Your First Analysis (5 minutes)

#### Option A: Via API (Recommended)

**Get Executive Dashboard:**
```bash
curl http://localhost:8000/ai/analysis/comprehensive \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"initiative_id": "ai_copilot_2024", "generate_action_plan": true}'
```

**Answer Individual Questions:**
```bash
# Q1: Team differences
curl http://localhost:8000/ai/analysis/question1?initiative_id=ai_copilot_2024

# Q2: Entrepreneurial culture
curl http://localhost:8000/ai/analysis/question2

# Q4: Risk aversion
curl http://localhost:8000/ai/analysis/question4
```

#### Option B: Via Python

```python
from backend.src.services.ai_narrative_intelligence_agent import AInarrativeIntelligenceAgent
from backend.src.services.reporting.executive_dashboard import ExecutiveDashboard
from backend.src.db.neo4j_client import Neo4jClient

# Initialize
client = Neo4jClient()
agent = AInarrativeIntelligenceAgent(client)
dashboard = ExecutiveDashboard(agent)

# Generate executive dashboard
report = dashboard.generate_dashboard(initiative_id='ai_copilot_2024')

print("📊 EXECUTIVE SUMMARY")
print("=" * 60)
print(report['executive_summary'])

print("\n🚨 RISK SIGNALS")
for risk in report['risk_signals']:
    print(f"\n{risk['severity'].upper()}: {risk['title']}")
    print(f"  → {risk['description']}")
    print(f"  Action: {risk['recommended_action']}")

print("\n✅ PRIORITY ACTIONS")
for i, action in enumerate(report['priority_actions'][:3], 1):
    print(f"\n{i}. [{action['priority'].upper()}] {action['action']}")
    print(f"   Owner: {action['suggested_owner']}")
    print(f"   Timeline: {action['timeline']}")
```

## 📖 Example Output

### Executive Dashboard
```
Overall Health: 45/100 (At Risk - Intervention Needed) 🔶

Our AI adoption readiness is currently at risk, requiring intervention
(45/100), with a cautiously innovative organizational culture. Narrative
alignment across teams is weak at 38%.

The primary challenge is severe narrative fragmentation: Teams are telling
fundamentally different stories about AI initiatives. This creates confused
priorities, wasted effort, initiative conflicts. Additional concerns include
High Risk Aversion Blocking Adoption.

Immediate priority: Facilitate cross-team storytelling sessions to develop
shared language. This addresses the most critical blocker and can show
results within 30 days.

RISK SIGNALS:
🚨 CRITICAL: High Risk Aversion Blocking Adoption
   → 3 resistance hotspots identified
   Action: Address root causes in resistant groups before expanding

⚠️  HIGH: Severe Narrative Fragmentation
   → Teams telling fundamentally different stories
   Action: Facilitate cross-team storytelling sessions

PRIORITY ACTIONS:
1. [IMMEDIATE] Facilitate cross-team dialogue to align narratives
   Owner: Internal Communications
   Timeline: 0-30 days
   Metric: Narrative alignment score increases to >0.7

2. [IMMEDIATE] Address root causes in customer service team
   Owner: Executive Team
   Timeline: 0-30 days
   Metric: Resistance hotspots reduce by 50%

3. [SHORT_TERM] Launch small pilot projects to build confidence
   Owner: Innovation Team
   Timeline: 1-3 months
   Metric: Pilot shows positive outcomes in 80% of cases
```

## 🎓 Understanding the Analyses

### Narrative Gap Analysis
**What it shows**: Differences between official messaging and actual employee stories

**Key metrics**:
- Vocabulary alignment (0-1): How much language is shared
- Frame conflicts: Are leaders and teams using different frames?
- Sentiment gaps: Do official and actual stories have different emotional tones?

**When to use**: When rollout messaging isn't resonating

### Frame Competition Analysis
**What it shows**: Different ways people are framing AI (opportunity vs threat vs tool vs replacement)

**Key insights**:
- Which frames dominate by group
- Where frames compete or conflict
- Common ground across frames

**When to use**: When you need to craft unified messaging

### Cultural Signal Detection
**What it shows**: Is your organization innovative or risk-averse?

**Key dimensions**:
- Experimentation (do people try new things?)
- Failure tolerance (is failure okay?)
- Employee agency (top-down vs bottom-up?)
- Iteration speed (fast or slow?)

**When to use**: Assessing readiness for change initiatives

### Resistance Mapping
**What it shows**: Where and why AI adoption is stalling

**Pattern types**:
- Passive: "Waiting to see", low priority
- Skeptical: "Show me proof"
- Active: "Won't work here"
- Fearful: "Might lose my job"

**Root causes identified**:
- Past failures casting shadows
- Threat perception (job security fears)
- Resource constraints
- Value misalignment
- Knowledge gaps

**When to use**: When adoption is slower than expected

### Adoption Readiness Scoring
**What it shows**: 6-dimensional readiness assessment with trajectory forecast

**Dimensions scored**:
- Narrative alignment (20%)
- Cultural receptivity (20%)
- Trust levels (20%)
- Learning orientation (15%)
- Leadership coherence (15%)
- Coordination narrative (10%)

**Trajectories**:
- Accelerating: High momentum, strong signals
- Steady: Moderate progress
- At risk: Significant blockers present
- Stalled: Major intervention required

**When to use**: Before launching major AI initiatives

## 🛠️ Common Workflows

### Workflow 1: Pre-Launch Assessment
**Goal**: Should we launch this AI initiative?

```python
# 1. Assess overall readiness
readiness = agent.readiness_scorer.assess_readiness()

if readiness['overall_score'] < 0.5:
    print("⚠️  Not ready. Address these issues first:")
    for weakness in readiness['weaknesses']:
        print(f"  - {weakness}")
else:
    print("✅ Ready to proceed")

# 2. Check for resistance hotspots
resistance = agent.resistance_mapper.map_resistance_landscape()

if resistance['overall_severity'] > 0.6:
    print("🚨 High resistance detected. Focus on these groups:")
    for hotspot in resistance['hotspots']:
        print(f"  - {hotspot['group']}: {hotspot['patterns']}")
```

### Workflow 2: Initiative Health Check
**Goal**: How's our AI initiative doing?

```python
# Run comprehensive analysis for specific initiative
dashboard = ExecutiveDashboard(agent)
report = dashboard.generate_dashboard(initiative_id='ai_copilot_2024')

# Review health metrics
health = report['health_metrics']
print(f"Health Score: {health['overall_health']['score']}/100")
print(f"Status: {health['overall_health']['label']}")

# Check risk signals
if report['risk_signals']:
    print("\n⚠️  Risks Detected:")
    for risk in report['risk_signals']:
        if risk['severity'] in ['critical', 'high']:
            print(f"  {risk['title']}: {risk['recommended_action']}")
```

### Workflow 3: Intervention Design
**Goal**: How do we fix resistance in a specific team?

```python
from backend.src.services.reporting.executive_dashboard import DetailedReport

reporter = DetailedReport(agent)

# Get team-specific analysis
team_report = reporter.generate_team_report(group='customer_service')

# Review root causes
print(f"\nPrimary Cause: {team_report['root_causes']['primary_cause'][0]}")

# Get intervention plan
for intervention in team_report['recommended_interventions']:
    print(f"\nApproach: {intervention['approach']}")
    print(f"Actions:")
    for action in intervention['actions']:
        print(f"  - {action}")
    print(f"Timeline: {intervention['timeline']}")
```

## 📊 Sample Data Story

The generated sample data tells a realistic story:

**Setup** (Days 0-30):
- Leadership announces GitHub Copilot and AI customer service
- Optimistic official messaging emphasizing productivity and empowerment

**Early Adoption** (Days 30-60):
- Engineering team splits: early adopters vs skeptics
- Customer service agents express job security fears
- Quality concerns emerge

**Resistance Builds** (Days 60-120):
- Cautionary tales spread ("insecure code", "customer frustration")
- Past AI failure referenced, casting doubt
- Pressure to show ROI creates tension
- Competing frames emerge (tool vs threat vs partner)

**Current State** (Days 120-180):
- Mixed results: some teams benefiting, others resisting
- Clear narrative gaps between leadership and teams
- Risk aversion patterns visible
- Need for intervention evident

This mirrors real organizational AI adoption journeys.

## 🎯 Tips for Real Data

When using with your own data:

1. **Collect Diverse Stories**: Get stories from all levels and groups
2. **Include Official Narratives**: Capture leadership messaging
3. **Tag AI Properties**: Use the AI analysis layer (sentiment, sophistication, frame)
4. **Link Initiatives**: Connect stories to specific AI initiatives
5. **Track Over Time**: Analyze evolution of narratives

## 🆘 Troubleshooting

**"No stories found"**
- Check that `ai_related = true` is set on stories
- Verify Neo4j connection and data import

**"Low confidence results"**
- Need more stories (aim for 20+ per initiative, 50+ overall)
- Ensure diverse group representation

**"Analysis seems off"**
- Review story tagging (sentiment, sophistication, frames)
- Check that AI concepts are properly captured

## 📚 Next Steps

1. **Try with real data**: Collect your organization's AI stories
2. **Customize frames**: Adjust frame types for your context
3. **Build dashboards**: Create visualizations using the API
4. **Schedule regular analysis**: Track adoption over time
5. **Design interventions**: Use insights to guide strategy

## 💡 Pro Tips

- **Start small**: Pilot with one initiative before organization-wide analysis
- **Involve stakeholders**: Share dashboards to build buy-in
- **Act on insights**: Use recommendations to drive actual interventions
- **Track progress**: Re-run analyses quarterly to measure improvement
- **Share stories**: Use evidence (actual quotes) in presentations

---

**Ready to go deeper?** See `AI_AGENT_IMPLEMENTATION_STATUS.md` for technical details.

**Questions?** Check the API documentation at `/docs` or review example queries in the codebase.
