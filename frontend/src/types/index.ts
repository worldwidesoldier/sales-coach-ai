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
  suggestions: Suggestion[];
  audioLevel: number;
  isMuted: boolean;
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
