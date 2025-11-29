import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Circle, Mic, MicOff } from 'lucide-react';
import { ConnectionStatus } from '@/types';

interface StatusIndicatorProps {
  connectionStatus: ConnectionStatus;
  isRecording: boolean;
  audioLevel: number;
  isMuted: boolean;
}

export const StatusIndicator = ({
  connectionStatus,
  isRecording,
  audioLevel,
  isMuted,
}: StatusIndicatorProps) => {
  const getConnectionBadge = () => {
    if (connectionStatus.connecting) {
      return (
        <Badge variant="warning" className="gap-1">
          <Circle className="h-2 w-2 fill-current animate-pulse" />
          Connecting...
        </Badge>
      );
    }

    if (connectionStatus.connected) {
      return (
        <Badge variant="success" className="gap-1">
          <Circle className="h-2 w-2 fill-current" />
          Connected
        </Badge>
      );
    }

    return (
      <Badge variant="danger" className="gap-1">
        <Circle className="h-2 w-2 fill-current" />
        Disconnected
        </Badge>
    );
  };

  return (
    <div className="flex items-center gap-4 p-4 border-b bg-muted/30">
      <div className="flex items-center gap-2">
        {getConnectionBadge()}
      </div>

      {isRecording && (
        <>
          <div className="flex items-center gap-2">
            {isMuted ? (
              <MicOff className="h-4 w-4 text-destructive" />
            ) : (
              <Mic className="h-4 w-4 text-green-500" />
            )}
            <Badge variant={isMuted ? "destructive" : "success"}>
              {isMuted ? 'Muted' : 'Recording'}
            </Badge>
          </div>

          {!isMuted && (
            <div className="flex-1 max-w-xs">
              <div className="flex items-center gap-2">
                <span className="text-xs text-muted-foreground">Audio Level:</span>
                <Progress value={audioLevel * 100} className="flex-1" />
              </div>
            </div>
          )}
        </>
      )}

      {connectionStatus.error && (
        <Badge variant="destructive" className="ml-auto">
          Error: {connectionStatus.error}
        </Badge>
      )}
    </div>
  );
};
