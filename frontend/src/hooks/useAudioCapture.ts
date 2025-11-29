import { useState, useRef, useCallback, useEffect } from 'react';

interface UseAudioCaptureReturn {
  isCapturing: boolean;
  audioLevel: number;
  startCapture: (onAudioData: (base64: string) => void) => Promise<boolean>;
  stopCapture: () => void;
  isMuted: boolean;
  toggleMute: () => void;
  error: string | null;
}

export const useAudioCapture = (): UseAudioCaptureReturn => {
  const [isCapturing, setIsCapturing] = useState(false);
  const [audioLevel, setAudioLevel] = useState(0);
  const [isMuted, setIsMuted] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const mediaStreamRef = useRef<MediaStream | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const animationFrameRef = useRef<number | null>(null);
  const isMutedRef = useRef<boolean>(false);

  const startCapture = useCallback(async (onAudioData: (base64: string) => void): Promise<boolean> => {
    try {
      setError(null);

      // Request microphone access
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
        },
      });

      mediaStreamRef.current = stream;

      // Create audio context
      const audioContext = new AudioContext({ sampleRate: 16000 });
      audioContextRef.current = audioContext;

      const source = audioContext.createMediaStreamSource(stream);

      // Create analyser for audio level visualization
      const analyser = audioContext.createAnalyser();
      analyser.fftSize = 256;
      analyserRef.current = analyser;
      source.connect(analyser);

      // Use MediaRecorder for audio capture (modern API)
      // Try different codecs - Safari/Chrome compatibility
      let options: MediaRecorderOptions;
      if (MediaRecorder.isTypeSupported('audio/webm;codecs=opus')) {
        options = { mimeType: 'audio/webm;codecs=opus' };
        console.log('✅ Using audio/webm;codecs=opus');
      } else if (MediaRecorder.isTypeSupported('audio/webm')) {
        options = { mimeType: 'audio/webm' };
        console.log('✅ Using audio/webm');
      } else if (MediaRecorder.isTypeSupported('audio/ogg;codecs=opus')) {
        options = { mimeType: 'audio/ogg;codecs=opus' };
        console.log('✅ Using audio/ogg;codecs=opus');
      } else {
        options = {};
        console.log('✅ Using default MediaRecorder format');
      }

      const mediaRecorder = new MediaRecorder(stream, options);
      mediaRecorderRef.current = mediaRecorder;

      let audioChunkCount = 0;

      mediaRecorder.onerror = (event) => {
        console.error('❌ MediaRecorder error:', event);
        setError('MediaRecorder error occurred');
      };

      mediaRecorder.onstart = () => {
        console.log('✅ MediaRecorder started');
      };

      mediaRecorder.ondataavailable = async (event) => {
        console.log(`📦 Data available: ${event.data.size} bytes, muted: ${isMutedRef.current}`);

        if (event.data.size > 0 && !isMutedRef.current) {
          // Convert Blob to base64
          const reader = new FileReader();
          reader.onloadend = () => {
            const base64 = reader.result as string;
            // Remove data URL prefix
            const base64Audio = base64.split(',')[1];

            audioChunkCount++;
            if (audioChunkCount % 10 === 0) {
              console.log(`🎤 Sent ${audioChunkCount} audio chunks`);
            }

            onAudioData(base64Audio);
          };
          reader.readAsDataURL(event.data);
        }
      };

      // Start recording with 100ms chunks
      console.log('🎙️ Starting MediaRecorder with 100ms chunks...');
      mediaRecorder.start(100);

      // Start audio level monitoring
      const updateAudioLevel = () => {
        if (!analyserRef.current) return;

        const dataArray = new Uint8Array(analyserRef.current.frequencyBinCount);
        analyserRef.current.getByteFrequencyData(dataArray);

        const average = dataArray.reduce((a, b) => a + b) / dataArray.length;
        setAudioLevel(average / 255); // Normalize to 0-1

        animationFrameRef.current = requestAnimationFrame(updateAudioLevel);
      };

      updateAudioLevel();

      setIsCapturing(true);
      console.log('✅ Audio capture started');

      return true;
    } catch (err) {
      console.error('Error starting audio capture:', err);
      setError(err instanceof Error ? err.message : 'Failed to access microphone');
      return false;
    }
  }, [isMuted]);

  const stopCapture = useCallback(() => {
    // Stop animation frame
    if (animationFrameRef.current) {
      cancelAnimationFrame(animationFrameRef.current);
      animationFrameRef.current = null;
    }

    // Stop media recorder
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current = null;
    }

    // Stop analyser
    if (analyserRef.current) {
      analyserRef.current.disconnect();
      analyserRef.current = null;
    }

    // Close audio context
    if (audioContextRef.current) {
      audioContextRef.current.close();
      audioContextRef.current = null;
    }

    // Stop media stream
    if (mediaStreamRef.current) {
      mediaStreamRef.current.getTracks().forEach(track => track.stop());
      mediaStreamRef.current = null;
    }

    setIsCapturing(false);
    setAudioLevel(0);
    console.log('✅ Audio capture stopped');
  }, []);

  const toggleMute = useCallback(() => {
    setIsMuted(prev => {
      const newValue = !prev;
      isMutedRef.current = newValue;
      return newValue;
    });
  }, []);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      stopCapture();
    };
  }, [stopCapture]);

  return {
    isCapturing,
    audioLevel,
    startCapture,
    stopCapture,
    isMuted,
    toggleMute,
    error,
  };
};
