import { useEffect, useState } from 'react';
import { useWebSocket } from '@/hooks/useWebSocket';
import { useAudioCapture } from '@/hooks/useAudioCapture';
import { useCallState } from '@/hooks/useCallState';
import { StatusIndicator } from '@/components/StatusIndicator';
import { CallControls } from '@/components/CallControls';
import { TranscriptionPanel } from '@/components/TranscriptionPanel';
import { PrimarySuggestionPanel } from '@/components/PrimarySuggestionPanel';
import { BackupToolkit } from '@/components/BackupToolkit';
import { Sun, Moon } from 'lucide-react';

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

  // Dark mode theme
  const [theme, setTheme] = useState<'light' | 'dark'>(() => {
    return (localStorage.getItem('theme') as 'light' | 'dark') || 'dark';
  });

  useEffect(() => {
    document.documentElement.classList.toggle('dark', theme === 'dark');
  }, [theme]);

  const toggleTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme);
  };

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
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold">Sales Coach AI</h1>
            <p className="text-sm text-muted-foreground">
              Real-time sales coaching assistant
            </p>
          </div>
          <button
            onClick={toggleTheme}
            className="p-2 rounded-lg hover:bg-accent transition-colors"
            aria-label="Toggle theme"
          >
            {theme === 'dark' ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
          </button>
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
      <main className="flex-1 overflow-auto">
        <div className="container mx-auto px-4 py-6">
          <div className="flex flex-col gap-4">
            {/* Top Section: Transcription + Primary Suggestion (75% height) */}
            <div className="flex gap-4 min-h-0" style={{ flex: '0 0 75%' }}>
              {/* Left: Live Transcription */}
              <div className="flex-1 min-w-0">
                <TranscriptionPanel transcriptions={transcriptions} />
              </div>

              {/* Right: Current Suggestion */}
              <div className="flex-1 min-w-0">
                <PrimarySuggestionPanel
                  currentSuggestion={suggestions.length > 0 ? suggestions[suggestions.length - 1] : null}
                  previousSuggestion={suggestions.length > 1 ? suggestions[suggestions.length - 2] : null}
                />
              </div>
            </div>

            {/* Bottom Section: Backup Toolkit (25% height) */}
            <div style={{ flex: '0 0 25%' }}>
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
