import React, { useEffect, useState } from 'react';
import { 
  SakinahShell, 
  SakinahHeader, 
  ConsideredFewList, 
  EmptyMatchState, 
  RayaScriptCard 
} from '../components';
import { ConsideredFewResponse } from '../types/sakinah.types';
import { getConsideredFew } from '../services/sakinahApi';

export const SakinahConsideredFewPage: React.FC = () => {
  const [response, setResponse] = useState<ConsideredFewResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getConsideredFew()
      .then(setResponse)
      .catch((err) => setError(err.message));
  }, []);

  const handleSelectCandidate = (candidateId: string) => {
    // Navigation logic goes here eventually
    console.log(`Navigate to candidate ${candidateId}`);
  };

  if (error) {
    return <SakinahShell><div className="text-red-500">Error: {error}</div></SakinahShell>;
  }

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

        {response.status === 'NO_SUITABLE_MATCHES_RIGHT_NOW' || response.candidates.length === 0 ? (
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
