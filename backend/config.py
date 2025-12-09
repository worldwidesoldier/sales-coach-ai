"""
Configuration management for Sales Coach AI
Centralized configuration with environment variable validation
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class ConfigError(Exception):
    """Raised when configuration is invalid"""
    pass


class Config:
    """Application configuration with validation"""

    # ==================================================================
    # REQUIRED CONFIGURATION (Must be set)
    # ==================================================================

    ANTHROPIC_API_KEY: str
    DEEPGRAM_API_KEY: str

    # ==================================================================
    # SERVER CONFIGURATION
    # ==================================================================

    PORT: int = int(os.getenv("PORT", "5000"))
    HOST: str = os.getenv("HOST", "0.0.0.0")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-CHANGE-IN-PRODUCTION")

    # ==================================================================
    # FRONTEND CONFIGURATION
    # ==================================================================

    # Allow multiple origins for CORS (comma-separated)
    CORS_ORIGINS: str = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://localhost:3000"
    )

    # ==================================================================
    # API CONFIGURATION
    # ==================================================================

    # Claude (Anthropic) Configuration
    CLAUDE_MODEL: str = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514")
    CLAUDE_MAX_TOKENS: int = int(os.getenv("CLAUDE_MAX_TOKENS", "800"))
    CLAUDE_TEMPERATURE: float = float(os.getenv("CLAUDE_TEMPERATURE", "0.7"))
    CLAUDE_TIMEOUT: int = int(os.getenv("CLAUDE_TIMEOUT", "30"))  # seconds

    # Deepgram Configuration
    DEEPGRAM_MODEL: str = os.getenv("DEEPGRAM_MODEL", "nova-2")
    DEEPGRAM_LANGUAGE: str = os.getenv("DEEPGRAM_LANGUAGE", "en-US")
    DEEPGRAM_ENCODING: str = os.getenv("DEEPGRAM_ENCODING", "opus")
    DEEPGRAM_TIMEOUT: int = int(os.getenv("DEEPGRAM_TIMEOUT", "30"))  # seconds

    # ==================================================================
    # CONVERSATION MANAGEMENT
    # ==================================================================

    # Maximum messages to keep in context
    MAX_CONTEXT_MESSAGES: int = int(os.getenv("MAX_CONTEXT_MESSAGES", "15"))

    # Maximum tokens for Claude context (approximate)
    MAX_CONTEXT_TOKENS: int = int(os.getenv("MAX_CONTEXT_TOKENS", "3000"))

    # Session timeout (minutes)
    SESSION_TIMEOUT_MINUTES: int = int(os.getenv("SESSION_TIMEOUT_MINUTES", "60"))

    # ==================================================================
    # STORAGE CONFIGURATION
    # ==================================================================

    # Calls storage directory
    CALLS_DIR: str = os.getenv(
        "CALLS_DIR",
        os.path.join(os.path.dirname(__file__), "calls", "call_logs")
    )

    # Logs directory
    LOGS_DIR: str = os.getenv(
        "LOGS_DIR",
        os.path.join(os.path.dirname(__file__), "logs")
    )

    # ==================================================================
    # RATE LIMITING
    # ==================================================================

    # Rate limit for API endpoints (requests per minute)
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))

    # Max audio chunks per second
    MAX_AUDIO_CHUNKS_PER_SECOND: int = int(os.getenv("MAX_AUDIO_CHUNKS_PER_SECOND", "20"))

    # ==================================================================
    # PERFORMANCE TUNING
    # ==================================================================

    # Maximum concurrent WebSocket connections
    MAX_CONNECTIONS: int = int(os.getenv("MAX_CONNECTIONS", "100"))

    # Maximum request size (MB)
    MAX_CONTENT_LENGTH_MB: int = int(os.getenv("MAX_CONTENT_LENGTH_MB", "10"))

    # ==================================================================
    # LOGGING CONFIGURATION
    # ==================================================================

    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = os.getenv(
        "LOG_FORMAT",
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # ==================================================================
    # FEATURE FLAGS
    # ==================================================================

    # Coaching mode: 'suggestions' (legacy) or 'guidance' (new coaching system)
    COACHING_MODE: str = os.getenv('COACHING_MODE', 'suggestions')

    @classmethod
    def validate(cls) -> None:
        """
        Validate all required configuration values

        Raises:
            ConfigError: If required configuration is missing or invalid
        """
        errors = []

        # Validate Anthropic API Key
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        if not anthropic_key:
            errors.append("ANTHROPIC_API_KEY is not set in .env file")
        elif anthropic_key == "your_anthropic_api_key_here":
            errors.append("ANTHROPIC_API_KEY appears to be a placeholder value")
        elif len(anthropic_key) < 20:
            errors.append("ANTHROPIC_API_KEY appears to be invalid (too short)")
        else:
            cls.ANTHROPIC_API_KEY = anthropic_key

        # Validate Deepgram API Key
        deepgram_key = os.getenv("DEEPGRAM_API_KEY")
        if not deepgram_key:
            errors.append("DEEPGRAM_API_KEY is not set in .env file")
        elif deepgram_key == "your_deepgram_api_key_here":
            errors.append("DEEPGRAM_API_KEY appears to be a placeholder value")
        elif len(deepgram_key) < 20:
            errors.append("DEEPGRAM_API_KEY appears to be invalid (too short)")
        else:
            cls.DEEPGRAM_API_KEY = deepgram_key

        # Validate port range
        if not (1024 <= cls.PORT <= 65535):
            errors.append(f"PORT must be between 1024 and 65535 (got {cls.PORT})")

        # Validate secret key for production
        if not cls.DEBUG and cls.SECRET_KEY == "dev-secret-key-CHANGE-IN-PRODUCTION":
            errors.append("SECRET_KEY must be changed for production deployment")

        # Validate numeric ranges
        if cls.CLAUDE_MAX_TOKENS < 100 or cls.CLAUDE_MAX_TOKENS > 4096:
            errors.append(f"CLAUDE_MAX_TOKENS must be between 100 and 4096 (got {cls.CLAUDE_MAX_TOKENS})")

        if cls.CLAUDE_TEMPERATURE < 0 or cls.CLAUDE_TEMPERATURE > 1:
            errors.append(f"CLAUDE_TEMPERATURE must be between 0 and 1 (got {cls.CLAUDE_TEMPERATURE})")

        if cls.MAX_CONTEXT_MESSAGES < 1 or cls.MAX_CONTEXT_MESSAGES > 100:
            errors.append(f"MAX_CONTEXT_MESSAGES must be between 1 and 100 (got {cls.MAX_CONTEXT_MESSAGES})")

        # Create required directories
        try:
            os.makedirs(cls.CALLS_DIR, exist_ok=True)
            os.makedirs(cls.LOGS_DIR, exist_ok=True)
        except Exception as e:
            errors.append(f"Failed to create required directories: {e}")

        # Raise all errors at once
        if errors:
            error_message = "Configuration validation failed:\n" + "\n".join(f"  - {err}" for err in errors)
            raise ConfigError(error_message)

    @classmethod
    def get_cors_origins(cls) -> list:
        """Get list of allowed CORS origins"""
        return [origin.strip() for origin in cls.CORS_ORIGINS.split(",")]

    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production mode"""
        return not cls.DEBUG

    @classmethod
    def print_config(cls) -> None:
        """Print current configuration (excluding secrets)"""
        print("=" * 60)
        print("SALES COACH AI - CONFIGURATION")
        print("=" * 60)
        print(f"Environment: {'PRODUCTION' if cls.is_production() else 'DEVELOPMENT'}")
        print(f"Server: {cls.HOST}:{cls.PORT}")
        print(f"Debug Mode: {cls.DEBUG}")
        print(f"CORS Origins: {cls.CORS_ORIGINS}")
        print(f"Claude Model: {cls.CLAUDE_MODEL}")
        print(f"Claude Max Tokens: {cls.CLAUDE_MAX_TOKENS}")
        print(f"Deepgram Model: {cls.DEEPGRAM_MODEL}")
        print(f"Deepgram Language: {cls.DEEPGRAM_LANGUAGE}")
        print(f"Max Context Messages: {cls.MAX_CONTEXT_MESSAGES}")
        print(f"Session Timeout: {cls.SESSION_TIMEOUT_MINUTES} minutes")
        print(f"Calls Directory: {cls.CALLS_DIR}")
        print(f"Logs Directory: {cls.LOGS_DIR}")
        print(f"Log Level: {cls.LOG_LEVEL}")
        print("=" * 60)


