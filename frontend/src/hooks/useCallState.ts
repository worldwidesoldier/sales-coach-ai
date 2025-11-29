import { useState, useCallback } from 'react';
import { CallState, Transcription, Suggestion } from '@/types';

interface UseCallStateReturn extends CallState {
  addTranscription: (transcript: Transcription) => void;
  addSuggestion: (suggestion: Suggestion) => void;
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
  audioLevel: 0,
  isMuted: false,
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
    startCall,
    endCall,
    setAudioLevel,
    toggleMute,
    clearState,
  };
};
