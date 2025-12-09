import { Check, Circle, Loader2 } from 'lucide-react';
import { motion } from 'framer-motion';
import { CallStage } from '@/types';

interface CallRoadmapProps {
  stage: CallStage;
}

export const CallRoadmap = ({ stage }: CallRoadmapProps) => {
  const stages = [
    { id: 'opening', label: 'Opening', color: '#3B82F6' },
    { id: 'discovery', label: 'Discovery', color: '#A855F7' },
    { id: 'pitch', label: 'Pitch', color: '#6366F1' },
    { id: 'objection', label: 'Objection', color: '#F97316' },
    { id: 'close', label: 'Close', color: '#10B981' }
  ];

  const getStageStatus = (stageId: string) => {
    if (stageId === stage.current) return 'current';
    // Mark all previous stages as completed
    const currentIndex = stages.findIndex(s => s.id === stage.current);
    const stageIndex = stages.findIndex(s => s.id === stageId);
    if (stageIndex < currentIndex) return 'completed';
    return 'pending';
  };

  const currentIndex = stages.findIndex(s => s.id === stage.current);

  return (
    <div className="w-full bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-4">
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-sm font-semibold text-gray-700 dark:text-gray-300">Call Progress</h3>
        <span className="text-xs text-gray-500 dark:text-gray-400">
          {Math.round(stage.confidence * 100)}% confident
        </span>
      </div>

      <div className="flex items-center justify-between gap-2">
        {stages.map((stage, index) => {
          const status = getStageStatus(stage.id);
          const isActive = status === 'current';
          const isCompleted = status === 'completed';
          const isPending = status === 'pending';

          return (
            <div key={stage.id} className="flex items-center flex-1">
              {/* Stage circle */}
              <div className="flex flex-col items-center flex-1">
                <motion.div
                  initial={false}
                  animate={{
                    scale: isActive ? 1.1 : 1,
                    backgroundColor: isActive || isCompleted ? stage.color : '#E5E7EB'
                  }}
                  transition={{ duration: 0.4 }}
                  className="w-10 h-10 rounded-full flex items-center justify-center relative"
                  style={{
                    boxShadow: isActive ? `0 0 0 4px ${stage.color}20` : 'none'
                  }}
                >
                  {isCompleted && (
                    <motion.div
                      initial={{ scale: 0, rotate: -180 }}
                      animate={{ scale: 1, rotate: 0 }}
                      transition={{ duration: 0.4 }}
                    >
                      <Check className="w-5 h-5 text-white" />
                    </motion.div>
                  )}
                  {isActive && (
                    <motion.div
                      animate={{ rotate: 360 }}
                      transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
                    >
                      <Loader2 className="w-5 h-5 text-white" />
                    </motion.div>
                  )}
                  {isPending && (
                    <Circle className="w-5 h-5 text-gray-400" />
                  )}
                </motion.div>

                {/* Stage label */}
                <motion.span
                  initial={false}
                  animate={{
                    color: isActive ? stage.color : isCompleted ? '#6B7280' : '#9CA3AF',
                    fontWeight: isActive ? 600 : 500
                  }}
                  transition={{ duration: 0.4 }}
                  className="text-xs mt-1.5 text-center"
                >
                  {stage.label}
                </motion.span>
              </div>

              {/* Connector line */}
              {index < stages.length - 1 && (
                <div className="flex-1 h-1 mx-1 relative overflow-hidden rounded-full bg-gray-200 dark:bg-gray-700">
                  <motion.div
                    initial={false}
                    animate={{
                      width: index < currentIndex ? '100%' : '0%',
                      backgroundColor: stages[index].color
                    }}
                    transition={{ duration: 0.4 }}
                    className="h-full"
                  />
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};
