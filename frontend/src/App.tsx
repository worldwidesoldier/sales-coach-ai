import { useEffect } from 'react';
import { useWebSocket } from '@/hooks/useWebSocket';
import { useAudioCapture } from '@/hooks/useAudioCapture';
import { useCallState } from '@/hooks/useCallState';
import { StatusIndicator } from '@/components/StatusIndicator';
import { CallControls } from '@/components/CallControls';
import { TranscriptionPanel } from '@/components/TranscriptionPanel';
import { PrimarySuggestionPanel } from '@/components/PrimarySuggestionPanel';
import { BackupToolkit } from '@/components/BackupToolkit';

function App() {
  const {
    connectionStatus,
    startCall: wsStartCall,
    endCall: wsEndCall,
    sendAudio,
    onTranscription,
    onSuggestion,
  } = useWebSocket();

  const {
    isCapturing,
    audioLevel,
    startCapture,
    stopCapture,
    isMuted,
    toggleMute: audioToggleMute,
    error: audioError,
  } = useAudioCapture();

  const {
    isActive,
    transcriptions,
    suggestions,
    addTranscription,
    addSuggestion,
    startCall: stateStartCall,
    endCall: stateEndCall,
    setAudioLevel,
    toggleMute: stateToggleMute,
  } = useCallState();

  // Listen for transcriptions and suggestions
  useEffect(() => {
    const cleanupTranscript = onTranscription((transcript) => {
      addTranscription(transcript);
    });

    const cleanupSuggestion = onSuggestion((suggestion) => {
      addSuggestion(suggestion);
    });

    return () => {
      cleanupTranscript();
      cleanupSuggestion();
    };
  }, [onTranscription, onSuggestion, addTranscription, addSuggestion]);

  // Update audio level in state
  useEffect(() => {
    setAudioLevel(audioLevel);
  }, [audioLevel, setAudioLevel]);

  const handleStartCall = async () => {
    try {
      console.log('🚀 Starting call...');

      // Start WebSocket call and WAIT for call_started event
      const sessionId = await wsStartCall();
      console.log(`✅ Session created: ${sessionId}`);

      // Update local state
      stateStartCall();

      // NOW start audio capture (session is ready!)
      const success = await startCapture((audioData) => {
        // Send audio to backend
        sendAudio(audioData);
      });

      if (!success) {
        console.error('❌ Failed to start audio capture');
        handleEndCall();
      }
    } catch (error) {
      console.error('❌ Failed to start call:', error);
      alert(`Failed to start call: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  };

  const handleEndCall = () => {
    // Stop audio capture
    stopCapture();

    // End WebSocket call
    wsEndCall();

    // Update state
    stateEndCall();
  };

  const handleToggleMute = () => {
    audioToggleMute();
    stateToggleMute();
  };

  return (
    <div className="h-screen flex flex-col bg-background">
      {/* Header */}
      <header className="border-b">
        <div className="container mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold">Sales Coach AI</h1>
          <p className="text-sm text-muted-foreground">
            Real-time sales coaching assistant
          </p>
        </div>
      </header>

      {/* Status Bar */}
      <StatusIndicator
        connectionStatus={connectionStatus}
        isRecording={isCapturing}
        audioLevel={audioLevel}
        isMuted={isMuted}
      />

      {/* Main Content */}
      <main className="flex-1 overflow-hidden">
        <div className="h-full container mx-auto px-4 py-6">
          <div className="h-full flex flex-col gap-4">
            {/* Top Section: Transcription + Primary Suggestion (70% height) */}
            <div className="flex gap-4 min-h-0" style={{ flex: '0 0 65%' }}>
              {/* Left: Live Transcription */}
              <div className="flex-1 min-w-0">
                <TranscriptionPanel transcriptions={transcriptions} />
              </div>

              {/* Right: Current Suggestion */}
              <div className="flex-1 min-w-0">
                <PrimarySuggestionPanel
                  suggestion={suggestions.length > 0 ? suggestions[suggestions.length - 1] : null}
                />
              </div>
            </div>

            {/* Bottom Section: Backup Toolkit (30% height) */}
            <div className="overflow-auto" style={{ flex: '0 0 35%' }}>
              <BackupToolkit
                highlightedCategories={
                  suggestions.length > 0 && suggestions[suggestions.length - 1]?.highlight_toolkit
                    ? suggestions[suggestions.length - 1].highlight_toolkit
                    : []
                }
              />
            </div>
          </div>
        </div>
      </main>

      {/* Controls */}
      <CallControls
        isActive={isActive}
        isMuted={isMuted}
        isRecording={isCapturing}
        onStart={handleStartCall}
        onStop={handleEndCall}
        onToggleMute={handleToggleMute}
        disabled={!connectionStatus.connected}
      />

      {/* Error Display */}
      {audioError && (
        <div className="fixed bottom-24 right-4 bg-destructive text-destructive-foreground px-4 py-2 rounded-lg shadow-lg">
          <p className="text-sm font-medium">Audio Error:</p>
          <p className="text-sm">{audioError}</p>
        </div>
      )}
    </div>
  );
}

export default App;
