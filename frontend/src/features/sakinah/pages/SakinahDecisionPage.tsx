import React from 'react';
import { SakinahShell, SakinahHeader } from '../components';

export const SakinahDecisionPage: React.FC = () => {
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

        <div className="mt-8 flex flex-col gap-4">
          <button className="w-full py-[16px] rounded-[14px] bg-[#D4A853] text-[#07090f] font-serif font-medium text-[20px] transition-opacity hover:opacity-90">
            PROCEED
          </button>
          
          <button className="w-full py-[16px] rounded-[14px] border border-[rgba(255,255,255,0.1)] text-[#e7c984] font-serif font-medium text-[20px] transition-colors hover:bg-[rgba(212,168,83,0.05)] hover:border-[#D4A853]">
            PAUSE
          </button>

          <button className="w-full py-[16px] rounded-[14px] border border-[rgba(255,255,255,0.1)] text-[#C98A8A] font-serif font-medium text-[20px] transition-colors hover:bg-[rgba(201,138,138,0.1)] hover:border-[rgba(201,138,138,0.3)]">
            CLOSE
          </button>
        </div>
      </main>
    </SakinahShell>
  );
};
