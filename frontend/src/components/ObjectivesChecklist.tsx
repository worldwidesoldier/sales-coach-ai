import { motion } from 'framer-motion';
import { CheckCircle2, Circle } from 'lucide-react';
import { Card } from './ui/card';
import { Badge } from './ui/badge';
import { Objectives } from '@/types';

interface ObjectivesChecklistProps {
  objectives: Objectives;
}

export const ObjectivesChecklist = ({ objectives }: ObjectivesChecklistProps) => {
  const { completed, remaining } = objectives;
  const totalObjectives = completed.length + remaining.length;
  const progress = totalObjectives > 0 ? (completed.length / totalObjectives) * 100 : 0;

  const priorityColors = {
    low: 'bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400',
    medium: 'bg-blue-100 text-blue-600 dark:bg-blue-900 dark:text-blue-400',
    high: 'bg-orange-100 text-orange-600 dark:bg-orange-900 dark:text-orange-400'
  };

  return (
    <Card className="shadow-sm">
      <div className="p-4">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-lg font-bold text-gray-900 dark:text-white">Objectives</h3>
          <div className="flex items-center gap-2">
            <span className="text-sm font-medium text-gray-600 dark:text-gray-400">
              {completed.length}/{totalObjectives}
            </span>
            <div className="w-16 h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${progress}%` }}
                transition={{ duration: 0.4 }}
                className="h-full bg-green-500"
              />
            </div>
          </div>
        </div>

        <div className="space-y-1.5 max-h-48 overflow-y-auto">
          {/* Completed objectives */}
          {completed.map((objective, index) => (
            <motion.div
              key={objective.id}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.4, delay: index * 0.05 }}
              className="flex items-start gap-2 p-2 rounded-md bg-green-50 dark:bg-green-900/20"
            >
              <CheckCircle2 className="w-5 h-5 text-green-600 dark:text-green-400 flex-shrink-0 mt-0.5" />
              <div className="flex-1 min-w-0">
                <p className="text-sm text-gray-700 dark:text-gray-300 line-through">
                  {objective.text}
                </p>
                {objective.priority && (
                  <Badge className={`${priorityColors[objective.priority]} text-xs mt-1`} variant="secondary">
                    {objective.priority}
                  </Badge>
                )}
              </div>
            </motion.div>
          ))}

          {/* Remaining objectives */}
          {remaining.map((objective, index) => (
            <motion.div
              key={objective.id}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.4, delay: (completed.length + index) * 0.05 }}
              className="flex items-start gap-2 p-2 rounded-md hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
            >
              <Circle className="w-5 h-5 text-gray-400 dark:text-gray-600 flex-shrink-0 mt-0.5" />
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 dark:text-white">
                  {objective.text}
                </p>
                {objective.priority && (
                  <Badge className={`${priorityColors[objective.priority]} text-xs mt-1`} variant="secondary">
                    {objective.priority}
                  </Badge>
                )}
              </div>
            </motion.div>
          ))}

          {/* Empty state */}
          {totalObjectives === 0 && (
            <div className="text-center py-4">
              <p className="text-sm text-gray-500 dark:text-gray-400">
                No objectives yet
              </p>
            </div>
          )}
        </div>
      </div>
    </Card>
  );
};
