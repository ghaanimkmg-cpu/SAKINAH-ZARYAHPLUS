import React, { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { SakinahShell, SakinahHeader, DevFallbackBadge, SakinahButton } from '../components';
import { submitDecision } from '../services/sakinahApi';
import type { DecisionOutcome } from '../types/sakinah.types';

export const SakinahDecisionPage: React.FC = () => {
  const navigate = useNavigate();
  const { matchflowId } = useParams();
  const [isPending, setIsPending] = useState(false);
  const [errorFallback, setErrorFallback] = useState('');

  const handleDecision = async (decision: DecisionOutcome) => {
    setIsPending(true);
    setErrorFallback('');
    try {
      await submitDecision(matchflowId || 'mock', decision);
      navigate('/sakinah/considered-few');
    } catch (err) {
      console.warn('Backend offline, using dev fallback for submitDecision', err);
      setErrorFallback(`Backend unreachable. Dev Fallback: Decision '${decision}' processed.`);
      setTimeout(() => navigate('/sakinah/considered-few'), 1500);
    } finally {
      setIsPending(false);
    }
  };

  return (
    <SakinahShell>
      <SakinahHeader title="Final Choice" subtitle="DECISION PENDING" onBack={() => window.history.back()} />

      <main className="mt-6 flex flex-col gap-6 text-center">
        <div className="relative w-[80px] h-[80px] mx-auto rounded-full border border-[rgba(212,168,83,0.16)] flex items-center justify-center mb-2 shadow-[0_0_20px_rgba(212,168,83,0.05)]">
          <div className="absolute inset-0 bg-[#D4A853] rounded-full opacity-5"></div>
          <span className="font-serif text-[32px] text-[#D4A853]">⚖️</span>
        </div>

        <h2 className="font-serif text-[26px] font-medium text-[#EDE7DA]">
          It is time to decide.
        </h2>
        
        <p className="text-[14px] font-light text-[#9aa0ac] leading-[1.6]">
          You have completed the structured conversation. How would you like to proceed? Make this choice with sincerity and intention. No one will pressure you.
        </p>

        {errorFallback && <DevFallbackBadge message={errorFallback} />}

        <div className="mt-8 flex flex-col gap-4">
          <SakinahButton 
            onClick={() => handleDecision('PROCEED')}
            disabled={isPending}
            size="lg"
          >
            PROCEED
          </SakinahButton>
          
          <SakinahButton 
            variant="secondary"
            onClick={() => handleDecision('NOT_SURE_YET')} 
            disabled={isPending}
            size="lg"
          >
            PAUSE
          </SakinahButton>

          <SakinahButton 
            variant="danger"
            onClick={() => handleDecision('SILENT_PASS')} 
            disabled={isPending}
            size="lg"
          >
            CLOSE
          </SakinahButton>
        </div>
      </main>
    </SakinahShell>
  );
};
