import { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { SavedCall, CallAnalysis as CallAnalysisType } from '@/types';
import { CallAnalysis } from '@/components/CallAnalysis';
import { Trash2, FileText, BarChart3, X, Loader2 } from 'lucide-react';

export const CallHistory = () => {
  const [calls, setCalls] = useState<SavedCall[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedCall, setSelectedCall] = useState<string | null>(null);
  const [analysis, setAnalysis] = useState<CallAnalysisType | null>(null);
  const [analysisLoading, setAnalysisLoading] = useState(false);
  const [generatingAnalysis, setGeneratingAnalysis] = useState(false);

  const fetchCalls = async () => {
    try {
      const response = await fetch('http://localhost:5001/api/calls');
      if (response.ok) {
        const data = await response.json();
        setCalls(data);
      }
    } catch (error) {
      console.error('Error fetching calls:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCalls();
    // Refresh every 10 seconds
    const interval = setInterval(fetchCalls, 10000);
    return () => clearInterval(interval);
  }, []);

  const deleteCall = async (callId: string) => {
    try {
      const response = await fetch(`http://localhost:5001/api/calls/${callId}`, {
        method: 'DELETE',
      });
      if (response.ok) {
        fetchCalls();
        if (selectedCall === callId) {
          setSelectedCall(null);
          setAnalysis(null);
        }
      }
    } catch (error) {
      console.error('Error deleting call:', error);
    }
  };

  const fetchAnalysis = async (callId: string) => {
    setAnalysisLoading(true);
    try {
      const response = await fetch(`http://localhost:5001/api/calls/${callId}/analyze`);
      if (response.ok) {
        const data = await response.json();
        setAnalysis(data);
      } else if (response.status === 404) {
        // Analysis doesn't exist yet
        setAnalysis(null);
      } else {
        console.error('Error fetching analysis:', response.statusText);
      }
    } catch (error) {
      console.error('Error fetching analysis:', error);
    } finally {
      setAnalysisLoading(false);
    }
  };

  const generateAnalysis = async (callId: string) => {
    setGeneratingAnalysis(true);
    try {
      const response = await fetch(`http://localhost:5001/api/calls/${callId}/analyze`, {
        method: 'POST',
      });
      if (response.ok) {
        const data = await response.json();
        setAnalysis(data);
      } else {
        console.error('Error generating analysis:', response.statusText);
      }
    } catch (error) {
      console.error('Error generating analysis:', error);
    } finally {
      setGeneratingAnalysis(false);
    }
  };

  const handleCallClick = async (callId: string) => {
    setSelectedCall(callId);
    await fetchAnalysis(callId);
  };

  const closeAnalysis = () => {
    setSelectedCall(null);
    setAnalysis(null);
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <>
      <Card className="w-80">
        <CardHeader className="pb-3">
          <CardTitle className="text-lg flex items-center justify-between">
            Call History
            {calls.length > 0 && (
              <Badge variant="secondary" className="text-xs">
                {calls.length}
              </Badge>
            )}
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-2 max-h-[600px] overflow-y-auto">
          {loading ? (
            <p className="text-sm text-muted-foreground">Loading...</p>
          ) : calls.length === 0 ? (
            <p className="text-sm text-muted-foreground">No saved calls yet</p>
          ) : (
            calls.map((call) => (
              <div
                key={call.id}
                className="p-3 rounded-lg border bg-card hover:bg-accent/50 transition-colors cursor-pointer"
                onClick={() => handleCallClick(call.id)}
              >
                <div className="flex items-start justify-between gap-2">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <FileText className="h-3 w-3 text-muted-foreground shrink-0" />
                      <p className="text-xs font-medium truncate">
                        {call.id.replace('call_', '')}
                      </p>
                    </div>
                    <p className="text-xs text-muted-foreground mb-2">
                      {formatDate(call.start_time)}
                    </p>
                    <div className="flex gap-2">
                      <Badge variant="outline" className="text-xs">
                        {call.transcript_count} msgs
                      </Badge>
                      <Badge variant="outline" className="text-xs">
                        {call.suggestion_count} tips
                      </Badge>
                    </div>
                  </div>
                  <div className="flex gap-1">
                    <Button
                      variant="ghost"
                      size="icon"
                      className="h-8 w-8"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleCallClick(call.id);
                      }}
                    >
                      <BarChart3 className="h-4 w-4" />
                    </Button>
                    <Button
                      variant="ghost"
                      size="icon"
                      className="h-8 w-8 text-destructive"
                      onClick={(e) => {
                        e.stopPropagation();
                        deleteCall(call.id);
                      }}
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              </div>
            ))
          )}
        </CardContent>
      </Card>

      {/* Analysis Modal */}
      {selectedCall && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-background rounded-lg shadow-lg max-w-2xl w-full max-h-[90vh] overflow-hidden flex flex-col">
            <div className="flex items-center justify-between p-4 border-b">
              <h3 className="text-lg font-semibold">
                Call Analysis: {selectedCall.replace('call_', '')}
              </h3>
              <Button variant="ghost" size="icon" onClick={closeAnalysis}>
                <X className="h-4 w-4" />
              </Button>
            </div>
            <div className="flex-1 overflow-y-auto p-4">
              {analysisLoading ? (
                <div className="flex items-center justify-center h-32">
                  <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
                </div>
              ) : analysis ? (
                <CallAnalysis analysis={analysis} />
              ) : (
                <div className="flex flex-col items-center justify-center h-32 gap-4">
                  <p className="text-sm text-muted-foreground">
                    No analysis available for this call
                  </p>
                  <Button
                    onClick={() => generateAnalysis(selectedCall)}
                    disabled={generatingAnalysis}
                  >
                    {generatingAnalysis ? (
                      <>
                        <Loader2 className="h-4 w-4 animate-spin mr-2" />
                        Generating...
                      </>
                    ) : (
                      <>
                        <BarChart3 className="h-4 w-4 mr-2" />
                        Generate Analysis
                      </>
                    )}
                  </Button>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </>
  );
};
