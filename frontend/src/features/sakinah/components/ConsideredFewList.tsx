import React from 'react';
import { CandidateSummary } from '../types/sakinah.types';

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
        <div 
          key={cand.candidateId}
          onClick={() => onSelectCandidate(cand.candidateId)}
          className="relative border border-[rgba(255,255,255,0.06)] rounded-[20px] p-[20px] cursor-pointer transition-transform duration-[0.24s] hover:border-[#D4A853] hover:-translate-y-[2px] hover:bg-[rgba(212,168,83,0.04)]"
        >
          <div className="font-serif text-[28px] text-[#D4A853] mb-[6px]">{cand.displayName}</div>
          <h3 className="font-serif font-medium text-[21px] mb-[5px] text-[#EDE7DA]">{cand.profession}</h3>
          <p className="text-[12px] text-[#9aa0ac] font-light leading-[1.5]">
            {cand.age} • {cand.location} • {cand.sect}
          </p>
          <div className="absolute top-[22px] right-[20px] text-[#5f6675] text-[20px]">
            →
          </div>
        </div>
      ))}
    </div>
  );
};
