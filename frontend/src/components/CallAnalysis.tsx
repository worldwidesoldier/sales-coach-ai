import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertTitle, AlertDescription } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import { CheckCircle2, AlertTriangle, TrendingUp, Clock } from 'lucide-react';

interface MissedOpportunity {
  timestamp: string;
  opportunity: string;
  what_to_do: string;
}

interface CallAnalysisData {
  what_worked: string[];
  missed_opportunities: MissedOpportunity[];
  improvement_tips: string[];
  success_score: number;
  call_outcome?: 'positive' | 'neutral' | 'negative';
  key_insights?: string;
}

interface CallAnalysisProps {
  analysis: CallAnalysisData | null;
}

export const CallAnalysis = ({ analysis }: CallAnalysisProps) => {
  if (!analysis) {
    return (
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-lg">Call Analysis</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center h-32 text-muted-foreground">
            <p className="text-sm">Analysis will appear after call ends</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  const getScoreColor = (score: number) => {
    if (score >= 8) return 'text-green-600';
    if (score >= 5) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getOutcomeBadge = (outcome?: string) => {
    switch (outcome) {
      case 'positive':
        return <Badge variant="success">Positive Outcome</Badge>;
      case 'negative':
        return <Badge variant="danger">Needs Improvement</Badge>;
      default:
        return <Badge variant="secondary">Neutral</Badge>;
    }
  };

  return (
    <Card>
      <CardHeader className="pb-4">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg">Call Analysis</CardTitle>
          {analysis.call_outcome && getOutcomeBadge(analysis.call_outcome)}
        </div>
        {analysis.key_insights && (
          <p className="text-sm text-muted-foreground mt-2">{analysis.key_insights}</p>
        )}
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Success Score */}
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <h4 className="text-sm font-semibold">Success Score</h4>
            <span className={`text-2xl font-bold ${getScoreColor(analysis.success_score)}`}>
              {analysis.success_score}/10
            </span>
          </div>
          <div className="relative h-3 w-full overflow-hidden rounded-full bg-secondary">
            <div
              className={`h-full transition-all ${
                analysis.success_score >= 8
                  ? 'bg-green-500'
                  : analysis.success_score >= 5
                  ? 'bg-yellow-500'
                  : 'bg-red-500'
              }`}
              style={{ width: `${analysis.success_score * 10}%` }}
            />
          </div>
        </div>

        {/* What Worked */}
        {analysis.what_worked.length > 0 && (
          <Alert variant="success">
            <CheckCircle2 className="h-4 w-4" />
            <div className="flex-1">
              <AlertTitle className="flex items-center gap-2 mb-2">
                What Worked
                <Badge variant="success" className="text-xs">
                  {analysis.what_worked.length}
                </Badge>
              </AlertTitle>
              <AlertDescription>
                <ul className="space-y-1">
                  {analysis.what_worked.map((item, index) => (
                    <li key={index} className="text-sm flex items-start gap-2">
                      <span className="text-green-600 mt-0.5">✓</span>
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </AlertDescription>
            </div>
          </Alert>
        )}

        {/* Missed Opportunities */}
        {analysis.missed_opportunities.length > 0 && (
          <Alert variant="warning">
            <AlertTriangle className="h-4 w-4" />
            <div className="flex-1">
              <AlertTitle className="flex items-center gap-2 mb-2">
                Missed Opportunities
                <Badge variant="warning" className="text-xs">
                  {analysis.missed_opportunities.length}
                </Badge>
              </AlertTitle>
              <AlertDescription>
                <div className="space-y-3">
                  {analysis.missed_opportunities.map((opportunity, index) => (
                    <div key={index} className="border-l-2 border-yellow-500/50 pl-3 space-y-1">
                      <div className="flex items-center gap-2 text-xs text-muted-foreground">
                        <Clock className="h-3 w-3" />
                        {opportunity.timestamp}
                      </div>
                      <p className="text-sm font-medium">{opportunity.opportunity}</p>
                      <p className="text-sm text-muted-foreground">
                        <span className="font-medium">What to do:</span> {opportunity.what_to_do}
                      </p>
                    </div>
                  ))}
                </div>
              </AlertDescription>
            </div>
          </Alert>
        )}

        {/* Improvement Tips */}
        {analysis.improvement_tips.length > 0 && (
          <Alert variant="default">
            <TrendingUp className="h-4 w-4" />
            <div className="flex-1">
              <AlertTitle className="flex items-center gap-2 mb-2">
                Improvement Tips
                <Badge variant="secondary" className="text-xs">
                  {analysis.improvement_tips.length}
                </Badge>
              </AlertTitle>
              <AlertDescription>
                <ul className="space-y-1">
                  {analysis.improvement_tips.map((tip, index) => (
                    <li key={index} className="text-sm flex items-start gap-2">
                      <span className="text-primary mt-0.5">→</span>
                      <span>{tip}</span>
                    </li>
                  ))}
                </ul>
              </AlertDescription>
            </div>
          </Alert>
        )}
      </CardContent>
    </Card>
  );
};
