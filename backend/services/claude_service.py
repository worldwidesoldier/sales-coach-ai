"""
Claude Service - AI-powered sales coaching suggestions
"""

import json
import logging
from anthropic import Anthropic
from config import SYSTEM_PROMPT

logger = logging.getLogger('sales_coach')


class ClaudeService:
    """Handles AI suggestions via Claude API"""

    def __init__(self, api_key):
        """
        Initialize Claude service

        Args:
            api_key: Anthropic API key
        """
        self.api_key = api_key
        self.client = Anthropic(api_key=api_key)
        self.model = "claude-sonnet-4-20250514"  # Latest Sonnet

        logger.info("✅ Claude service initialized")

    def get_suggestion(self, conversation_context):
        """
        Get AI coaching suggestion based on conversation

        Args:
            conversation_context: List of conversation messages

        Returns:
            dict: Primary suggestion with context and toolkit highlights
        """
        try:
            # Build the prompt with conversation history
            conversation_text = self._format_conversation(conversation_context)

            user_prompt = f"""Analyze this sales call conversation and provide coaching:

{conversation_text}

Respond ONLY with valid JSON matching the exact format specified in your system prompt.
Focus on what the salesperson should say RIGHT NOW."""

            # Call Claude API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=800,
                temperature=0.7,
                system=SYSTEM_PROMPT,
                messages=[
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ]
            )

            # Extract response
            response_text = response.content[0].text.strip()

            # Parse JSON
            suggestion = self._parse_response(response_text)

            logger.info(f"✅ Claude suggestion: stage={suggestion.get('context', {}).get('call_stage')}, "
                       f"confidence={suggestion.get('primary_suggestion', {}).get('confidence')}, "
                       f"highlight={suggestion.get('highlight_toolkit')}")

            return suggestion

        except Exception as e:
            logger.error(f"Error getting Claude suggestion: {e}", exc_info=True)
            # Return fallback suggestion
            return self._fallback_suggestion()

    def _format_conversation(self, context):
        """Format conversation history for Claude"""
        if not context:
            return "No conversation yet."

        formatted = []
        for msg in context[-10:]:  # Last 10 messages
            speaker = msg.get('speaker', 'unknown')
            text = msg.get('text', '')
            formatted.append(f"{speaker}: {text}")

        return "\n".join(formatted)

    def _parse_response(self, response_text):
        """Parse Claude's JSON response"""
        try:
            # Find JSON in response (might have markdown code blocks)
            if "```json" in response_text:
                # Extract from code block
                start = response_text.find("```json") + 7
                end = response_text.find("```", start)
                json_str = response_text[start:end].strip()
            elif "```" in response_text:
                # Extract from any code block
                start = response_text.find("```") + 3
                end = response_text.find("```", start)
                json_str = response_text[start:end].strip()
            else:
                json_str = response_text

            # Parse JSON
            suggestion = json.loads(json_str)

            # Validate structure
            if 'primary_suggestion' not in suggestion:
                logger.warning("Missing 'primary_suggestion' in Claude response")
                return self._fallback_suggestion()

            if 'context' not in suggestion:
                logger.warning("Missing 'context' in Claude response")
                return self._fallback_suggestion()

            # Validate primary_suggestion fields
            primary = suggestion['primary_suggestion']
            required_primary = ['text', 'reasoning', 'confidence']
            for field in required_primary:
                if field not in primary:
                    logger.warning(f"Missing field in primary_suggestion: {field}")
                    return self._fallback_suggestion()

            # Ensure highlight_toolkit exists (can be empty)
            if 'highlight_toolkit' not in suggestion:
                suggestion['highlight_toolkit'] = []

            return suggestion

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Claude JSON response: {e}")
            logger.debug(f"Response was: {response_text}")
            return self._fallback_suggestion()

    def _fallback_suggestion(self):
        """Return a fallback suggestion when Claude fails"""
        return {
            "primary_suggestion": {
                "text": "Continue building rapport. Ask them about their current phone challenges.",
                "reasoning": "Default guidance when AI is unavailable",
                "confidence": 50,
                "urgency": "normal"
            },
            "context": {
                "call_stage": "discovery",
                "objection_detected": False,
                "objection_type": "none",
                "buying_signal": False,
                "sentiment": "neutral"
            },
            "highlight_toolkit": ["discovery"],
            "next_move": "Listen and qualify their needs"
        }

    def analyze_call(self, conversation_context, call_duration):
        """
        Generate post-call analysis

        Args:
            conversation_context: Full conversation history
            call_duration: Duration in seconds

        Returns:
            dict: Call analysis with what worked, missed opportunities, improvements
        """
        try:
            conversation_text = self._format_conversation(conversation_context)

            analysis_prompt = f"""Analyze this completed sales call and provide coaching feedback:

CALL DURATION: {call_duration} seconds

CONVERSATION:
{conversation_text}

Provide a post-call analysis in JSON format:
{{
  "what_worked": ["List 2-3 things the salesperson did well"],
  "missed_opportunities": [
    {{
      "timestamp": "approximate time in conversation",
      "opportunity": "what they missed",
      "what_to_do": "what they should have done"
    }}
  ],
  "improvement_tips": ["2-3 actionable tips for next call"],
  "success_score": 0-10,
  "call_outcome": "positive/neutral/negative",
  "key_insights": "1-2 sentence summary of the call"
}}

Be specific, actionable, and constructive."""

            response = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                temperature=0.7,
                messages=[
                    {
                        "role": "user",
                        "content": analysis_prompt
                    }
                ]
            )

            response_text = response.content[0].text.strip()
            analysis = self._parse_analysis(response_text)

            logger.info(f"✅ Call analysis generated: score={analysis.get('success_score')}")
            return analysis

        except Exception as e:
            logger.error(f"Error analyzing call: {e}", exc_info=True)
            return self._fallback_analysis()

    def _parse_analysis(self, response_text):
        """Parse call analysis JSON"""
        try:
            if "```json" in response_text:
                start = response_text.find("```json") + 7
                end = response_text.find("```", start)
                json_str = response_text[start:end].strip()
            elif "```" in response_text:
                start = response_text.find("```") + 3
                end = response_text.find("```", start)
                json_str = response_text[start:end].strip()
            else:
                json_str = response_text

            analysis = json.loads(json_str)

            # Validate required fields
            required = ['what_worked', 'missed_opportunities', 'improvement_tips', 'success_score']
            for field in required:
                if field not in analysis:
                    logger.warning(f"Missing field in analysis: {field}")
                    return self._fallback_analysis()

            return analysis

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse analysis JSON: {e}")
            return self._fallback_analysis()

    def _fallback_analysis(self):
        """Fallback analysis when AI fails"""
        return {
            "what_worked": ["Call was attempted"],
            "missed_opportunities": [],
            "improvement_tips": ["Practice active listening", "Ask more discovery questions"],
            "success_score": 5,
            "call_outcome": "neutral",
            "key_insights": "Analysis unavailable - review transcript manually"
        }

    def is_healthy(self):
        """
        Check if Claude service is healthy

        Returns:
            bool: True if healthy
        """
        try:
            return bool(self.api_key and self.client)
        except Exception:
            return False
