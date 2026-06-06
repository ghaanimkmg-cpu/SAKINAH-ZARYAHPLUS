import React from 'react';
import { 
  SakinahShell, 
  SakinahHeader, 
  CandidatePortraitCard, 
  InterestActionPanel, 
  RayaScriptCard,
  MatchflowStepper
} from '../components';
import { mockCandidates } from '../data/mockSakinahData';
import { expressInterest, silentPass } from '../services/sakinahApi';

export const SakinahCandidatePage: React.FC = () => {
  // Mock data usage
  const candidate = mockCandidates[0];

  return (
    <SakinahShell>
      <SakinahHeader title={candidate.displayName} subtitle="CANDIDATE PROFILE" onBack={() => console.log('Go back')} />

      <main className="mt-6 flex flex-col gap-6">
        <MatchflowStepper currentStep="VIEWING_CANDIDATE" className="mb-2" />

        <CandidatePortraitCard candidate={candidate} />

        <div className="bg-[#111826] border border-[rgba(255,255,255,0.06)] rounded-[22px] p-5 space-y-4">
          <div>
            <h4 className="font-mono text-[10px] tracking-[0.15em] uppercase text-[#D4A853] mb-2">Shared Strengths</h4>
            <ul className="text-[13.5px] font-light text-[#EDE7DA] space-y-2 list-disc list-inside">
              <li>Both prioritize regular daily prayers.</li>
              <li>Aligned on timeline to marry (1 year).</li>
              <li>Family-oriented values match.</li>
            </ul>
          </div>
          <div className="border-t border-[rgba(255,255,255,0.06)] pt-4">
            <h4 className="font-mono text-[10px] tracking-[0.15em] uppercase text-[#D4A853] mb-2">Gentle Discussion Point</h4>
            <p className="text-[13.5px] font-light text-[#9aa0ac]">
              They are open to relocating, while you preferred to stay local. This might be worth exploring respectfully.
            </p>
          </div>
        </div>

        <RayaScriptCard 
          scriptText={`I noticed a strong alignment in your spiritual practices. ${candidate.displayName} also shares your deep appreciation for family.`}
          className="my-2"
        />

        <InterestActionPanel 
          onExpressInterest={() => {
            expressInterest(candidate.candidateId).then(() => console.log('Expressed Interest')).catch(console.error);
          }} 
          onSilentPass={() => {
            silentPass(candidate.candidateId).then(() => console.log('Silently Passed')).catch(console.error);
          }} 
        />
      </main>
    </SakinahShell>
  );
};