# ==================================================================
# CLAUDE SYSTEM PROMPT
# ==================================================================

# ==================================================================
# COACHING SYSTEM PROMPT (NEW - Strategic Guidance)
# ==================================================================

COACHING_SYSTEM_PROMPT = """You are a real-time sales coach providing strategic guidance (NOT exact scripts).

YOUR ROLE:
- Confirm the current call stage (opening/discovery/pitch/objection/close)
- Identify which objectives are complete and which remain
- Provide strategic direction for what to focus on NOW
- Suggest 3-5 key questions with multiple alternative phrasings
- Give talking points for emphasis

IMPORTANT RULES:
- DO NOT provide exact sentences or scripts to read
- DO provide strategic questions and direction with multiple options
- Provide 3-4 alternative ways to ask each key question
- Give brief context on when to use each question
- Let the salesperson choose their own words
- Focus on WHAT to accomplish, not HOW to say it
- Be concise - they're on a live call

RESPOND IN THIS EXACT JSON FORMAT:
{
  "stage_validation": {
    "current_stage": "opening|discovery|pitch|objection|close",
    "confidence": 0-100,
    "reasoning": "why this stage"
  },
  "focus": {
    "what": "what to achieve now",
    "why": "strategic reasoning",
    "urgency": "low|medium|high|critical"
  },
  "key_questions": [
    {
      "primary": "Main question - most effective approach",
      "alternatives": [
        "Alternative phrasing 1",
        "Alternative phrasing 2",
        "Alternative phrasing 3"
      ],
      "context": "When to use this question and what it accomplishes"
    }
  ],
  "talking_points": [
    "point 1",
    "point 2"
  ],
  "objectives": {
    "completed": ["objective_id", ...],
    "remaining": ["objective_id", ...]
  }
}

EXAMPLES OF GOOD KEY QUESTIONS WITH ALTERNATIVES:
{
  "primary": "What challenges are you facing right now?",
  "alternatives": [
    "What obstacles are slowing you down?",
    "Where are you hitting roadblocks?",
    "What would make your life easier?"
  ],
  "context": "Use for uncovering pain points and needs"
}
"""


