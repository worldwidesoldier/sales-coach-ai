import { useState } from 'react';
import { motion } from 'framer-motion';
import { Lightbulb, HelpCircle, MessageSquare, TrendingUp, ChevronRight, ChevronDown } from 'lucide-react';
import { Card } from './ui/card';
import { Badge } from './ui/badge';
import { Guidance, GuidanceQuestion } from '@/types';

interface GuidanceCardProps {
  guidance: Guidance;
}

export const GuidanceCard = ({ guidance }: GuidanceCardProps) => {
  const { direction, key_questions: keyQuestions, talking_points: talkingPoints, confidence } = guidance;
  const [expandedQuestion, setExpandedQuestion] = useState<number | null>(null);

  // DEBUG: Log what we're receiving
  console.log('🔍 GuidanceCard render:', {
    keyQuestionsCount: keyQuestions?.length || 0,
    firstQuestion: keyQuestions?.[0],
    questionType: typeof keyQuestions?.[0]
  });

  return (
    <Card className="shadow-sm flex-1 flex flex-col min-h-[200px] border-2 border-purple-500">
      <div className="p-4 flex flex-col h-full">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <Lightbulb className="w-5 h-5 text-yellow-500" />
            <h3 className="text-lg font-bold text-gray-900 dark:text-white">Strategic Direction ({keyQuestions?.length || 0} questions)</h3>
          </div>
          <Badge variant="secondary" className="bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300">
            <TrendingUp className="w-3 h-3 mr-1" />
            {Math.round(confidence * 100)}%
          </Badge>
        </div>

        {/* Main direction */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
          className="mb-4 p-3 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 rounded-lg border border-blue-200 dark:border-blue-800"
        >
          <p className="text-base font-semibold text-gray-900 dark:text-white leading-relaxed">
            {direction}
          </p>
        </motion.div>

        {/* Key questions */}
        {keyQuestions.length > 0 && (
          <div className="mb-4 flex-1 overflow-y-auto">
            <div className="flex items-center gap-2 mb-2">
              <HelpCircle className="w-4 h-4 text-purple-500" />
              <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300">
                Key Questions to Ask
              </h4>
            </div>
            <ul className="space-y-3">
              {keyQuestions.map((question, index) => {
                const isObject = typeof question === 'object' && question !== null;
                const primaryText = isObject ? (question as GuidanceQuestion).primary : question;
                const alternatives = isObject ? (question as GuidanceQuestion).alternatives : undefined;
                const context = isObject ? (question as GuidanceQuestion).context : undefined;
                const hasAlternatives = alternatives && alternatives.length > 0;
                const isExpanded = expandedQuestion === index;

                return (
                  <motion.li
                    key={index}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.4, delay: index * 0.1 }}
                    className="border-l-2 border-purple-400 pl-3"
                  >
                    <div className="flex items-start gap-2 p-2 rounded-md hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
                      <span className="text-purple-500 font-bold flex-shrink-0 mt-0.5">?</span>
                      <div className="flex-1">
                        <p className="text-sm font-medium text-gray-800 dark:text-gray-200 leading-relaxed">
                          {primaryText}
                        </p>

                        {/* Show alternatives if available */}
                        {hasAlternatives && (
                          <div className="mt-2">
                            <button
                              onClick={() => setExpandedQuestion(isExpanded ? null : index)}
                              className="text-xs text-purple-600 hover:text-purple-700 dark:text-purple-400 dark:hover:text-purple-300 flex items-center gap-1 font-medium transition-colors"
                            >
                              {isExpanded ? (
                                <ChevronDown className="w-3 h-3" />
                              ) : (
                                <ChevronRight className="w-3 h-3" />
                              )}
                              {alternatives.length} alternative {alternatives.length === 1 ? 'approach' : 'approaches'}
                            </button>

                            {isExpanded && (
                              <motion.div
                                initial={{ opacity: 0, height: 0 }}
                                animate={{ opacity: 1, height: 'auto' }}
                                exit={{ opacity: 0, height: 0 }}
                                transition={{ duration: 0.2 }}
                                className="mt-2 space-y-2 pl-4 border-l-2 border-gray-300 dark:border-gray-700"
                              >
                                {alternatives.map((alt, altIndex) => (
                                  <div
                                    key={altIndex}
                                    className="text-sm text-gray-700 dark:text-gray-300 leading-relaxed"
                                  >
                                    <span className="text-gray-400 dark:text-gray-600 mr-2">•</span>
                                    {alt}
                                  </div>
                                ))}
                                {context && (
                                  <div className="text-xs italic text-gray-500 dark:text-gray-400 mt-2 bg-gray-50 dark:bg-gray-800/50 p-2 rounded">
                                    <span className="font-semibold not-italic">💡 Context:</span> {context}
                                  </div>
                                )}
                              </motion.div>
                            )}
                          </div>
                        )}
                      </div>
                    </div>
                  </motion.li>
                );
              })}
            </ul>
          </div>
        )}

        {/* Talking points */}
        {talkingPoints.length > 0 && (
          <div className="border-t border-gray-200 dark:border-gray-700 pt-3">
            <div className="flex items-center gap-2 mb-2">
              <MessageSquare className="w-4 h-4 text-green-500" />
              <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300">
                Talking Points
              </h4>
            </div>
            <ul className="space-y-1.5">
              {talkingPoints.map((point, index) => (
                <motion.li
                  key={index}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.4, delay: index * 0.1 }}
                  className="flex items-start gap-2"
                >
                  <span className="text-green-500 flex-shrink-0">•</span>
                  <p className="text-sm text-gray-700 dark:text-gray-300">
                    {point}
                  </p>
                </motion.li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </Card>
  );
};
