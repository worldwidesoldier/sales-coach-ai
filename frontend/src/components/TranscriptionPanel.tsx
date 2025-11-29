import { useEffect, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Transcription } from '@/types';
import { formatTimestamp } from '@/lib/utils';
import { User, UserCircle2 } from 'lucide-react';

interface TranscriptionPanelProps {
  transcriptions: Transcription[];
}

export const TranscriptionPanel = ({ transcriptions }: TranscriptionPanelProps) => {
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new transcriptions arrive
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [transcriptions]);

  const getSpeakerIcon = (speaker: string) => {
    if (speaker.includes('customer') || speaker.includes('speaker_0')) {
      return <UserCircle2 className="h-4 w-4" />;
    }
    return <User className="h-4 w-4" />;
  };

  const getSpeakerColor = (speaker: string) => {
    if (speaker.includes('customer') || speaker.includes('speaker_0')) {
      return 'text-blue-600 dark:text-blue-400';
    }
    return 'text-green-600 dark:text-green-400';
  };

  const getSpeakerLabel = (speaker: string) => {
    if (speaker.includes('customer') || speaker.includes('speaker_0')) {
      return 'Customer';
    }
    if (speaker.includes('salesperson') || speaker.includes('speaker_1')) {
      return 'You';
    }
    return 'Unknown';
  };

  return (
    <Card className="flex flex-col h-full">
      <CardHeader className="pb-3">
        <CardTitle className="text-lg flex items-center gap-2">
          Live Transcription
          {transcriptions.length > 0 && (
            <Badge variant="secondary" className="text-xs">
              {transcriptions.length} messages
            </Badge>
          )}
        </CardTitle>
      </CardHeader>
      <CardContent className="flex-1 overflow-hidden p-0">
        <div
          ref={scrollRef}
          className="h-full overflow-y-auto px-6 pb-6 space-y-4"
        >
          {transcriptions.length === 0 ? (
            <div className="flex items-center justify-center h-full text-muted-foreground">
              <p className="text-sm">Waiting for conversation to start...</p>
            </div>
          ) : (
            transcriptions.map((transcript, index) => (
              <div
                key={index}
                className={`flex gap-3 ${
                  transcript.is_final ? 'opacity-100' : 'opacity-60'
                }`}
              >
                <div className={`mt-1 ${getSpeakerColor(transcript.speaker)}`}>
                  {getSpeakerIcon(transcript.speaker)}
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <span className={`text-sm font-medium ${getSpeakerColor(transcript.speaker)}`}>
                      {getSpeakerLabel(transcript.speaker)}
                    </span>
                    <span className="text-xs text-muted-foreground">
                      {formatTimestamp(transcript.timestamp)}
                    </span>
                  </div>
                  <p className="text-sm text-foreground">
                    {transcript.text}
                  </p>
                </div>
              </div>
            ))
          )}
        </div>
      </CardContent>
    </Card>
  );
};
