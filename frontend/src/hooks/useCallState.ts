import { useState, useCallback } from 'react';
import { CallState, Transcription, Suggestion, CoachingGuidance, FeatureFlags, DEFAULT_COACHING_GUIDANCE } from '@/types';

interface UseCallStateReturn extends CallState {
  addTranscription: (transcript: Transcription) => void;
  addSuggestion: (suggestion: Suggestion) => void;
  addCoachingGuidance: (guidance: CoachingGuidance) => void;
  setFeatureFlags: (flags: FeatureFlags) => void;
  startCall: () => void;
  endCall: () => void;
  setAudioLevel: (level: number) => void;
  toggleMute: () => void;
  clearState: () => void;
}

const initialState: CallState = {
  isActive: false,
  sessionId: null,
  transcriptions: [],
  suggestions: [],
  coachingGuidance: DEFAULT_COACHING_GUIDANCE,  // Show cards immediately
  audioLevel: 0,
  isMuted: false,
  featureFlags: {  // NEW
    coaching_mode: 'suggestions',
    guidance_version: 'v1'
  }
};

export const useCallState = (): UseCallStateReturn => {
  const [state, setState] = useState<CallState>(initialState);

  const addTranscription = useCallback((transcript: Transcription) => {
    setState(prev => ({
      ...prev,
      transcriptions: [...prev.transcriptions, transcript],
    }));
  }, []);

  const addSuggestion = useCallback((suggestion: Suggestion) => {
    setState(prev => ({
      ...prev,
      suggestions: [...prev.suggestions, suggestion],
    }));
  }, []);

  const addCoachingGuidance = useCallback((guidance: CoachingGuidance) => {
    setState(prev => ({
      ...prev,
      coachingGuidance: guidance,
    }));
  }, []);

  const setFeatureFlags = useCallback((flags: FeatureFlags) => {
    setState(prev => ({
      ...prev,
      featureFlags: flags,
    }));
  }, []);

  const startCall = useCallback(() => {
    setState(prev => ({
      ...prev,
      isActive: true,
      transcriptions: [],
      suggestions: [],
    }));
  }, []);

  const endCall = useCallback(() => {
    setState(prev => ({
      ...prev,
      isActive: false,
    }));
  }, []);

  const setAudioLevel = useCallback((level: number) => {
    setState(prev => ({
      ...prev,
      audioLevel: level,
    }));
  }, []);

  const toggleMute = useCallback(() => {
    setState(prev => ({
      ...prev,
      isMuted: !prev.isMuted,
    }));
  }, []);

  const clearState = useCallback(() => {
    setState(initialState);
  }, []);

  return {
    ...state,
    addTranscription,
    addSuggestion,
    addCoachingGuidance,
    setFeatureFlags,
    startCall,
    endCall,
    setAudioLevel,
    toggleMute,
    clearState,
  };
};
