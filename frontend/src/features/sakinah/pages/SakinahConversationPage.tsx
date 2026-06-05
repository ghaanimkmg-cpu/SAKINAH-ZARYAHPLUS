import React from 'react';
import { 
  SakinahShell, 
  SakinahHeader, 
  ConversationTopicList, 
  ConversationMessageList,
  SafetyNotice,
  RayaScriptCard
} from '../components';
import { ConversationTopic } from '../types/sakinah.types';

export const SakinahConversationPage: React.FC = () => {
  // Hardcoded standard topics reflecting the safe, structured curriculum.
  // Note: No intimacy/closeness topic is present before nikah.
  const topics: ConversationTopic[] = [
    { id: 't1', title: 'Parents & Family', description: 'Upbringing, boundaries, and care for parents.', isUnlocked: true },
    { id: 't2', title: 'Work', description: 'Career ambitions, work-life balance.', isUnlocked: false, unlockRequirement: 'Complete Parents & Family' },
    { id: 't3', title: 'Friends', description: 'Social circles and boundaries.', isUnlocked: false, unlockRequirement: 'Complete Work' },
    { id: 't4', title: 'Habits', description: 'Daily routines, free time, screen time.', isUnlocked: false, unlockRequirement: 'Complete Friends' },
    { id: 't5', title: 'Self-image', description: 'Personal growth and deen journey.', isUnlocked: false, unlockRequirement: 'Complete Habits' },
    { id: 't6', title: 'Responsibility', description: 'Household roles and expectations.', isUnlocked: false, unlockRequirement: 'Complete Self-image' },
    { id: 't7', title: 'Expectations', description: 'What you expect from a spouse.', isUnlocked: false, unlockRequirement: 'Complete Responsibility' },
    { id: 't8', title: 'Finances', description: 'Saving, spending, and financial views.', isUnlocked: false, unlockRequirement: 'Complete Expectations' },
  ];

  return (
    <SakinahShell>
      <SakinahHeader title="Structured Conversation" subtitle="DISCUSSION TOPICS" onBack={() => window.history.back()} />

      <main className="mt-6 flex flex-col gap-6">
        <SafetyNotice message="For your protection, keep all communication within Sakinah until marriage is agreed upon. Do not share your private contact information." />

        <RayaScriptCard 
          scriptText="I have unlocked the first topic for you both. Explore 'Parents & Family'. Once you both feel understood, the next topic will open."
        />

        <div className="mt-4 border-t border-[rgba(255,255,255,0.06)] pt-6">
          <h3 className="font-serif text-[21px] text-[#EDE7DA] mb-4">Curriculum</h3>
          <ConversationTopicList topics={topics} />
        </div>
      </main>
    </SakinahShell>
  );
};
