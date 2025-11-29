import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys Configuration (from .env file)
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

# System Configuration
PORT = int(os.getenv("PORT", "5000"))
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")

# Claude System Prompt
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

# Deepgram Configuration
DEEPGRAM_MODEL = "nova-2"
DEEPGRAM_LANGUAGE = "en-US"

# Backup Toolkit - Pre-loaded Scripts
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
