import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { SakinahShell, SakinahHeader, MatchflowStepper, RayaScriptCard, DevFallbackBadge, SakinahCard, SakinahButton, SakinahLoadingState } from '../components';
import { getMatchflow } from '../services/sakinahApi';
import type { MatchflowResponse } from '../types/sakinah.types';

export const SakinahMatchflowPage: React.FC = () => {
  const navigate = useNavigate();
  const { matchflowId } = useParams();
  const [matchflow, setMatchflow] = useState<MatchflowResponse | null>(null);
  const [isOfflineFallback, setIsOfflineFallback] = useState(false);

  useEffect(() => {
    if (matchflowId) {
      getMatchflow(matchflowId)
        .then(setMatchflow)
        .catch((err) => {
          console.warn('Backend offline, using dev fallback for SakinahMatchflow', err);
          setIsOfflineFallback(true);
          setMatchflow({
            matchflow_id: matchflowId,
            current_step: 'CONVERSATION_OPEN',
            steps: []
          });
        });
    }
  }, [matchflowId]);

  if (!matchflow) {
    return <SakinahLoadingState fullPage message="Loading journey details..." />;
  }

  const isConversationOpen = matchflow.current_step === 'CONVERSATION_OPEN';

  return (
    <SakinahShell>
      <SakinahHeader title="Match Journey" subtitle="CURRENT STATUS" onBack={() => navigate('/sakinah/considered-few')} />

      <main className="mt-6 flex flex-col gap-6">
        <RayaScriptCard 
          scriptText={isConversationOpen ? "The conversation is now open. Approach it with honesty and respect." : "The journey to nikah is deliberate. We are currently waiting for mutual alignment before proceeding further. Take your time to reflect."}
          className="mb-2"
        />

        {isOfflineFallback && <DevFallbackBadge message="Backend unreachable. Proceeding with CONVERSATION_OPEN state." />}

        <SakinahCard padding="md">
          <h3 className="font-serif text-[21px] text-[#EDE7DA] mb-2">Current Phase</h3>
          <p className="text-[14px] font-light text-[#9aa0ac] leading-[1.6]">
            {isConversationOpen 
              ? "Mutual interest confirmed. A structured conversation is now open." 
              : "Mutual Interest is pending. Both parties must quietly express interest before any conversation opens."}
          </p>
          <MatchflowStepper currentStep={matchflow.current_step as any} />
        </SakinahCard>
        
        {isConversationOpen && (
          <SakinahButton 
            onClick={() => navigate('/sakinah/conversation/mock_conversation_1')}
            size="lg"
            className="mt-4"
          >
            Enter Conversation
          </SakinahButton>
        )}

      </main>
    </SakinahShell>
  );
};
