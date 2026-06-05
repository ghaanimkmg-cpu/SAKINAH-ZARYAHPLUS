import React from 'react';
import { ConversationTopic } from '../../types/sakinah.types';

interface ConversationTopicListProps {
  topics: ConversationTopic[];
  onSelectTopic?: (topicId: string) => void;
  className?: string;
}

export const ConversationTopicList: React.FC<ConversationTopicListProps> = ({ topics, onSelectTopic, className = '' }) => {
  return (
    <div className={`space-y-[13px] ${className}`}>
      {topics.map(topic => (
        <div 
          key={topic.id}
          onClick={() => topic.isUnlocked && onSelectTopic && onSelectTopic(topic.id)}
          className={`border rounded-[20px] p-[20px] relative transition-[0.24s] ${topic.isUnlocked ? 'border-[rgba(255,255,255,0.06)] cursor-pointer hover:border-[#D4A853] hover:-translate-y-[2px] hover:bg-[rgba(212,168,83,0.04)]' : 'border-[rgba(255,255,255,0.02)] opacity-60 cursor-not-allowed bg-[rgba(0,0,0,0.2)]'}`}
        >
          <div className="font-serif text-[28px] text-[#D4A853] mb-[6px]">{topic.title}</div>
          <p className="text-[12px] text-[#9aa0ac] font-light leading-[1.5]">
            {topic.description}
          </p>
          {!topic.isUnlocked && topic.unlockRequirement && (
            <div className="mt-4 font-mono text-[9px] tracking-[0.16em] uppercase text-[#C98A8A]">
              🔒 {topic.unlockRequirement}
            </div>
          )}
          {topic.isUnlocked && (
            <div className="absolute top-[22px] right-[20px] text-[#5f6675] text-[20px]">
              →
            </div>
          )}
        </div>
      ))}
    </div>
  );
};
