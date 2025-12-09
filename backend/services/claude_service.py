"""
Claude Service - AI-powered sales coaching suggestions
"""

import json
import logging
import time
from anthropic import Anthropic
from config import SYSTEM_PROMPT, COACHING_SYSTEM_PROMPT, CALL_OBJECTIVES, Config

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

    # ==================================================================
    # NEW COACHING GUIDANCE METHODS
    # ==================================================================

    def get_coaching_guidance(self, conversation_context, previous_stage=None):
        """
        Get strategic coaching guidance (not scripts)

        Args:
            conversation_context: List of recent messages
            previous_stage: Previously detected stage (optional)

        Returns:
            CoachingGuidance dict with stage, focus, guidance, objectives
        """
        try:
            # Detect current stage
            detected_stage = self._detect_call_stage(conversation_context, previous_stage)

            # Track objectives
            objectives = self._track_objectives(conversation_context, detected_stage)

            # Format context for Claude
            formatted_context = self._format_conversation_for_coaching(conversation_context)

            # Build prompt
            prompt = f"""CURRENT CONVERSATION:
{formatted_context}

DETECTED STAGE: {detected_stage['stage']}
CONFIDENCE: {detected_stage['confidence']}%

{COACHING_SYSTEM_PROMPT}"""

            # Call Claude API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=800,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Parse JSON response
            response_text = response.content[0].text.strip()
            claude_response = self._parse_coaching_response(response_text)

            # Build coaching guidance
            guidance = {
                "type": "coaching_guidance",
                "stage": {
                    "current": claude_response['stage_validation']['current_stage'],
                    "confidence": claude_response['stage_validation']['confidence'],
                    "time_in_stage": detected_stage.get('time_in_stage', 0)
                },
                "focus": claude_response['focus'],
                "objectives": objectives,
                "guidance": {
                    "direction": f"{claude_response['focus']['what']}. {claude_response['focus']['why']}",
                    "key_questions": claude_response['key_questions'],
                    "talking_points": claude_response['talking_points'],
                    "confidence": claude_response['stage_validation']['confidence']
                },
                "metadata": {
                    "timestamp": int(time.time()),
                    "session_id": "will_be_added_by_app",
                    "model_version": "coaching_v1"
                }
            }

            logger.info(f"✅ Coaching guidance: stage={guidance['stage']['current']}, "
                       f"confidence={guidance['stage']['confidence']}, "
                       f"objectives_remaining={len(objectives['remaining'])}")
            logger.info(f"🔍 DEBUG: key_questions type={type(claude_response['key_questions'])}, "
                       f"count={len(claude_response['key_questions']) if claude_response['key_questions'] else 0}, "
                       f"sample={claude_response['key_questions'][0] if claude_response['key_questions'] else 'EMPTY'}")

            return guidance

        except Exception as e:
            logger.error(f"Error getting coaching guidance: {e}", exc_info=True)
            # Return fallback generic guidance
            return self._get_fallback_guidance(detected_stage['stage'] if 'detected_stage' in locals() else "opening")

    def _detect_call_stage(self, conversation_context, previous_stage=None):
        """
        Detect current call stage using multi-signal algorithm

        Returns dict with stage, confidence, time_in_stage
        """
        if not conversation_context:
            return {"stage": "opening", "confidence": 100, "time_in_stage": 0}

        # Get last 3 messages
        recent_messages = conversation_context[-3:]
        recent_text = " ".join([msg.get('text', '') for msg in recent_messages]).lower()

        # Stage scoring (keyword-based)
        stage_scores = {
            "opening": 0,
            "discovery": 0,
            "pitch": 0,
            "objection": 0,
            "close": 0
        }

        # Keyword analysis (40% weight)
        opening_keywords = ["hello", "hi", "calling from", "quick question", "introduction"]
        discovery_keywords = ["what", "how many", "tell me about", "currently using", "challenge"]
        pitch_keywords = ["we offer", "our solution", "it works by", "helps you", "features"]
        objection_keywords = ["expensive", "not interested", "call back", "no budget", "think about it"]
        close_keywords = ["trial", "demo", "start", "schedule", "meeting", "when can"]

        for keyword in opening_keywords:
            if keyword in recent_text:
                stage_scores["opening"] += 10

        for keyword in discovery_keywords:
            if keyword in recent_text:
                stage_scores["discovery"] += 10

        for keyword in pitch_keywords:
            if keyword in recent_text:
                stage_scores["pitch"] += 10

        for keyword in objection_keywords:
            if keyword in recent_text:
                stage_scores["objection"] += 10

        for keyword in close_keywords:
            if keyword in recent_text:
                stage_scores["close"] += 10

        # Natural progression (30% weight)
        stage_order = ["opening", "discovery", "pitch", "objection", "close"]
        if previous_stage and previous_stage in stage_order:
            current_index = stage_order.index(previous_stage)
            # Boost next stages
            for i in range(current_index, min(current_index + 2, len(stage_order))):
                stage_scores[stage_order[i]] += 15

        # Determine winning stage
        max_score = max(stage_scores.values())
        if max_score == 0:
            # Default to discovery if unclear
            detected_stage = "discovery"
            confidence = 50
        else:
            detected_stage = max(stage_scores, key=stage_scores.get)
            # Confidence = (max_score / possible_max) * 100
            confidence = min(int((max_score / 100) * 100), 100)

        return {
            "stage": detected_stage,
            "confidence": confidence,
            "time_in_stage": 0  # Will be tracked by conversation_manager later
        }

    def _track_objectives(self, conversation_context, detected_stage):
        """
        Track which objectives are completed based on conversation keywords
        """
        stage = detected_stage.get('stage', 'opening')
        objectives_for_stage = CALL_OBJECTIVES.get(stage, [])

        completed = []
        remaining = []

        # Get all conversation text
        all_text = " ".join([msg.get('text', '') for msg in conversation_context]).lower()

        for obj in objectives_for_stage:
            # Check if any keywords present
            has_keywords = any(keyword in all_text for keyword in obj['keywords'])

            if has_keywords:
                completed.append({"id": obj['id'], "text": obj['text']})
            else:
                remaining.append({"id": obj['id'], "text": obj['text'], "priority": "high"})

        return {
            "completed": completed,
            "remaining": remaining
        }

    def _format_conversation_for_coaching(self, context):
        """Format conversation history for coaching prompt"""
        if not context:
            return "No conversation yet."

        formatted = []
        for msg in context[-10:]:  # Last 10 messages
            speaker = msg.get('speaker', 'unknown')
            text = msg.get('text', '')
            formatted.append(f"{speaker}: {text}")

        return "\n".join(formatted)

    def _parse_coaching_response(self, response_text):
        """Parse coaching guidance JSON response"""
        try:
            # Find JSON in response (might have markdown code blocks)
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

            # Parse JSON
            guidance = json.loads(json_str)

            # Validate structure
            required_fields = ['stage_validation', 'focus', 'key_questions', 'talking_points', 'objectives']
            for field in required_fields:
                if field not in guidance:
                    logger.warning(f"Missing field in coaching response: {field}")
                    raise ValueError(f"Missing field: {field}")

            return guidance

        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Failed to parse coaching JSON response: {e}")
            logger.debug(f"Response was: {response_text}")
            raise

    def _get_fallback_guidance(self, stage):
        """Return generic guidance if Claude fails"""
        fallback_map = {
            "opening": {
                "direction": "Build rapport and establish the reason for your call",
                "key_questions": [
                    {
                        "primary": "How are you doing today?",
                        "alternatives": ["How's everything going?", "How's your day treating you?", "Hope you're doing well!"],
                        "context": "Use to open conversation warmly"
                    },
                    {
                        "primary": "Is now a good time to chat for a few minutes?",
                        "alternatives": ["Do you have a quick moment?", "Caught you at a good time?", "Can I steal 2 minutes of your time?"],
                        "context": "Use to respect their time and set expectations"
                    },
                    {
                        "primary": "Have you heard of us before?",
                        "alternatives": ["Are you familiar with our company?", "Has our name come across your desk?", "Know what we do?"],
                        "context": "Use to gauge awareness and adjust approach"
                    }
                ],
                "talking_points": ["Be friendly and professional", "Respect their time"]
            },
            "discovery": {
                "direction": "Understand their current situation and pain points",
                "key_questions": [
                    {
                        "primary": "What's your current process for handling calls?",
                        "alternatives": ["How do you manage incoming calls now?", "Walk me through your call workflow", "What's your setup look like for calls?"],
                        "context": "Use to understand current state"
                    },
                    {
                        "primary": "What challenges are you facing?",
                        "alternatives": ["What's keeping you up at night?", "Where are the bottlenecks?", "What's not working well?"],
                        "context": "Use to uncover pain points"
                    },
                    {
                        "primary": "How many calls do you handle per week?",
                        "alternatives": ["What's your call volume like?", "How busy does it get?", "What kind of numbers are we talking?"],
                        "context": "Use to quantify the problem"
                    }
                ],
                "talking_points": ["Listen actively", "Ask open-ended questions"]
            },
            "pitch": {
                "direction": "Present your solution and connect it to their needs",
                "key_questions": [
                    {
                        "primary": "Would it help if you could capture 90% of missed calls?",
                        "alternatives": ["What if you never missed another call?", "How valuable would recovering lost calls be?", "Imagine not losing customers to voicemail"],
                        "context": "Use to paint the value picture"
                    },
                    {
                        "primary": "What would 10 more customers per month be worth?",
                        "alternatives": ["What's the value of one new customer?", "How much revenue per customer?", "ROI makes sense, right?"],
                        "context": "Use to quantify ROI"
                    },
                    {
                        "primary": "Want to see how it works?",
                        "alternatives": ["Should I show you a quick demo?", "Want to check it out?", "Can I walk you through it?"],
                        "context": "Use to transition to demo"
                    }
                ],
                "talking_points": ["Focus on benefits not features", "Use their language"]
            },
            "objection": {
                "direction": "Acknowledge their concern and reframe the conversation",
                "key_questions": [
                    {
                        "primary": "What's your main concern?",
                        "alternatives": ["What's holding you back?", "What's the sticking point?", "Help me understand your hesitation"],
                        "context": "Use to surface real objection"
                    },
                    {
                        "primary": "Have you thought about the cost of inaction?",
                        "alternatives": ["What's it costing you to wait?", "How much are missed calls costing now?", "What happens if nothing changes?"],
                        "context": "Use to reframe price objections"
                    },
                    {
                        "primary": "What would make this a no-brainer for you?",
                        "alternatives": ["What needs to happen for you to move forward?", "What would remove all doubt?", "What's missing?"],
                        "context": "Use to uncover hidden objections"
                    }
                ],
                "talking_points": ["Stay calm and empathetic", "Don't get defensive"]
            },
            "close": {
                "direction": "Propose a clear next step and get commitment",
                "key_questions": [
                    {
                        "primary": "Want to try it risk-free for 14 days?",
                        "alternatives": ["Should we get you started?", "Ready to test it out?", "Want to give it a shot?"],
                        "context": "Use to propose trial"
                    },
                    {
                        "primary": "When would be a good time to start?",
                        "alternatives": ["Which day works better for you?", "This week or next?", "Sooner or later in the month?"],
                        "context": "Use to create urgency"
                    },
                    {
                        "primary": "Should we schedule a quick demo?",
                        "alternatives": ["Want to see it in action first?", "Let me show you how it works?", "Can I walk you through it?"],
                        "context": "Use to secure next step"
                    }
                ],
                "talking_points": ["Be direct and assumptive", "Create urgency"]
            }
        }

        guidance_content = fallback_map.get(stage, fallback_map["discovery"])

        return {
            "type": "coaching_guidance",
            "stage": {"current": stage, "confidence": 70, "time_in_stage": 0},
            "focus": {"what": guidance_content["direction"], "why": "Generic fallback guidance", "urgency": "medium"},
            "objectives": {"completed": [], "remaining": []},
            "guidance": {
                "direction": guidance_content["direction"],
                "key_questions": guidance_content["key_questions"],
                "talking_points": guidance_content["talking_points"],
                "confidence": 70
            },
            "metadata": {
                "timestamp": int(time.time()),
                "session_id": "",
                "model_version": "fallback_v1"
            }
        }