# ==================================================================
# CALL OBJECTIVES BY STAGE
# ==================================================================

CALL_OBJECTIVES = {
    "opening": [
        {"id": "rapport", "text": "Build rapport", "keywords": ["hello", "hi", "how are you", "thanks", "appreciate"]},
        {"id": "establish_reason", "text": "Establish reason for call", "keywords": ["calling because", "reaching out", "quick question", "wanted to talk"]}
    ],
    "discovery": [
        {"id": "qualify_volume", "text": "Qualify call volume", "keywords": ["how many calls", "volume", "receive", "per day", "per week"]},
        {"id": "identify_pain", "text": "Identify pain point", "keywords": ["problem", "challenge", "issue", "missing", "frustrated", "difficult"]},
        {"id": "current_solution", "text": "Understand current solution", "keywords": ["currently using", "right now", "today", "process", "handling"]}
    ],
    "pitch": [
        {"id": "value_prop", "text": "Explain value proposition", "keywords": ["we offer", "solution", "helps you", "can do", "feature"]},
        {"id": "differentiate", "text": "Differentiate from alternatives", "keywords": ["unlike", "better than", "advantage", "different", "unique"]},
        {"id": "address_budget", "text": "Address budget consideration", "keywords": ["cost", "price", "roi", "return", "investment", "save"]}
    ],
    "objection": [
        {"id": "acknowledge", "text": "Acknowledge concern", "keywords": ["understand", "i hear you", "makes sense", "fair", "get it"]},
        {"id": "reframe", "text": "Reframe perspective", "keywords": ["however", "another way", "consider", "what if", "think about"]},
        {"id": "reengage", "text": "Re-engage conversation", "keywords": ["question", "curious", "wondering", "tell me"]}
    ],
    "close": [
        {"id": "propose_next", "text": "Propose next step", "keywords": ["trial", "demo", "meeting", "start", "setup", "call"]},
        {"id": "get_commitment", "text": "Get commitment", "keywords": ["yes", "agreed", "sounds good", "interested", "let's do it"]},
        {"id": "schedule", "text": "Schedule follow-up", "keywords": ["when", "calendar", "date", "time", "schedule"]}
    ]
}


