import { useEffect, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertTitle, AlertDescription } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import { Suggestion } from '@/types';
import { Lightbulb, AlertTriangle, TrendingUp, Copy } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface SuggestionsPanelProps {
  suggestions: Suggestion[];
}

export const SuggestionsPanel = ({ suggestions }: SuggestionsPanelProps) => {
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new suggestions arrive
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [suggestions]);

  const getAlertVariant = (sentiment: string) => {
    switch (sentiment) {
      case 'positive':
        return 'success';
      case 'negative':
        return 'destructive';
      default:
        return 'default';
    }
  };

  const getSentimentBadge = (sentiment: string) => {
    switch (sentiment) {
      case 'positive':
        return <Badge variant="success">Positive</Badge>;
      case 'negative':
        return <Badge variant="danger">Negative</Badge>;
      default:
        return <Badge variant="secondary">Neutral</Badge>;
    }
  };

  const getObjectionIcon = (objection_type: string) => {
    if (objection_type !== 'none') {
      return <AlertTriangle className="h-4 w-4" />;
    }
    return <Lightbulb className="h-4 w-4" />;
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  return (
    <Card className="flex flex-col h-full">
      <CardHeader className="pb-3">
        <CardTitle className="text-lg flex items-center gap-2">
          AI Suggestions
          {suggestions.length > 0 && (
            <Badge variant="secondary" className="text-xs">
              {suggestions.length} suggestions
            </Badge>
          )}
        </CardTitle>
      </CardHeader>
      <CardContent className="flex-1 overflow-hidden p-0">
        <div
          ref={scrollRef}
          className="h-full overflow-y-auto px-6 pb-6 space-y-4"
        >
          {suggestions.length === 0 ? (
            <div className="flex items-center justify-center h-full text-muted-foreground">
              <p className="text-sm">AI suggestions will appear here...</p>
            </div>
          ) : (
            suggestions.map((suggestion, index) => (
              <Alert key={index} variant={getAlertVariant(suggestion.sentiment)}>
                {getObjectionIcon(suggestion.objection_type)}
                <div className="flex-1">
                  <div className="flex items-center justify-between mb-2">
                    <AlertTitle className="flex items-center gap-2">
                      {suggestion.objection_detected && (
                        <Badge variant="destructive" className="text-xs">
                          Objection: {suggestion.objection_type}
                        </Badge>
                      )}
                      {suggestion.buying_signal && (
                        <Badge variant="success" className="text-xs gap-1">
                          <TrendingUp className="h-3 w-3" />
                          Buying Signal
                        </Badge>
                      )}
                      {getSentimentBadge(suggestion.sentiment)}
                      <Badge variant="outline" className="text-xs">
                        {suggestion.confidence}% confident
                      </Badge>
                    </AlertTitle>
                  </div>

                  <AlertDescription className="space-y-2">
                    <div>
                      <div className="flex items-start justify-between gap-2">
                        <div className="flex-1">
                          <p className="font-medium text-sm mb-1">Suggested Response:</p>
                          <p className="text-sm">{suggestion.suggestion}</p>
                        </div>
                        <Button
                          variant="ghost"
                          size="icon"
                          className="h-8 w-8"
                          onClick={() => copyToClipboard(suggestion.suggestion)}
                        >
                          <Copy className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>

                    <div className="pt-2 border-t border-border/50">
                      <p className="text-xs text-muted-foreground">
                        <span className="font-medium">Strategy:</span> {suggestion.strategy}
                      </p>
                    </div>
                  </AlertDescription>
                </div>
              </Alert>
            ))
          )}
        </div>
      </CardContent>
    </Card>
  );
};
