import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { CoachingSuggestion } from '@/types';
import { Zap, AlertTriangle, TrendingUp, Clock } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface PrimarySuggestionPanelProps {
  currentSuggestion: CoachingSuggestion | null;
  previousSuggestion: CoachingSuggestion | null;
}

// Helper functions
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

const getConfidenceColor = (confidence: number) => {
  if (confidence >= 80) return 'text-green-600 dark:text-green-400';
  if (confidence >= 60) return 'text-yellow-600 dark:text-yellow-400';
  return 'text-red-600 dark:text-red-400';
};

// Primary Card Component (Full Detail)
const PrimaryCard = ({ suggestion }: { suggestion: CoachingSuggestion }) => {
  const { primary_suggestion, context } = suggestion;
  const colors = getSentimentColors(context.sentiment);

  return (
    <Card className={`flex flex-col border-2 ${colors.border} ${colors.bg}`}>
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

// Secondary Card Component (Compact)
const SecondaryCard = ({ suggestion }: { suggestion: CoachingSuggestion }) => {
  const { primary_suggestion, context } = suggestion;

  return (
    <Card className="opacity-85 scale-98 transition-all border border-border bg-muted/50">
      <CardHeader className="pb-2">
        <div className="flex items-center justify-between">
          <CardTitle className="text-base text-muted-foreground flex items-center gap-2">
            <Clock className="h-4 w-4" />
            Previous Suggestion
          </CardTitle>
          {getUrgencyBadge(primary_suggestion.urgency)}
        </div>
      </CardHeader>
      <CardContent className="pt-2 space-y-2">
        <p className="text-sm text-foreground">
          {primary_suggestion.text}
        </p>
        <p className="text-xs text-muted-foreground line-clamp-2">
          {primary_suggestion.reasoning}
        </p>
      </CardContent>
    </Card>
  );
};

// Main Component
export const PrimarySuggestionPanel = ({
  currentSuggestion,
  previousSuggestion,
}: PrimarySuggestionPanelProps) => {
  return (
    <div className="flex flex-col gap-4 p-1">
      {/* PRIMARY SUGGESTION (Latest) */}
      <AnimatePresence mode="wait">
        {currentSuggestion ? (
          <motion.div
            key={currentSuggestion.primary_suggestion.text}
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0.7, y: 60, scale: 0.95 }}
            transition={{ duration: 0.4, ease: 'easeInOut' }}
          >
            <PrimaryCard suggestion={currentSuggestion} />
          </motion.div>
        ) : (
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
        )}
      </AnimatePresence>

      {/* PREVIOUS SUGGESTION (Secondary) */}
      <AnimatePresence>
        {previousSuggestion && (
          <motion.div
            key={previousSuggestion.primary_suggestion.text}
            initial={{ opacity: 0, y: -60, scale: 0.95 }}
            animate={{ opacity: 0.7, y: 0, scale: 0.95 }}
            exit={{ opacity: 0, y: 20, scale: 0.9 }}
            transition={{ duration: 0.4, ease: 'easeInOut' }}
          >
            <SecondaryCard suggestion={previousSuggestion} />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};
