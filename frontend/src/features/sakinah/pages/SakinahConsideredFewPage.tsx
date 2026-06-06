import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  SakinahShell, 
  SakinahHeader, 
  ConsideredFewList, 
  EmptyMatchState, 
  RayaScriptCard 
} from '../components';
import type { ConsideredFewResponse } from '../types/sakinah.types';
import { getConsideredFew } from '../services/sakinahApi';
import { mockCandidates } from '../data/mockSakinahData';

export const SakinahConsideredFewPage: React.FC = () => {
  const [response, setResponse] = useState<ConsideredFewResponse | null>(null);
  const [isOfflineFallback, setIsOfflineFallback] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    getConsideredFew()
      .then(setResponse)
      .catch((err) => {
        console.warn('Backend offline, using dev fallback for SakinahConsideredFew', err);
        setIsOfflineFallback(true);
        setResponse({ status: 'FOUND', candidates: mockCandidates });
      });
  }, []);

  const handleSelectCandidate = (candidateId: string) => {
    navigate(`/sakinah/candidate/${candidateId}`);
  };

  if (!response) {
    return <SakinahShell><div className="p-4 text-center">Loading considered few...</div></SakinahShell>;
  }

  return (
    <SakinahShell>
      <SakinahHeader title="Considered Few" subtitle="ALIGNED CANDIDATES" />

      <main className="mt-6 flex flex-col gap-6">
        <RayaScriptCard 
          scriptText="I have reviewed your signals alongside others. Rather than showing you many incompatible profiles, I have brought forward only those who share your core values. Take your time."
          className="mb-2"
        />

        {isOfflineFallback && (
          <div className="bg-[#D4A853]/10 border border-[#D4A853]/30 rounded-[12px] p-3 text-center text-[12px] text-[#D4A853]">
            [Dev Fallback: Backend unreachable. Showing mock candidates.]
          </div>
        )}

        {response.status === 'NO_SUITABLE_MATCHES_RIGHT_NOW' || !response.candidates || response.candidates.length === 0 ? (
          <EmptyMatchState />
        ) : (
          <ConsideredFewList 
            candidates={response.candidates} 
            onSelectCandidate={handleSelectCandidate} 
          />
        )}
      </main>
    </SakinahShell>
  );
};
