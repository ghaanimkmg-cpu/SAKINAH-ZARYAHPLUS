import React, { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { SakinahShell, SakinahHeader, DevFallbackBadge } from '../components';
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
        <div className="w-[80px] h-[80px] mx-auto rounded-full border border-[rgba(212,168,83,0.16)] flex items-center justify-center mb-2">
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
          <button 
            onClick={() => handleDecision('PROCEED')}
            disabled={isPending}
            className="w-full py-[16px] rounded-[14px] bg-[#D4A853] text-[#07090f] font-serif font-medium text-[20px] transition-opacity hover:opacity-90 disabled:opacity-50"
          >
            PROCEED
          </button>
          
          <button 
            onClick={() => handleDecision('NOT_SURE_YET')} // Note: the type says NOT_SURE_YET for pause
            disabled={isPending}
            className="w-full py-[16px] rounded-[14px] border border-[rgba(255,255,255,0.1)] text-[#e7c984] font-serif font-medium text-[20px] transition-colors hover:bg-[rgba(212,168,83,0.05)] hover:border-[#D4A853] disabled:opacity-50"
          >
            PAUSE
          </button>

          <button 
            onClick={() => handleDecision('SILENT_PASS')} // Note: the type says SILENT_PASS for close
            disabled={isPending}
            className="w-full py-[16px] rounded-[14px] border border-[rgba(255,255,255,0.1)] text-[#C98A8A] font-serif font-medium text-[20px] transition-colors hover:bg-[rgba(201,138,138,0.1)] hover:border-[rgba(201,138,138,0.3)] disabled:opacity-50"
          >
            CLOSE
          </button>
        </div>
      </main>
    </SakinahShell>
  );
};
