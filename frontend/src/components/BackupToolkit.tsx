import { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { X, Target, XCircle, DollarSign, Clock, Bot, CheckCircle, HelpCircle } from 'lucide-react';

interface Script {
  name: string;
  text: string;
  when_to_use: string;
}

interface ToolkitCategory {
  title: string;
  scripts: Script[];
}

interface Toolkit {
  [key: string]: ToolkitCategory;
}

interface BackupToolkitProps {
  highlightedCategories?: string[];
}

const TOOLKIT_ICONS: { [key: string]: React.ReactNode } = {
  opener: <Target className="h-4 w-4" />,
  not_interested: <XCircle className="h-4 w-4" />,
  price: <DollarSign className="h-4 w-4" />,
  callback: <Clock className="h-4 w-4" />,
  ai_concerns: <Bot className="h-4 w-4" />,
  closing: <CheckCircle className="h-4 w-4" />,
  discovery: <HelpCircle className="h-4 w-4" />,
};

export const BackupToolkit = ({ highlightedCategories = [] }: BackupToolkitProps) => {
  const [toolkit, setToolkit] = useState<Toolkit>({});
  const [expandedCategory, setExpandedCategory] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const cardRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const fetchToolkit = async () => {
      try {
        const response = await fetch('http://localhost:5001/api/toolkit');
        if (response.ok) {
          const data = await response.json();
          setToolkit(data);
        } else {
          console.error('Failed to fetch toolkit');
        }
      } catch (error) {
        console.error('Error fetching toolkit:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchToolkit();
  }, []);

  // Close on click outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (cardRef.current && !cardRef.current.contains(event.target as Node)) {
        setExpandedCategory(null);
      }
    };

    if (expandedCategory) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [expandedCategory]);

  const toggleCategory = (categoryKey: string) => {
    setExpandedCategory(expandedCategory === categoryKey ? null : categoryKey);
  };

  const isHighlighted = (categoryKey: string) => {
    return highlightedCategories.includes(categoryKey);
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  if (loading) {
    return (
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-lg">Backup Toolkit</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">Loading toolkit...</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card ref={cardRef}>
      <CardHeader className="pb-3">
        <CardTitle className="text-lg">Backup Toolkit</CardTitle>
        <p className="text-sm text-muted-foreground">
          Click a category for pre-written scripts
        </p>
      </CardHeader>
      <CardContent className="space-y-2">
        {Object.entries(toolkit).map(([key, category]) => {
          const highlighted = isHighlighted(key);
          const isExpanded = expandedCategory === key;

          return (
            <div key={key} className="space-y-2">
              <Button
                variant={highlighted ? 'default' : 'outline'}
                className={`w-full justify-start gap-2 ${
                  highlighted ? 'animate-pulse bg-primary' : ''
                }`}
                onClick={() => toggleCategory(key)}
              >
                {TOOLKIT_ICONS[key]}
                <span className="flex-1 text-left">{category.title}</span>
                {highlighted && (
                  <Badge variant="secondary" className="text-xs">
                    Recommended
                  </Badge>
                )}
              </Button>

              {isExpanded && (
                <div className="space-y-2 pl-4 border-l-2 border-primary/30">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="text-sm font-semibold">{category.title}</h4>
                    <Button
                      variant="ghost"
                      size="icon"
                      className="h-6 w-6"
                      onClick={() => setExpandedCategory(null)}
                    >
                      <X className="h-4 w-4" />
                    </Button>
                  </div>

                  {category.scripts.map((script, index) => (
                    <Card
                      key={index}
                      className="bg-muted/50 border-muted hover:border-primary/50 transition-colors cursor-pointer"
                      onClick={() => copyToClipboard(script.text)}
                    >
                      <CardContent className="p-3 space-y-2">
                        <div className="flex items-center justify-between">
                          <h5 className="text-sm font-medium">{script.name}</h5>
                          <Badge variant="outline" className="text-xs">
                            Click to copy
                          </Badge>
                        </div>
                        <p className="text-sm text-foreground">{script.text}</p>
                        <p className="text-xs text-muted-foreground">
                          <span className="font-medium">When to use:</span> {script.when_to_use}
                        </p>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              )}
            </div>
          );
        })}
      </CardContent>
    </Card>
  );
};
