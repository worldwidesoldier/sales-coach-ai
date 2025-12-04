import { useEffect, useState, useCallback } from 'react';
import socket from '@/lib/socket';
import { Transcription, Suggestion, ConnectionStatus } from '@/types';

interface UseWebSocketReturn {
  connectionStatus: ConnectionStatus;
  startCall: () => Promise<string>;
  endCall: () => void;
  sendAudio: (audioData: string) => void;
  onTranscription: (callback: (transcript: Transcription) => void) => void;
  onSuggestion: (callback: (suggestion: Suggestion) => void) => void;
  sessionId: string | null;
}

export const useWebSocket = (): UseWebSocketReturn => {
  const [connectionStatus, setConnectionStatus] = useState<ConnectionStatus>({
    connected: false,
    connecting: true,
    error: null,
  });
  const [sessionId, setSessionId] = useState<string | null>(null);

  useEffect(() => {
    // Connection event handlers
    socket.on('connect', () => {
      console.log('✅ Connected to WebSocket');
      setConnectionStatus({
        connected: true,
        connecting: false,
        error: null,
      });
    });

    socket.on('disconnect', () => {
      console.log('❌ Disconnected from WebSocket');
      setConnectionStatus({
        connected: false,
        connecting: false,
        error: 'Disconnected from server',
      });
    });

    socket.on('connect_error', (error) => {
      console.error('WebSocket connection error:', error);
      setConnectionStatus({
        connected: false,
        connecting: false,
        error: error.message,
      });
    });

    socket.on('connection_established', (data) => {
      console.log('Connection established:', data);
    });

    socket.on('call_started', (data) => {
      console.log('Call started:', data);
      setSessionId(data.session_id);
    });

    socket.on('call_ended', (data) => {
      console.log('Call ended:', data);
      setSessionId(null);
    });

    socket.on('error', (error) => {
      console.error('Server error:', error);
    });

    // Cleanup
    return () => {
      socket.off('connect');
      socket.off('disconnect');
      socket.off('connect_error');
      socket.off('connection_established');
      socket.off('call_started');
      socket.off('call_ended');
      socket.off('error');
    };
  }, []);

  const startCall = useCallback(() => {
    console.log('Starting call...');
    return new Promise<string>((resolve, reject) => {
      // Set up one-time listener for call_started
      const onCallStarted = (data: { session_id: string }) => {
        console.log('✅ Call started event received:', data.session_id);
        setSessionId(data.session_id);
        resolve(data.session_id);
      };

      const onError = (error: { message: string }) => {
        console.error('❌ Failed to start call:', error);
        reject(new Error(error.message));
      };

      // Register temporary listeners
      socket.once('call_started', onCallStarted);
      socket.once('error', onError);

      // Emit start_call event
      socket.emit('start_call');

      // Timeout after 5 seconds
      setTimeout(() => {
        socket.off('call_started', onCallStarted);
        socket.off('error', onError);
        reject(new Error('Timeout waiting for call to start'));
      }, 5000);
    });
  }, []);

  const endCall = useCallback(() => {
    console.log('Ending call...');
    socket.emit('end_call');
  }, []);

  const sendAudio = useCallback((audioData: string) => {
    console.log(`📤 Sending audio_stream event (${audioData.length} bytes)`);
    socket.emit('audio_stream', {
      audio: audioData,
      timestamp: Date.now(),
    });
  }, []);

  const onTranscription = useCallback((callback: (transcript: Transcription) => void) => {
    socket.on('transcription', callback);
    return () => {
      socket.off('transcription', callback);
    };
  }, []);

  const onSuggestion = useCallback((callback: (suggestion: Suggestion) => void) => {
    socket.on('suggestion', callback);
    return () => {
      socket.off('suggestion', callback);
    };
  }, []);

  return {
    connectionStatus,
    startCall,
    endCall,
    sendAudio,
    onTranscription,
    onSuggestion,
    sessionId,
  };
};
