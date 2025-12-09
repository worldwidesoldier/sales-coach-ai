import { useState } from 'react';
import { CoachingPanel } from './CoachingPanel';
import { CoachingGuidance } from '@/types';

/**
 * Demo component showing CoachingPanel with sample data
 * This is for testing and demonstration purposes
 */
export const CoachingPanelDemo = () => {
  const [sampleGuidance] = useState<CoachingGuidance>({
    type: 'coaching_guidance',
    stage: {
      current: 'discovery',
      confidence: 0.85,
      time_in_stage: 45
    },
    focus: {
      what: 'Uncover the customer\'s pain points and budget constraints',
      why: 'Discovery is critical for positioning the right solution and avoiding objections later',
      urgency: 'high'
    },
    objectives: {
      completed: [
        {
          id: 'obj-1',
          text: 'Established rapport with decision maker',
          priority: 'high',
          completed_at: Date.now() - 30000
        },
        {
          id: 'obj-2',
          text: 'Confirmed their current process',
          priority: 'medium',
          completed_at: Date.now() - 15000
        }
      ],
      remaining: [
        {
          id: 'obj-3',
          text: 'Identify budget range and approval process',
          priority: 'high'
        },
        {
          id: 'obj-4',
          text: 'Understand timeline and urgency',
          priority: 'high'
        },
        {
          id: 'obj-5',
          text: 'Map out key stakeholders',
          priority: 'medium'
        }
      ]
    },
    guidance: {
      direction: 'Focus on asking open-ended questions about their current challenges. Listen more than you talk.',
      key_questions: [
        'What prompted you to look for a solution now?',
        'How is this problem impacting your team today?',
        'What have you tried in the past to solve this?',
        'If we could solve this perfectly, what would that look like?'
      ],
      talking_points: [
        'Reference similar customers in their industry',
        'Acknowledge their pain points with empathy',
        'Build credibility through industry knowledge'
      ],
      confidence: 0.92
    },
    metadata: {
      timestamp: Date.now(),
      session_id: 'demo-session-123',
      model_version: 'v1.0.0'
    }
  });

  return (
    <div className="h-screen w-full p-8 bg-gray-50 dark:bg-gray-900">
      <div className="max-w-4xl mx-auto h-full">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
          Coaching Panel Demo
        </h1>
        <div className="h-[calc(100%-3rem)] bg-white dark:bg-gray-800 rounded-lg shadow-lg p-4">
          <CoachingPanel guidance={sampleGuidance} />
        </div>
      </div>
    </div>
  );
};
