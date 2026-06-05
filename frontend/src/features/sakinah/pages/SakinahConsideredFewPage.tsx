import React from 'react';
import { 
  SakinahShell, 
  SakinahHeader, 
  ConsideredFewList, 
  EmptyMatchState, 
  RayaScriptCard 
} from '../components';
import { mockConsideredFewResponse, mockNoMatchesResponse } from '../data/mockSakinahData';
import { ConsideredFewResponse } from '../types/sakinah.types';

export const SakinahConsideredFewPage: React.FC = () => {
  // Using mock data. In production, this would be fetched from the backend.
  // Switch between mockConsideredFewResponse and mockNoMatchesResponse to test states.
  const response: ConsideredFewResponse = mockConsideredFewResponse;

  const handleSelectCandidate = (candidateId: string) => {
    // Navigation logic goes here eventually
    console.log(`Navigate to candidate ${candidateId}`);
  };

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
