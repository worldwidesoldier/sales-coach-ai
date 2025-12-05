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
          <div className="flex items-center gap-4">
            {/* Eternyx AI Logo SVG */}
            <svg
              width="48"
              height="48"
              viewBox="0 0 200 200"
              className="flex-shrink-0"
            >
              <defs>
                <linearGradient id="eternyxGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#00D9FF" />
                  <stop offset="100%" stopColor="#7B3FF2" />
                </linearGradient>
              </defs>
              {/* Spiral */}
              <circle cx="65" cy="100" r="55" fill="none" stroke="url(#eternyxGradient)" strokeWidth="4" opacity="0.3"/>
              <path d="M 65 45 Q 120 45, 120 100 Q 120 155, 65 155 Q 10 155, 10 100 Q 10 55, 50 50" fill="none" stroke="url(#eternyxGradient)" strokeWidth="5" strokeLinecap="round"/>
              <circle cx="50" cy="50" r="8" fill="#7B3FF2"/>
              {/* AI Text */}
              <text x="140" y="120" fontSize="52" fontWeight="bold" fill="#7B3FF2">AI</text>
            </svg>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-xl font-bold bg-gradient-to-r from-cyan-500 to-purple-600 bg-clip-text text-transparent">
                  ETERNYX
                </h1>
                <span className="text-xl font-bold">Sales Coach</span>
              </div>
              <p className="text-sm text-muted-foreground">
                Real-time AI sales coaching
              </p>
            </div>
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
        <div className="h-full container mx-auto px-4 py-6">
          <div className="flex flex-col gap-4">
            {/* Top Section: Transcription + Primary Suggestion - FIXED HEIGHT */}
            <div className="flex gap-4 min-h-[85vh] max-h-[85vh]">
              {/* Left: Live Transcription - Fixed height with internal scroll */}
              <div className="flex-1 min-w-0 h-full flex flex-col">
                <TranscriptionPanel transcriptions={transcriptions} />
              </div>

              {/* Right: Current Suggestion - ALWAYS SHOW BOTH CARDS */}
              <div className="flex-1 min-w-0 h-full flex flex-col">
                <PrimarySuggestionPanel
                  currentSuggestion={suggestions.length > 0 ? suggestions[suggestions.length - 1] : null}
                  previousSuggestion={suggestions.length > 1 ? suggestions[suggestions.length - 2] : null}
                />
              </div>
            </div>

            {/* Bottom Section: Backup Toolkit - Can scroll to see */}
            <div className="mt-4">
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
