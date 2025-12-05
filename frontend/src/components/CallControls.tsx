import { Button } from '@/components/ui/button';
import { Phone, PhoneOff, Mic, MicOff, Save } from 'lucide-react';

interface CallControlsProps {
  isActive: boolean;
  isMuted: boolean;
  isRecording: boolean;
  onStart: () => void;
  onStop: () => void;
  onToggleMute: () => void;
  disabled?: boolean;
}

export const CallControls = ({
  isActive,
  isMuted,
  isRecording,
  onStart,
  onStop,
  onToggleMute,
  disabled = false,
}: CallControlsProps) => {
  return (
    <div className="flex items-center justify-center gap-4 p-6 border-t bg-muted/30">
      {!isActive ? (
        <Button
          onClick={onStart}
          disabled={disabled}
          size="lg"
          className="bg-green-600 hover:bg-green-700 text-white gap-2"
        >
          <Phone className="h-5 w-5" />
          Start Call
        </Button>
      ) : (
        <>
          <Button
            onClick={onToggleMute}
            variant={isMuted ? "destructive" : "secondary"}
            size="lg"
            className="gap-2"
          >
            {isMuted ? (
              <>
                <MicOff className="h-5 w-5" />
                Unmute
              </>
            ) : (
              <>
                <Mic className="h-5 w-5" />
                Mute
              </>
            )}
          </Button>

          <Button
            onClick={onStop}
            variant="destructive"
            size="lg"
            className="gap-2"
          >
            <PhoneOff className="h-5 w-5" />
            End Call
          </Button>
        </>
      )}
    </div>
  );
};
