import React, { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
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
  const navigate = useNavigate();
  const { candidateId } = useParams();
  const [isPending, setIsPending] = useState(false);
  const [errorFallback, setErrorFallback] = useState('');

  // Fallback to mock for now if not fetched via API
  const candidate = mockCandidates.find(c => c.candidateId === candidateId) || mockCandidates[0];

  const handleExpressInterest = async () => {
    setIsPending(true);
    setErrorFallback('');
    try {
      await expressInterest(candidate.candidateId);
      // Assuming mutual interest for dev flow preview
      navigate('/sakinah/matchflow/mock_matchflow_1');
    } catch (err) {
      console.warn('Backend offline, using dev fallback for expressInterest', err);
      setErrorFallback('Backend unreachable. Proceeding in Development Preview Mode.');
      setTimeout(() => navigate('/sakinah/matchflow/mock_matchflow_1'), 1000);
    } finally {
      setIsPending(false);
    }
  };

  const handleSilentPass = async () => {
    setIsPending(true);
    setErrorFallback('');
    try {
      await silentPass(candidate.candidateId);
      navigate('/sakinah/considered-few');
    } catch (err) {
      console.warn('Backend offline, using dev fallback for silentPass', err);
      setErrorFallback('Backend unreachable. Proceeding in Development Preview Mode.');
      setTimeout(() => navigate('/sakinah/considered-few'), 1000);
    } finally {
      setIsPending(false);
    }
  };

  return (
    <SakinahShell>
      <SakinahHeader title={candidate.displayName} subtitle="CANDIDATE PROFILE" onBack={() => navigate('/sakinah/considered-few')} />

      <main className="mt-6 flex flex-col gap-6">
        <MatchflowStepper currentStep="VIEWING_CANDIDATE" className="mb-2" />

        {errorFallback && (
          <div className="bg-[#D4A853]/10 border border-[#D4A853]/30 rounded-[12px] p-3 text-center text-[12px] text-[#D4A853]">
            {errorFallback}
          </div>
        )}

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
          onExpressInterest={handleExpressInterest} 
          onSilentPass={handleSilentPass} 
        />
      </main>
    </SakinahShell>
  );
};