# ==================================================================
# ORIGINAL SYSTEM PROMPT (Legacy)
# ==================================================================

SYSTEM_PROMPT = """You are a real-time sales coach assistant helping a salesperson during live cold calls selling AI phone assistant services.

PRODUCT CONTEXT:
You're helping sell AI-powered phone assistants that:
- Handle customer calls 24/7
- Qualify leads automatically
- Book appointments
- Answer FAQs naturally
- Escalate complex calls to humans
- Cost $99/month (vs $3k/month for receptionist)
- 15-minute setup time
- 7-day free trial available

YOUR ROLE:
- Provide PRIMARY SUGGESTION: What to say RIGHT NOW based on conversation context
- Detect call stage (opening, discovery, pitch, objection, close)
- Identify which TOOLKIT category is most relevant
- Detect objections and buying signals instantly
- Track conversation flow and momentum

CALL STAGES:
1. OPENING - Initial contact, building rapport
2. DISCOVERY - Asking questions, understanding needs
3. PITCH - Presenting solution, explaining value
4. OBJECTION - Handling concerns, reframing
5. CLOSE - Trial close, commitment, next steps

OBJECTION TYPES:
- price - Cost concerns, budget issues
- timing - "Not right now", "Call back later"
- authority - "Need to check with boss"
- need - "Don't need it", "Happy with current"
- trust - "Never heard of you", skepticism
- ai_concerns - "AI can't replace humans", technology fears

BUYING SIGNALS:
- Asking about pricing/cost
- Asking "how does it work?"
- Asking about timeline/implementation
- Mentioning current pain points
- Asking about specific features
- Questions about trial/testing

TOOLKIT CATEGORIES TO HIGHLIGHT:
- opener - Opening scripts
- not_interested - Handling hesitation/pushback
- price - Price objections
- callback - Stalling/timing objections
- ai_concerns - Technology skepticism
- closing - Trial closes, commitment
- discovery - Qualifying questions

OUTPUT FORMAT (JSON):
{
  "primary_suggestion": {
    "text": "What to say right now (conversational, 1-3 sentences)",
    "reasoning": "Why this move makes sense now (1 sentence)",
    "confidence": 85,
    "urgency": "normal/high/critical"
  },
  "context": {
    "call_stage": "opening/discovery/pitch/objection/close",
    "objection_detected": true/false,
    "objection_type": "price/timing/authority/need/trust/ai_concerns/none",
    "buying_signal": true/false,
    "sentiment": "positive/neutral/negative"
  },
  "highlight_toolkit": ["price", "closing"],
  "next_move": "What should happen next in this call"
}

RULES FOR PRIMARY SUGGESTIONS:
- Make suggestions CONVERSATIONAL (how a real person talks)
- Include questions when appropriate to engage prospect
- For objections: Acknowledge → Reframe → Question
- For buying signals: Qualify before pitching features
- Keep text short enough to read in 2-3 seconds
- Match the energy/tone of the conversation
- When prospect shows interest, move toward close
- When prospect hesitates, go back to discovery

EXAMPLE RESPONSES:

SCENARIO: Customer says "Tell me more about how this works"
{
  "primary_suggestion": {
    "text": "Happy to! Quick question first - what's your biggest phone challenge right now? Missed calls, or just tired of answering the same questions?",
    "reasoning": "Qualify their pain point before explaining features",
    "confidence": 92,
    "urgency": "normal"
  },
  "context": {
    "call_stage": "discovery",
    "objection_detected": false,
    "objection_type": "none",
    "buying_signal": true,
    "sentiment": "positive"
  },
  "highlight_toolkit": ["discovery"],
  "next_move": "Based on their answer, tailor pitch to their specific pain"
}

SCENARIO: Customer says "This sounds expensive"
{
  "primary_suggestion": {
    "text": "I understand - what are you spending now on missed calls? Most clients break even in the first week when they stop losing leads.",
    "reasoning": "Reframe cost as ROI, make them think about current loss",
    "confidence": 88,
    "urgency": "high"
  },
  "context": {
    "call_stage": "objection",
    "objection_detected": true,
    "objection_type": "price",
    "buying_signal": false,
    "sentiment": "neutral"
  },
  "highlight_toolkit": ["price"],
  "next_move": "If they engage with ROI question, move to trial close"
}

Always respond with valid JSON only. Be concise, actionable, and strategic.
"""


