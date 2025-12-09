import { motion } from 'framer-motion';
import { Target, AlertCircle, AlertTriangle, Zap } from 'lucide-react';
import { Card } from './ui/card';
import { Badge } from './ui/badge';
import { StageFocus, CoachingGuidance } from '@/types';

interface CurrentFocusProps {
  stage: 'opening' | 'discovery' | 'pitch' | 'objection' | 'close';
  focus: StageFocus;
  guidance?: CoachingGuidance;  // Optional, used to check if pre-call
}

export const CurrentFocus = ({ stage, focus, guidance }: CurrentFocusProps) => {
  const { what, why, urgency } = focus;
  const isPreCall = guidance?.metadata?.session_id === 'pre-call';
  const urgencyConfig = {
    low: {
      color: 'bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300',
      icon: Target,
      border: 'border-blue-300 dark:border-blue-700'
    },
    medium: {
      color: 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900 dark:text-yellow-300',
      icon: AlertCircle,
      border: 'border-yellow-300 dark:border-yellow-700'
    },
    high: {
      color: 'bg-orange-100 text-orange-700 dark:bg-orange-900 dark:text-orange-300',
      icon: AlertTriangle,
      border: 'border-orange-300 dark:border-orange-700'
    },
    critical: {
      color: 'bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300',
      icon: Zap,
      border: 'border-red-300 dark:border-red-700'
    }
  };

  const config = urgencyConfig[urgency];
  const Icon = config.icon;

  const stageColors: Record<string, string> = {
    opening: 'bg-blue-500',
    discovery: 'bg-purple-500',
    pitch: 'bg-indigo-500',
    objection: 'bg-orange-500',
    close: 'bg-green-500'
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
    >
      <Card className={`border-2 ${config.border} shadow-sm`}>
        <div className="p-4">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2 flex-wrap">
              <div className={`w-2 h-2 rounded-full ${stageColors[stage] || 'bg-gray-500'}`} />
              <h3 className="text-sm font-semibold text-gray-700 dark:text-gray-300 capitalize">
                {stage} Stage
              </h3>
              {isPreCall && (
                <Badge variant="outline" className="text-xs border-blue-400 text-blue-600 dark:border-blue-600 dark:text-blue-400">
                  Pre-Call Briefing
                </Badge>
              )}
            </div>
            <Badge className={config.color} variant="secondary">
              <Icon className="w-3 h-3 mr-1" />
              {urgency.toUpperCase()}
            </Badge>
          </div>

          <div className="space-y-2">
            <div>
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Focus:</p>
              <p className="text-base font-semibold text-gray-900 dark:text-white mt-0.5">
                {what}
              </p>
            </div>

            <div>
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Why:</p>
              <p className="text-sm text-gray-700 dark:text-gray-300 mt-0.5">
                {why}
              </p>
            </div>
          </div>
        </div>
      </Card>
    </motion.div>
  );
};
