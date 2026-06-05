import React from 'react';
import { CandidateSummary } from '../types/sakinah.types';

interface CandidatePortraitCardProps {
  candidate: CandidateSummary;
  className?: string;
}

export const CandidatePortraitCard: React.FC<CandidatePortraitCardProps> = ({ candidate, className = '' }) => {
  return (
    <div className={`rounded-[22px] border border-[rgba(212,168,83,0.16)] bg-gradient-to-br from-[#111826] to-[#0f1521] overflow-hidden ${className}`}>
      {/* Blurred portrait placeholder — as per safety rules, no real photos yet */}
      <div className="h-[280px] w-full bg-[#0a0e15] relative overflow-hidden flex items-center justify-center">
        <div className="absolute inset-0 bg-gradient-to-t from-[#111826] to-transparent z-10" />
        {/* Placeholder silhouette/blur */}
        <div className="w-[120px] h-[120px] rounded-full bg-[rgba(212,168,83,0.05)] blur-md" />
        <p className="absolute z-20 text-[10px] tracking-[0.2em] uppercase text-[rgba(212,168,83,0.4)]">
          Portrait locked until mutual interest
        </p>
      </div>
      
      <div className="p-[20px] pt-[10px]">
        <h3 className="font-serif text-[28px] font-medium text-[#D4A853] mb-[6px]">{candidate.displayName}</h3>
        
        <div className="flex gap-[10px] mb-[16px]">
          <div className="flex-1 border border-[rgba(255,255,255,0.06)] rounded-[14px] p-[12px] text-center bg-[rgba(255,255,255,0.012)]">
            <span className="font-serif text-[18px] text-[#e7c984] block leading-[1.1]">{candidate.age}</span>
            <span className="font-mono text-[9px] tracking-[0.16em] uppercase text-[#5f6675] mt-[4px]">Age</span>
          </div>
          <div className="flex-1 border border-[rgba(255,255,255,0.06)] rounded-[14px] p-[12px] text-center bg-[rgba(255,255,255,0.012)]">
            <span className="font-serif text-[18px] text-[#e7c984] block leading-[1.1] truncate px-1">{candidate.location}</span>
            <span className="font-mono text-[9px] tracking-[0.16em] uppercase text-[#5f6675] mt-[4px]">Location</span>
          </div>
        </div>
        
        <p className="text-[14px] font-light text-[#9aa0ac] leading-[1.5]">
          <span className="text-[#D4A853] font-medium mr-2">Bio</span>
          {candidate.bioSnippet}
        </p>
      </div>
    </div>
  );
};
