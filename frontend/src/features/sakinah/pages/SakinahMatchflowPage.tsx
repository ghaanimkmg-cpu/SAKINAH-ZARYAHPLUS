import React from 'react';
import { SakinahShell, SakinahHeader, MatchflowStepper, RayaScriptCard } from '../components';

export const SakinahMatchflowPage: React.FC = () => {
  return (
    <SakinahShell>
      <SakinahHeader title="Match Journey" subtitle="CURRENT STATUS" onBack={() => window.history.back()} />

      <main className="mt-6 flex flex-col gap-6">
        <RayaScriptCard 
          scriptText="The journey to nikah is deliberate. We are currently waiting for mutual alignment before proceeding further. Take your time to reflect."
          className="mb-2"
        />

        {/* The current step is completely controlled by the backend. Frontend only renders it. */}
        <div className="bg-[#111826] border border-[rgba(255,255,255,0.06)] rounded-[22px] p-5">
          <h3 className="font-serif text-[21px] text-[#EDE7DA] mb-2">Current Phase</h3>
          <p className="text-[14px] font-light text-[#9aa0ac] leading-[1.6]">
            Mutual Interest is pending. Both parties must quietly express interest before any conversation opens.
          </p>
          <MatchflowStepper currentStep="MUTUAL_INTEREST_PENDING" />
        </div>
        
      </main>
    </SakinahShell>
  );
};
