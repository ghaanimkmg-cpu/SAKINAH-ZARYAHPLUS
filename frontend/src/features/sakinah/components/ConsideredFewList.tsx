import React from 'react';
import type { CandidateSummary } from '../types/sakinah.types';
import { SakinahCard } from './SakinahCard';

interface ConsideredFewListProps {
  candidates: CandidateSummary[];
  onSelectCandidate: (id: string) => void;
  className?: string;
}

export const ConsideredFewList: React.FC<ConsideredFewListProps> = ({ candidates, onSelectCandidate, className = '' }) => {
  if (candidates.length === 0) return null;

  return (
    <div className={`space-y-[13px] ${className}`}>
      {candidates.map((cand) => (
        <SakinahCard 
          key={cand.candidateId}
          onClick={() => onSelectCandidate(cand.candidateId)}
          className="relative cursor-pointer transition-transform duration-[0.24s] hover:border-[#D4A853] hover:-translate-y-[2px] hover:bg-[rgba(212,168,83,0.04)] group"
        >
          <div className="font-serif text-[28px] text-[#D4A853] mb-[6px] transition-colors group-hover:text-[#ebd097]">{cand.displayName}</div>
          <h3 className="font-serif font-medium text-[21px] mb-[5px] text-[#EDE7DA]">{cand.profession}</h3>
          <p className="text-[13px] text-[#9aa0ac] font-light leading-[1.5]">
            {cand.age} • {cand.location} • {cand.sect}
          </p>
          <div className="absolute top-1/2 -translate-y-1/2 right-[24px] text-[#5f6675] text-[20px] transition-colors group-hover:text-[#D4A853]">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
              <line x1="5" y1="12" x2="19" y2="12"></line>
              <polyline points="12 5 19 12 12 19"></polyline>
            </svg>
          </div>
        </SakinahCard>
      ))}
    </div>
  );
};
