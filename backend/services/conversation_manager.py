"""
Conversation Manager - Handles conversation context and history
"""

import logging
from datetime import datetime

logger = logging.getLogger('sales_coach')


class ConversationManager:
    """Manages conversation history and context for AI analysis"""

    def __init__(self):
        """Initialize conversation manager"""
        self.conversations = {}
        logger.info("✅ Conversation manager initialized")

    def start_conversation(self, session_id):
        """
        Start tracking a new conversation

        Args:
            session_id: Unique session identifier
        """
        self.conversations[session_id] = {
            'messages': [],
            'start_time': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat()
        }

        logger.info(f"Started conversation tracking for session: {session_id}")

    def add_message(self, session_id, text, speaker='unknown'):
        """
        Add a message to the conversation

        Args:
            session_id: Session ID
            text: Message text
            speaker: Who said it (customer/salesperson/unknown)
        """
        if session_id not in self.conversations:
            logger.warning(f"Session not found: {session_id}, creating new one")
            self.start_conversation(session_id)

        message = {
            'text': text,
            'speaker': speaker,
            'timestamp': datetime.now().isoformat()
        }

        self.conversations[session_id]['messages'].append(message)
        self.conversations[session_id]['last_updated'] = datetime.now().isoformat()

        logger.debug(f"Added message to session {session_id}: {speaker}: {text[:50]}...")

    def get_context(self, session_id, max_messages=15):
        """
        Get conversation context for AI analysis

        Args:
            session_id: Session ID
            max_messages: Maximum number of recent messages to include

        Returns:
            list: Recent conversation messages
        """
        if session_id not in self.conversations:
            logger.warning(f"Session not found: {session_id}")
            return []

        messages = self.conversations[session_id]['messages']

        # Return last N messages
        return messages[-max_messages:] if messages else []

    def get_full_conversation(self, session_id):
        """
        Get full conversation history

        Args:
            session_id: Session ID

        Returns:
            dict: Full conversation data
        """
        return self.conversations.get(session_id, {})

    def end_conversation(self, session_id):
        """
        Mark conversation as ended (but keep in memory for saving)

        Args:
            session_id: Session ID
        """
        if session_id in self.conversations:
            self.conversations[session_id]['end_time'] = datetime.now().isoformat()
            logger.info(f"Conversation ended: {session_id}")

    def clear_conversation(self, session_id):
        """
        Remove conversation from memory

        Args:
            session_id: Session ID
        """
        if session_id in self.conversations:
            del self.conversations[session_id]
            logger.info(f"Conversation cleared: {session_id}")

    def get_active_sessions(self):
        """
        Get list of active session IDs

        Returns:
            list: Active session IDs
        """
        return list(self.conversations.keys())

    def get_message_count(self, session_id):
        """
        Get number of messages in a session

        Args:
            session_id: Session ID

        Returns:
            int: Message count
        """
        if session_id not in self.conversations:
            return 0

        return len(self.conversations[session_id]['messages'])