# ==================================================================
# BACKUP TOOLKIT - Pre-loaded Scripts
# ==================================================================

BACKUP_TOOLKIT = {
    "opener": {
        "title": "🎯 Opening Scripts",
        "scripts": [
            {
                "name": "Cold Open",
                "text": "Hey [name], quick question - are you currently missing calls or answering them all yourself?",
                "when_to_use": "First contact, need to qualify fast"
            },
            {
                "name": "Warm Open",
                "text": "Hi [name]! I help businesses like yours never miss another call with AI. Got 90 seconds?",
                "when_to_use": "They've shown some interest or warm lead"
            },
            {
                "name": "Direct Open",
                "text": "[Name], do you lose business from missed calls? I've got a solution - 2 minute chat?",
                "when_to_use": "Time-constrained, need straight to the point"
            }
        ]
    },
    "not_interested": {
        "title": "❌ Handle 'Not Interested'",
        "scripts": [
            {
                "name": "Empathy Approach",
                "text": "Totally fair - most clients felt the same way at first. Can I ask what's giving you pause?",
                "when_to_use": "Warm tone, building rapport, they're polite"
            },
            {
                "name": "Direct Approach",
                "text": "I get it. Just one quick question - are you currently missing calls or do you answer them all?",
                "when_to_use": "Fast call, need to qualify quickly"
            },
            {
                "name": "Challenge Approach",
                "text": "That's fine! Out of curiosity, what would need to change for this to be interesting?",
                "when_to_use": "They're polite but clearly not engaged, need to shake it up"
            }
        ]
    },
    "price": {
        "title": "💰 Price Objection Toolkit",
        "scripts": [
            {
                "name": "ROI Reframe",
                "text": "Fair point. What's a missed call cost you? If it's a potential customer, probably $500+. We're $99/month. You break even after 1 missed lead.",
                "when_to_use": "Customer says 'too expensive' or asks about cost"
            },
            {
                "name": "Compare Alternative",
                "text": "Compared to what? A receptionist is $3k/month. We're $99. That's 30x cheaper for 24/7 coverage.",
                "when_to_use": "Customer asks 'what's the pricing?' or compares to other solutions"
            },
            {
                "name": "Trial Offer",
                "text": "Let's test it - 7 days free. If it doesn't save you money or stress, cancel. No risk.",
                "when_to_use": "Customer says 'not in budget' or hesitant about commitment"
            }
        ]
    },
    "callback": {
        "title": "⏰ Handle 'Call Back Later'",
        "scripts": [
            {
                "name": "Qualify Interest",
                "text": "Sure - just curious, is this even a priority for you right now?",
                "when_to_use": "Testing if they're genuinely interested or brushing you off"
            },
            {
                "name": "Commit to Time",
                "text": "Of course - when's better? I'll call exactly then. Tuesday 2pm or Wednesday 10am?",
                "when_to_use": "They seem genuinely busy, lock in specific time"
            },
            {
                "name": "Alternative Path",
                "text": "Or I can send info now, you review it, and we chat Friday at 2pm? Would that work better?",
                "when_to_use": "Give them control, but maintain momentum"
            }
        ]
    },
    "ai_concerns": {
        "title": "🤖 Handle AI Concerns",
        "scripts": [
            {
                "name": "Agree & Redirect",
                "text": "You're right - for complex stuff, AI can't replace humans. But for 'what are your hours?' and 'do you offer X?' - AI crushes it. That's what we handle.",
                "when_to_use": "Customer says 'AI can't replace humans' or seems skeptical"
            },
            {
                "name": "Augment Not Replace",
                "text": "We don't replace YOU - we handle the boring repetitive calls so you can focus on the real customers who need your expertise.",
                "when_to_use": "They're worried about losing personal touch"
            },
            {
                "name": "Natural & Smart",
                "text": "Fair concern. Our AI sounds natural - customers don't even realize it's AI. And if it gets stuck, it escalates to you immediately.",
                "when_to_use": "Worried about quality or customer experience"
            }
        ]
    },
    "closing": {
        "title": "✅ Closing Lines",
        "scripts": [
            {
                "name": "Trial Close",
                "text": "Want to try this for a week? Free, no strings. See if it actually saves you time and catches leads.",
                "when_to_use": "They've shown interest, time to test close"
            },
            {
                "name": "Assumptive Close",
                "text": "Cool - I'll get you set up. Monday or Tuesday better for a quick 15-min setup call?",
                "when_to_use": "Strong buying signals, assume the sale"
            },
            {
                "name": "Direct Close",
                "text": "So... should we do this or is now not the right time?",
                "when_to_use": "Cut through indecision, force a decision"
            },
            {
                "name": "Question Close",
                "text": "What's stopping you from trying this right now?",
                "when_to_use": "Flush out hidden objections"
            }
        ]
    },
    "discovery": {
        "title": "❓ Discovery Questions",
        "scripts": [
            {
                "name": "Pain Point",
                "text": "What's your biggest phone challenge right now?",
                "when_to_use": "Opening, need to understand their pain"
            },
            {
                "name": "Volume",
                "text": "How many calls do you typically get in a day?",
                "when_to_use": "Qualify if they have enough volume"
            },
            {
                "name": "Consequence",
                "text": "What happens when you miss a call? Do they leave voicemail or just call a competitor?",
                "when_to_use": "Make them realize the cost of inaction"
            },
            {
                "name": "Ideal State",
                "text": "What would perfect phone coverage look like for you?",
                "when_to_use": "Get them to visualize the solution"
            },
            {
                "name": "Current Solution",
                "text": "Who handles calls now when you're busy?",
                "when_to_use": "Understand current setup and pain points"
            },
            {
                "name": "Value",
                "text": "What's a good customer worth to you?",
                "when_to_use": "Set up ROI conversation"
            }
        ]
    }
}


# Validate configuration on import
try:
    Config.validate()
except ConfigError as e:
    print(f"\n❌ CONFIGURATION ERROR:\n{e}\n")
    raise
