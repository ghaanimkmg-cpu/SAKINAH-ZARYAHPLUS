import React from 'react';
import type { ConversationTopic } from '../types/sakinah.types';
import { SakinahCard } from './SakinahCard';

interface ConversationTopicListProps {
  topics: ConversationTopic[];
  onSelectTopic?: (topicId: string) => void;
  className?: string;
}

export const ConversationTopicList: React.FC<ConversationTopicListProps> = ({ topics, onSelectTopic, className = '' }) => {
  return (
    <div className={`space-y-[13px] ${className}`}>
      {topics.map(topic => (
        <SakinahCard 
          key={topic.id}
          padding="md"
          onClick={() => topic.isUnlocked && onSelectTopic && onSelectTopic(topic.id)}
          className={`relative transition-[0.24s] ${topic.isUnlocked ? 'cursor-pointer hover:border-[#D4A853] hover:-translate-y-[2px] hover:bg-[rgba(212,168,83,0.04)] group' : 'opacity-60 cursor-not-allowed bg-[rgba(0,0,0,0.2)] border-[rgba(255,255,255,0.02)] shadow-none'}`}
        >
          <div className={`font-serif text-[28px] mb-[6px] transition-colors ${topic.isUnlocked ? 'text-[#D4A853] group-hover:text-[#ebd097]' : 'text-[#D4A853]/50'}`}>
            {topic.title}
          </div>
          <p className="text-[13px] text-[#9aa0ac] font-light leading-[1.5]">
            {topic.description}
          </p>
          {!topic.isUnlocked && topic.unlockRequirement && (
            <div className="mt-4 font-mono text-[9px] tracking-[0.16em] uppercase text-[#C98A8A]">
              🔒 {topic.unlockRequirement}
            </div>
          )}
          {topic.isUnlocked && (
            <div className="absolute top-1/2 -translate-y-1/2 right-[24px] text-[#5f6675] text-[20px] transition-colors group-hover:text-[#D4A853]">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                <line x1="5" y1="12" x2="19" y2="12"></line>
                <polyline points="12 5 19 12 12 19"></polyline>
              </svg>
            </div>
          )}
        </SakinahCard>
      ))}
    </div>
  );
};
