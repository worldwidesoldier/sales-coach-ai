export interface Transcription {
  id?: string;
  text: string;
  speaker: 'customer' | 'salesperson' | 'unknown' | string;
  timestamp: number;
  is_final: boolean;
  confidence?: number;
}

// Legacy suggestion format (for backwards compatibility)
export interface LegacySuggestion {
  objection_detected: boolean;
  objection_type: 'price' | 'timing' | 'authority' | 'need' | 'trust' | 'technical' | 'none';
  buying_signal: boolean;
  suggestion: string;
  strategy: string;
  confidence: number;
  sentiment: 'positive' | 'neutral' | 'negative';
}

// New suggestion format matches CoachingSuggestion
export type Suggestion = CoachingSuggestion;

export interface CallState {
  isActive: boolean;
  sessionId: string | null;
  transcriptions: Transcription[];
  suggestions: Suggestion[];  // Legacy
  coachingGuidance: CoachingGuidance;  // Always has value (no null)
  audioLevel: number;
  isMuted: boolean;
  featureFlags: FeatureFlags;  // NEW
}

export interface SavedCall {
  id: string;
  start_time: string;
  end_time?: string;
  transcript_count: number;
  suggestion_count: number;
}

export interface ConnectionStatus {
  connected: boolean;
  connecting: boolean;
  error: string | null;
}

export interface PrimarySuggestion {
  text: string;
  reasoning: string;
  confidence: number;
  urgency: 'low' | 'medium' | 'high' | 'critical';
}

export interface SuggestionContext {
  call_stage: 'opening' | 'discovery' | 'pitch' | 'objection' | 'close';
  objection_detected: boolean;
  objection_type: 'price' | 'timing' | 'authority' | 'need' | 'trust' | 'technical' | 'none';
  buying_signal: boolean;
  sentiment: 'positive' | 'neutral' | 'negative';
}

export interface CoachingSuggestion {
  primary_suggestion: PrimarySuggestion;
  context: SuggestionContext;
  highlight_toolkit: string[];
  next_move: string;
}

export interface ToolkitScript {
  name: string;
  text: string;
  when_to_use: string;
}

export interface ToolkitCategory {
  title: string;
  scripts: ToolkitScript[];
}

export interface MissedOpportunity {
  timestamp: string;
  opportunity: string;
  what_to_do: string;
}

export interface CallAnalysis {
  what_worked: string[];
  missed_opportunities: MissedOpportunity[];
  improvement_tips: string[];
  success_score: number;
  call_outcome: 'positive' | 'neutral' | 'negative';
  key_insights: string;
}

// Coaching Guidance Types
export interface CallStage {
  current: 'opening' | 'discovery' | 'pitch' | 'objection' | 'close';
  confidence: number;
  time_in_stage: number;
}

export interface StageFocus {
  what: string;
  why: string;
  urgency: 'low' | 'medium' | 'high' | 'critical';
}

export interface Objective {
  id: string;
  text: string;
  priority?: 'low' | 'medium' | 'high';
  completed_at?: number;
}

export interface Objectives {
  completed: Objective[];
  remaining: Objective[];
}

export interface GuidanceQuestion {
  primary: string;
  alternatives?: string[];
  context?: string;  // When to use this approach
}

export interface Guidance {
  direction: string;
  key_questions: (string | GuidanceQuestion)[];  // Support both formats for backward compatibility
  talking_points: string[];
  confidence: number;
}

export interface CoachingGuidance {
  type: 'coaching_guidance';
  stage: CallStage;
  focus: StageFocus;
  objectives: Objectives;
  guidance: Guidance;
  metadata: {
    timestamp: number;
    session_id: string;
    model_version: string;
  };
}

export interface FeatureFlags {
  coaching_mode: 'guidance' | 'suggestions';
  guidance_version: string;
}

// Default coaching guidance for pre-call state
export const DEFAULT_COACHING_GUIDANCE: CoachingGuidance = {
  type: 'coaching_guidance',
  stage: {
    current: 'opening',
    confidence: 0,
    time_in_stage: 0
  },
  focus: {
    what: 'Build rapport and establish credibility',
    why: 'Start the conversation on the right foot',
    urgency: 'low'
  },
  objectives: {
    completed: [],
    remaining: [
      { id: 'rapport', text: 'Build rapport', priority: 'high' },
      { id: 'reason', text: 'Establish reason for call', priority: 'high' },
      { id: 'needs', text: 'Understand their needs', priority: 'medium' }
    ]
  },
  guidance: {
    direction: 'Begin with a warm greeting and establish credibility. Your goal is to make them comfortable and understand what they need.',
    key_questions: [
      {
        primary: 'How are things going with your current situation?',
        alternatives: [
          'What\'s been keeping you busy lately?',
          'How has business been treating you recently?',
          'What\'s top of mind for you right now?',
          'How are things progressing on your end?'
        ],
        context: 'Use for initial rapport building and opening conversation'
      },
      {
        primary: 'What challenges are you facing right now?',
        alternatives: [
          'What obstacles are slowing you down these days?',
          'Where are you hitting roadblocks in your process?',
          'What would make your life easier?',
          'What\'s the biggest pain point you\'re dealing with?'
        ],
        context: 'Use for uncovering needs and pain points'
      },
      {
        primary: 'What would make this call valuable for you?',
        alternatives: [
          'What outcome would you like from our conversation today?',
          'How can I best use your time in our call?',
          'What would success look like for you today?',
          'What do you hope to accomplish in our discussion?'
        ],
        context: 'Use for agenda setting and expectation alignment'
      }
    ],
    talking_points: [
      'Start with rapport building - be warm and genuine',
      'Listen actively and show you understand their situation',
      'Let them do most of the talking (80/20 rule)',
      'Take notes on key phrases they use'
    ],
    confidence: 0
  },
  metadata: {
    timestamp: Date.now(),
    session_id: 'pre-call',
    model_version: 'v1'
  }
};
