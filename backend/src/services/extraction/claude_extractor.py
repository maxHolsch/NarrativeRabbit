"""
LLM-based narrative extraction using Claude API.
"""
import json
from typing import Dict, Any, Optional, List
import logging
from anthropic import Anthropic, APIError

from ...config import settings
from ...models import (
    Story, ContentLayer, StructureLayer, ActorLayer, ThemeLayer, ContextLayer,
    StoryType, NarrativeArc, TellingPurpose
)

logger = logging.getLogger(__name__)


class ClaudeNarrativeExtractor:
    """Extract structured narrative elements using Claude API."""

    def __init__(self):
        """Initialize the extractor with Claude API client."""
        self.client = Anthropic(api_key=settings.anthropic_api_key)
        self.model = "claude-3-sonnet-20240229"

    def extract_narrative_elements(self, text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Extract narrative elements from raw text using Claude.

        Args:
            text: Raw narrative text
            context: Optional context (source, author, timestamp, etc.)

        Returns:
            Extracted narrative elements as dictionary
        """
        prompt = self._build_extraction_prompt(text, context)

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0.1,  # Low temperature for consistent extraction
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            # Parse the response
            extracted_json = self._parse_response(response.content[0].text)
            return extracted_json

        except APIError as e:
            logger.error(f"Claude API error: {e}")
            raise
        except Exception as e:
            logger.error(f"Extraction failed: {e}")
            raise

    def _build_extraction_prompt(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Build the extraction prompt for Claude."""

        context_str = ""
        if context:
            context_str = f"\n\nCONTEXT:\n{json.dumps(context, indent=2)}"

        return f"""You are an expert at analyzing organizational narratives and extracting structured information.

Analyze the following text and extract narrative elements. Return your analysis as valid JSON matching the specified schema.

TEXT:
{text}
{context_str}

Extract the following elements:

1. **SUMMARY**: A 2-3 sentence summary of what happened
2. **ACTORS**:
   - protagonists: Main actors who drove the action (list of names/roles)
   - stakeholders: People who were affected (list)
   - decision_makers: People who made key decisions (list)
   - group_affiliations: Teams/departments involved (list)

3. **PROBLEM**: What issue or challenge did this address?

4. **DECISION_POINTS**: Key choices that were made (list of decision descriptions)

5. **OUTCOME**: What resulted from these events?

6. **THEMES**: Core themes (select 3-5 from: innovation, reliability, collaboration, technical-debt, scaling, speed, learning, risk-management, communication, customer-first, prioritization, experimentation, culture, process)

7. **VALUES**: What organizational values does this express? (select from: integrity, excellence, innovation, collaboration, customer-centric, transparency, growth-mindset, accountability, quality)

8. **STORY_TYPE**: One of: success, failure, conflict, decision, learning, crisis

9. **NARRATIVE_ARC**: Identify these stages with brief descriptions:
   - setup: Initial situation
   - complication: Problem introduced
   - rising_action: Attempts to resolve
   - climax: Key turning point
   - resolution: How it concluded
   - reflection: What was learned

10. **CAUSAL_CHAIN**: Sequence of cause-effect relationships
    Format: [
      {{"cause": "X happened", "effect": "which led to Y"}},
      {{"cause": "Y occurred", "effect": "which resulted in Z"}}
    ]

11. **LESSONS_LEARNED**: Key takeaways (list of 2-4 lessons)

12. **KEY_QUOTES**: Notable quotes from the text (list of 1-3 quotes)

13. **TEMPORAL_SEQUENCE**: Timeline of events (list)

14. **TELLING_PURPOSE**: Why is this story being told? One of: teaching, warning, celebrating, explaining, bonding, persuading

Return your response as a valid JSON object with this exact structure:

{{
  "summary": "string",
  "actors": {{
    "protagonists": ["string"],
    "stakeholders": ["string"],
    "decision_makers": ["string"],
    "group_affiliations": ["string"]
  }},
  "problem": "string",
  "decision_points": ["string"],
  "outcome": "string",
  "themes": ["string"],
  "values": ["string"],
  "story_type": "string",
  "narrative_arc": {{
    "setup": "string",
    "complication": "string",
    "rising_action": "string",
    "climax": "string",
    "resolution": "string",
    "reflection": "string"
  }},
  "causal_chain": [
    {{"cause": "string", "effect": "string"}}
  ],
  "lessons_learned": ["string"],
  "key_quotes": ["string"],
  "temporal_sequence": ["string"],
  "telling_purpose": "string"
}}

Respond with ONLY the JSON object, no additional text."""

    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Claude's response into structured data."""
        try:
            # Try to extract JSON from the response
            # Claude might wrap it in markdown code blocks
            if "```json" in response_text:
                start = response_text.find("```json") + 7
                end = response_text.find("```", start)
                json_str = response_text[start:end].strip()
            elif "```" in response_text:
                start = response_text.find("```") + 3
                end = response_text.find("```", start)
                json_str = response_text[start:end].strip()
            else:
                json_str = response_text.strip()

            return json.loads(json_str)

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.error(f"Response text: {response_text}")
            raise

    def create_story_from_extraction(
        self,
        extracted: Dict[str, Any],
        story_id: str,
        source: str = "extraction",
        timestamp: Optional[str] = None
    ) -> Story:
        """
        Convert extracted data into a Story object.

        Args:
            extracted: Extracted narrative elements
            story_id: Unique story identifier
            source: Source of the narrative
            timestamp: When the events occurred

        Returns:
            Complete Story object
        """
        from datetime import datetime

        # Map extracted data to Story layers
        content = ContentLayer(
            summary=extracted.get("summary", ""),
            full_text="",  # Would come from original text
            key_quotes=extracted.get("key_quotes", []),
            outcome=extracted.get("outcome", "")
        )

        # Map narrative arc
        arc_data = extracted.get("narrative_arc", {})
        narrative_arc = {
            NarrativeArc.SETUP: arc_data.get("setup", ""),
            NarrativeArc.COMPLICATION: arc_data.get("complication", ""),
            NarrativeArc.RISING_ACTION: arc_data.get("rising_action", ""),
            NarrativeArc.CLIMAX: arc_data.get("climax", ""),
            NarrativeArc.RESOLUTION: arc_data.get("resolution", ""),
            NarrativeArc.REFLECTION: arc_data.get("reflection", "")
        }

        structure = StructureLayer(
            story_type=StoryType(extracted.get("story_type", "learning")),
            narrative_arc=narrative_arc,
            temporal_sequence=extracted.get("temporal_sequence", []),
            causal_chain=extracted.get("causal_chain", [])
        )

        actors_data = extracted.get("actors", {})
        actors = ActorLayer(
            protagonists=actors_data.get("protagonists", []),
            stakeholders=actors_data.get("stakeholders", []),
            decision_makers=actors_data.get("decision_makers", []),
            group_affiliations=actors_data.get("group_affiliations", [])
        )

        themes = ThemeLayer(
            primary_themes=extracted.get("themes", [])[:5],  # Max 5
            problems_addressed=[extracted.get("problem", "")],
            values_expressed=extracted.get("values", []),
            lessons_learned=extracted.get("lessons_learned", [])
        )

        # Parse timestamp
        story_timestamp = datetime.utcnow()
        if timestamp:
            try:
                story_timestamp = datetime.fromisoformat(timestamp)
            except:
                pass

        context = ContextLayer(
            timestamp=story_timestamp,
            era=None,
            department=actors_data.get("group_affiliations", [None])[0] if actors_data.get("group_affiliations") else None,
            project=None,
            why_told=TellingPurpose(extracted.get("telling_purpose", "teaching")),
            trigger_events=[]
        )

        # Create story
        story = Story(
            id=story_id,
            content=content,
            structure=structure,
            actors=actors,
            themes=themes,
            context=context,
            variations=[],
            source=source,
            confidence_score=0.85,  # Could be calculated based on extraction quality
            tags=extracted.get("themes", [])
        )

        return story

    def extract_and_create_story(
        self,
        text: str,
        story_id: str,
        source: str = "extraction",
        context: Optional[Dict[str, Any]] = None
    ) -> Story:
        """
        Extract narrative elements and create a Story object in one step.

        Args:
            text: Raw narrative text
            story_id: Unique identifier
            source: Source of the narrative
            context: Optional context information

        Returns:
            Complete Story object
        """
        # Extract elements
        extracted = self.extract_narrative_elements(text, context)

        # Create story
        timestamp = context.get("timestamp") if context else None
        story = self.create_story_from_extraction(extracted, story_id, source, timestamp)

        # Add full text
        story.content.full_text = text

        return story

    def analyze_perspective(
        self,
        text: str,
        teller_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze how a specific perspective frames a narrative.

        Args:
            text: Narrative text
            teller_info: Information about who is telling (role, department, etc.)

        Returns:
            Perspective analysis
        """
        prompt = f"""Analyze the perspective and framing in this narrative.

NARRATIVE:
{text}

TELLER INFO:
{json.dumps(teller_info, indent=2)}

Analyze:
1. **FRAMING**: How does this teller position/frame the story?
2. **EMPHASIS**: What aspects are highlighted or emphasized?
3. **DOWNPLAYED**: What aspects are minimized or omitted?
4. **BIAS**: What biases or viewpoints are evident?
5. **AUDIENCE**: Who seems to be the intended audience?

Return as JSON:
{{
  "framing": "string describing how story is framed",
  "emphasis": ["list", "of", "emphasized", "aspects"],
  "downplayed": ["list", "of", "minimized", "aspects"],
  "bias": "string describing evident biases",
  "intended_audience": ["list", "of", "audience", "groups"]
}}

Respond with ONLY the JSON object."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}]
            )

            return self._parse_response(response.content[0].text)

        except Exception as e:
            logger.error(f"Perspective analysis failed: {e}")
            return {
                "framing": "",
                "emphasis": [],
                "downplayed": [],
                "bias": "",
                "intended_audience": []
            }
