"""
Import Discord chat CSV and run narrative analysis.

This script reads the Discord chat export CSV and uses Claude API
to extract narrative elements from conversations.
"""
import csv
import os
import sys
import logging
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.extraction.claude_extractor import ClaudeNarrativeExtractor
from src.database.neo4j_repository import Neo4jRepository
from src.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def read_discord_csv(csv_path: str):
    """Read and parse Discord CSV file."""
    messages = []

    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Skip empty messages or links-only
            content = row.get('Content', '').strip()
            if not content or content.startswith('http'):
                continue

            messages.append({
                'date': row.get('Date', ''),
                'username': row.get('Username', ''),
                'content': content,
                'mentions': row.get('Mentions', ''),
                'link': row.get('link', '')
            })

    logger.info(f"Read {len(messages)} messages from CSV")
    return messages


def group_messages_by_conversation(messages, time_window_minutes=30):
    """
    Group messages into conversations based on time proximity.

    Messages within time_window_minutes of each other are considered
    part of the same conversation.
    """
    conversations = []
    current_conv = []
    last_timestamp = None

    for msg in messages:
        try:
            # Parse timestamp
            timestamp = datetime.strptime(msg['date'], '%Y-%m-%d,%H:%M:%S')

            # Start new conversation if time gap is too large
            if last_timestamp and (timestamp - last_timestamp).total_seconds() > time_window_minutes * 60:
                if current_conv:
                    conversations.append(current_conv)
                current_conv = []

            current_conv.append(msg)
            last_timestamp = timestamp

        except Exception as e:
            logger.warning(f"Failed to parse timestamp: {msg['date']} - {e}")
            continue

    # Add final conversation
    if current_conv:
        conversations.append(current_conv)

    logger.info(f"Grouped into {len(conversations)} conversations")
    return conversations


def format_conversation_for_analysis(conversation):
    """Format a conversation into a narrative text for Claude analysis."""
    if not conversation:
        return "", {}

    # Build narrative text
    lines = []
    participants = set()

    for msg in conversation:
        username = msg['username']
        participants.add(username)
        content = msg['content']
        date = msg['date']

        lines.append(f"[{date}] {username}: {content}")

    text = "\n".join(lines)

    # Build context
    context = {
        'source': 'Discord',
        'timestamp': conversation[0]['date'],
        'participants': list(participants),
        'message_count': len(conversation)
    }

    return text, context


def analyze_discord_conversations(csv_path: str, min_messages=3, max_conversations=None):
    """
    Main function to analyze Discord conversations.

    Args:
        csv_path: Path to Discord CSV export
        min_messages: Minimum messages to consider as a conversation
        max_conversations: Maximum number of conversations to process (None = all)
    """
    logger.info(f"Starting Discord narrative analysis from {csv_path}")

    # Initialize services
    extractor = ClaudeNarrativeExtractor()
    repo = Neo4jRepository(
        uri=settings.neo4j_uri,
        username=settings.neo4j_username,
        password=settings.neo4j_password
    )

    try:
        # Read and group messages
        messages = read_discord_csv(csv_path)
        conversations = group_messages_by_conversation(messages)

        # Filter by minimum size
        conversations = [c for c in conversations if len(c) >= min_messages]
        logger.info(f"Processing {len(conversations)} conversations with {min_messages}+ messages")

        # Limit if specified
        if max_conversations:
            conversations = conversations[:max_conversations]
            logger.info(f"Limited to first {max_conversations} conversations")

        # Process each conversation
        processed_count = 0
        error_count = 0

        for i, conv in enumerate(conversations):
            try:
                logger.info(f"\n{'='*60}")
                logger.info(f"Processing conversation {i+1}/{len(conversations)}")
                logger.info(f"Messages: {len(conv)}, Participants: {len(set(m['username'] for m in conv))}")

                # Format for analysis
                text, context = format_conversation_for_analysis(conv)

                # Skip very short conversations
                if len(text) < 100:
                    logger.info("Skipping - too short")
                    continue

                logger.info(f"Text length: {len(text)} characters")

                # Extract narrative using Claude
                story_id = f"discord_conv_{i+1:03d}"
                logger.info(f"Extracting narrative elements with Claude API...")

                story = extractor.extract_and_create_story(
                    text=text,
                    story_id=story_id,
                    source="Discord",
                    context=context
                )

                logger.info(f"✓ Story created: {story.id}")
                logger.info(f"  Summary: {story.content.summary[:100]}...")
                logger.info(f"  Type: {story.structure.story_type}")
                logger.info(f"  Themes: {', '.join(story.themes.primary_themes)}")
                logger.info(f"  Actors: {len(story.actors.protagonists)} protagonists")

                # Save to database
                logger.info("Saving to Neo4j...")
                repo.add_story(story)

                processed_count += 1
                logger.info(f"✓ Successfully saved story {story.id}")

            except Exception as e:
                error_count += 1
                logger.error(f"✗ Error processing conversation {i+1}: {e}", exc_info=True)
                continue

        # Summary
        logger.info(f"\n{'='*60}")
        logger.info(f"ANALYSIS COMPLETE")
        logger.info(f"{'='*60}")
        logger.info(f"Total conversations: {len(conversations)}")
        logger.info(f"Successfully processed: {processed_count}")
        logger.info(f"Errors: {error_count}")
        logger.info(f"Success rate: {processed_count/len(conversations)*100:.1f}%")

    finally:
        repo.close()
        logger.info("Database connection closed")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Import Discord CSV and run narrative analysis')
    parser.add_argument('csv_path', help='Path to Discord CSV export file')
    parser.add_argument('--min-messages', type=int, default=3,
                       help='Minimum messages per conversation (default: 3)')
    parser.add_argument('--max-conversations', type=int, default=None,
                       help='Maximum conversations to process (default: all)')
    parser.add_argument('--time-window', type=int, default=30,
                       help='Time window in minutes for grouping messages (default: 30)')

    args = parser.parse_args()

    # Verify file exists
    if not os.path.exists(args.csv_path):
        logger.error(f"File not found: {args.csv_path}")
        sys.exit(1)

    # Run analysis
    analyze_discord_conversations(
        csv_path=args.csv_path,
        min_messages=args.min_messages,
        max_conversations=args.max_conversations
    )
