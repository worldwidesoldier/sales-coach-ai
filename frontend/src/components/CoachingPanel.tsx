import { motion } from 'framer-motion';
import { CoachingGuidance, Transcription } from '@/types';
import { CallRoadmap } from './CallRoadmap';
import { CurrentFocus } from './CurrentFocus';
import { ObjectivesChecklist } from './ObjectivesChecklist';
import { GuidanceCard } from './GuidanceCard';
import { TranscriptionPanel } from './TranscriptionPanel';
import { Loader2 } from 'lucide-react';

interface CoachingPanelProps {
  guidance: CoachingGuidance;  // Always has value now (no null)
  transcriptions: Transcription[];
}

export const CoachingPanel = ({ guidance, transcriptions }: CoachingPanelProps) => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.4 }}
      className="h-screen flex flex-col overflow-hidden"
    >
      {/* TOP 30%: TRANSCRIPT */}
      <div className="h-[30vh] flex-shrink-0">
        <TranscriptionPanel transcriptions={transcriptions} />
      </div>

      {/* MIDDLE 58%: GUIDANCE HERO */}
      <div className="h-[58vh] flex-shrink-0 flex flex-col gap-2 p-3 overflow-hidden">
        {/* Roadmap - Compact */}
        <div className="flex-shrink-0">
          <CallRoadmap stage={guidance.stage} />
        </div>

        {/* CurrentFocus - Compact */}
        <div className="flex-shrink-0">
          <CurrentFocus
            stage={guidance.stage.current}
            focus={guidance.focus}
            guidance={guidance}
          />
        </div>

        {/* GuidanceCard - LARGE (takes most space) */}
        <div className="flex-1 min-h-[300px] overflow-y-auto">
          <GuidanceCard guidance={guidance.guidance} />
        </div>

        {/* ObjectivesChecklist - Bottom */}
        <div className="flex-shrink-0">
          <ObjectivesChecklist objectives={guidance.objectives} />
        </div>
      </div>

      {/* BOTTOM 12%: Quick Toolkit Placeholder */}
      <div className="h-[12vh] flex-shrink-0 flex items-center justify-center bg-gray-50 dark:bg-gray-900 border-t border-gray-200 dark:border-gray-800">
        <p className="text-sm text-gray-500 dark:text-gray-400">
          Quick Toolkit coming soon
        </p>
      </div>
    </motion.div>
  );
};
