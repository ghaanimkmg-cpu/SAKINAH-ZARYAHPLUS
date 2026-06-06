import React, { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { 
  SakinahShell, 
  SakinahHeader, 
  ConversationTopicList, 
  SafetyNotice,
  RayaScriptCard,
  SakinahCard,
  SakinahButton,
  SakinahInput
} from '../components';
import type { ConversationTopic } from '../types/sakinah.types';
import { sendConversationMessage } from '../services/sakinahApi';

export const SakinahConversationPage: React.FC = () => {
  const navigate = useNavigate();
  const { conversationId } = useParams();
  const [messages, setMessages] = useState<{sender: string, text: string}[]>([]);
  const [inputText, setInputText] = useState('');
  const [inputError, setInputError] = useState('');
  const [isPending, setIsPending] = useState(false);
  const [contactWarning, setContactWarning] = useState(false);

  const topics: ConversationTopic[] = [
    { id: 't1', title: 'Parents & Family', description: 'Upbringing, boundaries, and care for parents.', isUnlocked: true },
    { id: 't2', title: 'Work', description: 'Career ambitions, work-life balance.', isUnlocked: false, unlockRequirement: 'Complete Parents & Family' },
    { id: 't3', title: 'Friends', description: 'Social circles and boundaries.', isUnlocked: false, unlockRequirement: 'Complete Work' },
    { id: 't4', title: 'Habits', description: 'Daily routines, free time, screen time.', isUnlocked: false, unlockRequirement: 'Complete Friends' },
  ];

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    setInputError('');

    if (!inputText.trim()) {
      setInputError('Message cannot be empty.');
      return;
    }

    // Contact leak detection simulation
    if (inputText.includes('@') || inputText.match(/\d{5,}/)) {
      setContactWarning(true);
      setTimeout(() => setContactWarning(false), 5000);
      return;
    }

    setIsPending(true);
    try {
      await sendConversationMessage(conversationId || 'mock', 't1', inputText);
      setMessages([...messages, { sender: 'You', text: inputText }]);
      setInputText('');
    } catch (err) {
      console.warn('Backend offline, using dev fallback for sendMessage', err);
      // Dev fallback: just add to UI
      setMessages([...messages, { sender: 'You', text: inputText }, { sender: 'System', text: 'Development Preview Mode: Message received safely.' }]);
      setInputText('');
    } finally {
      setIsPending(false);
    }
  };

  return (
    <SakinahShell>
      <SakinahHeader title="Structured Conversation" subtitle="DISCUSSION TOPICS" onBack={() => window.history.back()} />

      <main className="mt-6 flex flex-col gap-6">
        <SafetyNotice message="For your protection, keep all communication within Sakinah until marriage is agreed upon. Do not share your private contact information." />

        {contactWarning && (
          <div className="bg-red-500/10 border border-red-500/30 rounded-[12px] p-3 text-center text-[12px] text-red-400">
            [Safety System]: Sharing contact info is disabled. Please continue discussing the topic.
          </div>
        )}

        <RayaScriptCard 
          scriptText="I have unlocked the first topic for you both. Explore 'Parents & Family'. Once you both feel understood, the next topic will open."
        />

        <div className="mt-4 border-t border-[rgba(255,255,255,0.06)] pt-6">
          <h3 className="font-serif text-[21px] text-[#EDE7DA] mb-4">Chat: Parents & Family</h3>
          
          <SakinahCard padding="sm" className="h-48 overflow-y-auto flex flex-col gap-2 mb-4">
            {messages.length === 0 ? (
              <p className="text-[#5f6675] text-[13px] text-center mt-auto mb-auto">Start the discussion...</p>
            ) : (
              messages.map((m, i) => (
                <div key={i} className={`p-3 rounded-[12px] text-[13px] max-w-[80%] ${m.sender === 'You' ? 'bg-[#D4A853]/20 text-[#EDE7DA] self-end border border-[#D4A853]/20' : 'bg-[rgba(255,255,255,0.05)] text-[#9aa0ac] self-start border border-[rgba(255,255,255,0.05)]'}`}>
                  <strong>{m.sender}: </strong>{m.text}
                </div>
              ))
            )}
          </SakinahCard>

          <form onSubmit={handleSendMessage} className="flex gap-2 items-start mb-6" noValidate>
            <SakinahInput 
              type="text" 
              value={inputText}
              onChange={(e) => { setInputText(e.target.value); setInputError(''); }}
              placeholder="Type your message..."
              className="flex-1"
              required
              error={inputError}
            />
            <SakinahButton 
              type="submit" 
              disabled={isPending}
              fullWidth={false}
              className="h-[52px]"
            >
              Send
            </SakinahButton>
          </form>

          <h3 className="font-serif text-[21px] text-[#EDE7DA] mb-4">Curriculum</h3>
          <ConversationTopicList topics={topics} />
        </div>

        <SakinahButton 
          variant="secondary"
          onClick={() => navigate('/sakinah/decision/mock_matchflow_1')}
          size="lg"
        >
          Make a Decision
        </SakinahButton>
      </main>
    </SakinahShell>
  );
};
