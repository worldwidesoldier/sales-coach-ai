import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { CoachingSuggestion } from '@/types';
import { Zap, AlertTriangle, TrendingUp, Clock } from 'lucide-react';

interface PrimarySuggestionPanelProps {
  suggestion: CoachingSuggestion | null;
}

export const PrimarySuggestionPanel = ({ suggestion }: PrimarySuggestionPanelProps) => {
  if (!suggestion) {
    return (
      <Card className="flex flex-col h-full">
        <CardHeader className="pb-3">
          <CardTitle className="text-lg flex items-center gap-2">
            <Zap className="h-5 w-5 text-yellow-500" />
            Primary Suggestion
          </CardTitle>
        </CardHeader>
        <CardContent className="flex-1 flex items-center justify-center">
          <p className="text-sm text-muted-foreground">
            Waiting for Claude's coaching...
          </p>
        </CardContent>
      </Card>
    );
  }

  const { primary_suggestion, context } = suggestion;

  // Get sentiment-based colors
  const getSentimentColors = (sentiment: string) => {
    switch (sentiment) {
      case 'positive':
        return {
          border: 'border-green-500',
          bg: 'bg-green-50 dark:bg-green-950/20',
          text: 'text-green-700 dark:text-green-300',
        };
      case 'negative':
        return {
          border: 'border-red-500',
          bg: 'bg-red-50 dark:bg-red-950/20',
          text: 'text-red-700 dark:text-red-300',
        };
      default:
        return {
          border: 'border-yellow-500',
          bg: 'bg-yellow-50 dark:bg-yellow-950/20',
          text: 'text-yellow-700 dark:text-yellow-300',
        };
    }
  };

  const colors = getSentimentColors(context.sentiment);

  // Get urgency badge
  const getUrgencyBadge = (urgency: string) => {
    switch (urgency) {
      case 'critical':
        return <Badge variant="danger" className="gap-1"><Zap className="h-3 w-3" />Critical</Badge>;
      case 'high':
        return <Badge variant="warning" className="gap-1"><AlertTriangle className="h-3 w-3" />High</Badge>;
      case 'medium':
        return <Badge variant="secondary">Medium</Badge>;
      default:
        return <Badge variant="outline">Low</Badge>;
    }
  };

  // Get call stage badge
  const getCallStageBadge = (stage: string) => {
    const stageColors = {
      opening: 'bg-blue-500 text-white',
      discovery: 'bg-purple-500 text-white',
      pitch: 'bg-indigo-500 text-white',
      objection: 'bg-orange-500 text-white',
      close: 'bg-green-500 text-white',
    };

    return (
      <Badge className={stageColors[stage as keyof typeof stageColors] || 'bg-gray-500 text-white'}>
        {stage.charAt(0).toUpperCase() + stage.slice(1)}
      </Badge>
    );
  };

  // Get confidence color
  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 80) return 'text-green-600 dark:text-green-400';
    if (confidence >= 60) return 'text-yellow-600 dark:text-yellow-400';
    return 'text-red-600 dark:text-red-400';
  };

  return (
    <Card className={`flex flex-col h-full border-2 ${colors.border} ${colors.bg}`}>
      <CardHeader className="pb-3">
        <CardTitle className="text-lg flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Zap className="h-5 w-5 text-yellow-500" />
            Primary Suggestion
          </div>
          <div className="flex items-center gap-2">
            {getCallStageBadge(context.call_stage)}
            {getUrgencyBadge(primary_suggestion.urgency)}
          </div>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Main Suggestion */}
        <div className={`p-4 rounded-lg border-2 ${colors.border} bg-white dark:bg-gray-900`}>
          <p className="text-base font-semibold mb-2 text-foreground">
            {primary_suggestion.text}
          </p>
          <div className="flex items-center gap-2 text-xs text-muted-foreground">
            <Clock className="h-3 w-3" />
            <span>Act on this now</span>
          </div>
        </div>

        {/* Context Badges */}
        <div className="flex flex-wrap gap-2">
          {context.objection_detected && (
            <Badge variant="destructive" className="gap-1">
              <AlertTriangle className="h-3 w-3" />
              Objection: {context.objection_type}
            </Badge>
          )}
          {context.buying_signal && (
            <Badge variant="success" className="gap-1">
              <TrendingUp className="h-3 w-3" />
              Buying Signal
            </Badge>
          )}
          <Badge
            variant={context.sentiment === 'positive' ? 'success' : context.sentiment === 'negative' ? 'danger' : 'warning'}
          >
            {context.sentiment.charAt(0).toUpperCase() + context.sentiment.slice(1)} Sentiment
          </Badge>
          <Badge variant="outline" className={getConfidenceColor(primary_suggestion.confidence)}>
            {primary_suggestion.confidence}% Confident
          </Badge>
        </div>

        {/* Reasoning */}
        <div className="pt-3 border-t border-border">
          <p className="text-xs font-medium text-muted-foreground mb-2">Why this suggestion:</p>
          <p className="text-sm text-foreground">
            {primary_suggestion.reasoning}
          </p>
        </div>
      </CardContent>
    </Card>
  );
};
