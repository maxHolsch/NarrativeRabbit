"""
Conversational AI Chat Agent for Narrative Graph Exploration

Provides natural language interface to query and explore the narrative knowledge graph.
Integrates with AInarrativeIntelligenceAgent for strategic analysis and Neo4j for data queries.
"""

import logging
from typing import Dict, Any, List, Optional
from anthropic import Anthropic
from datetime import datetime

from ..config import settings
from ..db.neo4j_client import neo4j_client
from .ai_narrative_intelligence_agent import AInarrativeIntelligenceAgent
from .queries.ai_queries import AIQueries

logger = logging.getLogger(__name__)


class ChatAgent:
    """
    Conversational agent for narrative graph exploration.

    Handles:
    - Intent classification
    - Query routing
    - Context-aware responses
    - Source citation
    """

    def __init__(self):
        """Initialize chat agent with Claude and Neo4j access."""
        self.claude = Anthropic(api_key=settings.anthropic_api_key)
        self.model = "claude-3-5-sonnet-20241022"
        self.ai_agent = AInarrativeIntelligenceAgent(neo4j_client)
        self.ai_queries = AIQueries(neo4j_client)

    async def chat(self, message: str, conversation_history: Optional[List[Dict]] = None,
                   context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process a chat message and generate response.

        Args:
            message: User's message
            conversation_history: Previous messages in conversation
            context: Optional context (initiative_id, etc.)

        Returns:
            Dict with response, sources, suggested_followups, and metadata
        """
        try:
            # Step 1: Classify intent
            intent = await self._classify_intent(message, conversation_history, context)
            logger.info(f"Classified intent: {intent['type']}")

            # Step 2: Execute query based on intent
            data = await self._execute_query(intent, message, context)

            # Step 3: Generate natural language response
            response = await self._generate_response(message, intent, data, conversation_history)

            # Step 4: Extract sources and generate follow-ups
            sources = self._extract_sources(data, intent)
            followups = self._generate_followups(intent, data)

            return {
                "response": response,
                "sources": sources,
                "suggested_followups": followups,
                "intent": intent['type'],
                "data_summary": self._summarize_data(data),
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error in chat processing: {e}", exc_info=True)
            return {
                "response": f"I encountered an error processing your request: {str(e)}. Please try rephrasing your question.",
                "sources": [],
                "suggested_followups": [],
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def _classify_intent(self, message: str, history: Optional[List[Dict]],
                              context: Optional[Dict]) -> Dict[str, Any]:
        """
        Classify user intent to route to appropriate handler.

        Intent types:
        - story_search: Find specific stories
        - initiative_query: Ask about AI initiatives
        - strategic_analysis: Run one of the 5 strategic questions
        - graph_exploration: Explore relationships and patterns
        - general_question: General information request
        """
        classification_prompt = f"""Classify this user message for a narrative intelligence system.

User Message: "{message}"

{"Recent context: " + str(history[-3:]) if history else ""}
{"Current context: " + str(context) if context else ""}

Classify the intent as ONE of:
1. story_search - User wants to find specific stories (e.g., "show me stories about X", "find stories from team Y")
2. initiative_query - User asks about AI initiatives (e.g., "what initiatives are active?", "tell me about chatbot project")
3. strategic_analysis - User wants strategic analysis (e.g., "are we risk-averse?", "do we have entrepreneurial culture?")
4. graph_exploration - User wants to explore patterns/relationships (e.g., "how are teams connected?", "what themes are common?")
5. general_question - General information or clarification request

Also extract:
- entities: Any specific entities mentioned (team names, initiative names, themes, etc.)
- filters: Any filters implied (date ranges, sentiment, etc.)
- specific_question: Which strategic question if applicable (Q1-Q5)

Respond in JSON format:
{{
  "type": "intent_type",
  "confidence": 0.0-1.0,
  "entities": [...],
  "filters": {{}},
  "specific_question": null or "Q1"|"Q2"|"Q3"|"Q4"|"Q5",
  "reasoning": "brief explanation"
}}"""

        try:
            response = self.claude.messages.create(
                model=self.model,
                max_tokens=500,
                temperature=0.1,
                messages=[{"role": "user", "content": classification_prompt}]
            )

            # Parse JSON response
            import json
            intent_text = response.content[0].text
            intent = json.loads(intent_text)
            return intent

        except Exception as e:
            logger.error(f"Intent classification error: {e}")
            # Default to general_question if classification fails
            return {
                "type": "general_question",
                "confidence": 0.5,
                "entities": [],
                "filters": {},
                "specific_question": None,
                "reasoning": "Classification failed, defaulting to general"
            }

    async def _execute_query(self, intent: Dict, message: str, context: Optional[Dict]) -> Dict[str, Any]:
        """Execute appropriate query based on intent."""
        intent_type = intent['type']

        try:
            if intent_type == "story_search":
                return await self._search_stories(intent, context)

            elif intent_type == "initiative_query":
                return await self._query_initiatives(intent, context)

            elif intent_type == "strategic_analysis":
                return await self._run_strategic_analysis(intent, context)

            elif intent_type == "graph_exploration":
                return await self._explore_graph(intent, context)

            else:  # general_question
                return await self._handle_general_question(message, intent, context)

        except Exception as e:
            logger.error(f"Query execution error: {e}")
            return {"error": str(e), "data": []}

    async def _search_stories(self, intent: Dict, context: Optional[Dict]) -> Dict[str, Any]:
        """Search for stories based on intent entities and filters."""
        entities = intent.get('entities', [])
        filters = intent.get('filters', {})

        # Extract search parameters
        themes = [e for e in entities if not any(x in e.lower() for x in ['team', 'group', 'department'])]
        groups = [e for e in entities if any(x in e.lower() for x in ['team', 'group', 'department'])]

        # Search stories
        stories = self.ai_queries.get_all_ai_stories(limit=50)

        # Apply filters
        filtered_stories = stories
        if themes:
            filtered_stories = [s for s in filtered_stories
                              if any(theme.lower() in str(s.get('primary_themes', [])).lower()
                                    for theme in themes)]
        if groups:
            filtered_stories = [s for s in filtered_stories
                              if any(group.lower() in str(s.get('teller_group', '')).lower()
                                    for group in groups)]

        return {
            "type": "stories",
            "count": len(filtered_stories),
            "stories": filtered_stories[:10],  # Return top 10
            "total_found": len(filtered_stories),
            "search_terms": {"themes": themes, "groups": groups}
        }

    async def _query_initiatives(self, intent: Dict, context: Optional[Dict]) -> Dict[str, Any]:
        """Query AI initiatives."""
        initiatives = self.ai_queries.get_all_ai_initiatives()

        # Filter by entities if specified
        entities = intent.get('entities', [])
        if entities:
            filtered = [i for i in initiatives
                       if any(e.lower() in str(i.get('name', '')).lower() or
                             e.lower() in str(i.get('official_description', '')).lower()
                             for e in entities)]
            initiatives = filtered if filtered else initiatives

        return {
            "type": "initiatives",
            "count": len(initiatives),
            "initiatives": initiatives,
            "active_count": len([i for i in initiatives if i.get('status') == 'active'])
        }

    async def _run_strategic_analysis(self, intent: Dict, context: Optional[Dict]) -> Dict[str, Any]:
        """Run strategic analysis using AI agent."""
        question = intent.get('specific_question')
        initiative_id = context.get('initiative_id') if context else None

        result = {}

        if question == "Q1" or not question:
            # Default to Q1 if question unclear
            result = self.ai_agent.answer_question_1(initiative_id)
        elif question == "Q2":
            result = self.ai_agent.answer_question_2()
        elif question == "Q3":
            if initiative_id:
                result = self.ai_agent.answer_question_3(initiative_id)
            else:
                result = {"error": "Q3 requires an initiative_id"}
        elif question == "Q4":
            result = self.ai_agent.answer_question_4()
        elif question == "Q5":
            result = self.ai_agent.answer_question_5(initiative_id)

        return {
            "type": "strategic_analysis",
            "question": question,
            "analysis": result
        }

    async def _explore_graph(self, intent: Dict, context: Optional[Dict]) -> Dict[str, Any]:
        """Explore graph patterns and relationships."""
        # Get connectivity data
        connectivity = self.ai_queries.get_group_connectivity()

        # Get theme distribution
        frame_dist = self.ai_queries.get_frame_distribution()

        # Get sentiment by group
        sentiment = self.ai_queries.get_group_sentiment_summary()

        return {
            "type": "graph_exploration",
            "connectivity": connectivity[:10],
            "frame_distribution": frame_dist[:10],
            "sentiment_by_group": sentiment[:10]
        }

    async def _handle_general_question(self, message: str, intent: Dict,
                                       context: Optional[Dict]) -> Dict[str, Any]:
        """Handle general questions with basic system info."""
        # Get summary statistics
        stories = self.ai_queries.get_all_ai_stories(limit=1000)
        initiatives = self.ai_queries.get_all_ai_initiatives()

        return {
            "type": "general_info",
            "stats": {
                "total_stories": len(stories),
                "total_initiatives": len(initiatives),
                "active_initiatives": len([i for i in initiatives if i.get('status') == 'active'])
            }
        }

    async def _generate_response(self, message: str, intent: Dict, data: Dict,
                                history: Optional[List[Dict]]) -> str:
        """Generate natural language response using Claude."""

        # Build context for response generation
        context_text = f"""User asked: "{message}"

Intent: {intent['type']}
Data retrieved: {self._format_data_for_prompt(data)}

{"Conversation history: " + str(history[-3:]) if history else ""}

Generate a helpful, conversational response that:
1. Directly answers the user's question
2. Cites specific data points and numbers
3. Provides insights and patterns
4. Is concise but complete (2-4 paragraphs max)
5. Uses a friendly, knowledgeable tone

Do not use markdown formatting. Use plain text with clear structure."""

        try:
            response = self.claude.messages.create(
                model=self.model,
                max_tokens=800,
                temperature=0.7,
                messages=[{"role": "user", "content": context_text}]
            )

            return response.content[0].text

        except Exception as e:
            logger.error(f"Response generation error: {e}")
            # Fallback to template response
            return self._generate_fallback_response(data)

    def _format_data_for_prompt(self, data: Dict) -> str:
        """Format data for inclusion in prompt."""
        data_type = data.get('type', 'unknown')

        if data_type == "stories":
            return f"Found {data['count']} stories. Sample: {data.get('stories', [])[:3]}"
        elif data_type == "initiatives":
            return f"Found {data['count']} initiatives: {[i.get('name') for i in data.get('initiatives', [])[:5]]}"
        elif data_type == "strategic_analysis":
            return f"Analysis results: {data.get('analysis', {})}"
        elif data_type == "graph_exploration":
            return f"Graph data: {data}"
        else:
            return str(data)

    def _generate_fallback_response(self, data: Dict) -> str:
        """Generate simple fallback response if Claude fails."""
        data_type = data.get('type', 'unknown')

        if data_type == "stories":
            return f"I found {data['count']} stories matching your criteria. The stories cover various themes and perspectives from different teams."
        elif data_type == "initiatives":
            return f"There are {data['count']} AI initiatives in the system, with {data.get('active_count', 0)} currently active."
        elif data_type == "strategic_analysis":
            return "I've completed the analysis. The results show various patterns and insights about organizational AI adoption."
        else:
            return "I've retrieved the requested information from the narrative graph."

    def _extract_sources(self, data: Dict, intent: Dict) -> List[Dict[str, str]]:
        """Extract source citations from data."""
        sources = []

        if data.get('type') == 'stories':
            for story in data.get('stories', [])[:5]:
                sources.append({
                    "type": "story",
                    "id": story.get('id'),
                    "label": story.get('summary', '')[:100] + "..."
                })

        elif data.get('type') == 'initiatives':
            for initiative in data.get('initiatives', [])[:5]:
                sources.append({
                    "type": "initiative",
                    "id": initiative.get('id'),
                    "label": initiative.get('name', '')
                })

        return sources

    def _generate_followups(self, intent: Dict, data: Dict) -> List[str]:
        """Generate suggested follow-up questions."""
        followups = []
        data_type = data.get('type', 'unknown')

        if data_type == "stories":
            if data.get('count', 0) > 0:
                followups = [
                    "What are the main themes in these stories?",
                    "How do different teams view this topic?",
                    "Show me the most influential stories"
                ]

        elif data_type == "initiatives":
            followups = [
                "What do people think about these initiatives?",
                "Are we risk-averse in our approach?",
                "Show me stories related to these initiatives"
            ]

        elif data_type == "strategic_analysis":
            question = data.get('question')
            if question == "Q4":
                followups = [
                    "Which teams are most affected?",
                    "What are the root causes of resistance?",
                    "How can we reduce risk aversion?"
                ]
            else:
                followups = [
                    "Can you analyze another aspect?",
                    "What are the key recommendations?",
                    "Show me related stories"
                ]

        else:
            followups = [
                "Tell me about active AI initiatives",
                "Are we ready for AI adoption?",
                "Show me recent stories"
            ]

        return followups[:3]  # Return top 3

    def _summarize_data(self, data: Dict) -> Dict[str, Any]:
        """Create summary of data for client."""
        return {
            "type": data.get('type', 'unknown'),
            "count": data.get('count', 0),
            "has_analysis": 'analysis' in data
        }
