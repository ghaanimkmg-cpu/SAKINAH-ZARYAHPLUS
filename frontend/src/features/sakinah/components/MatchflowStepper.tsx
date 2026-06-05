import React from 'react';
import { MatchflowStep } from '../types/sakinah.types';

interface MatchflowStepperProps {
  currentStep: MatchflowStep;
  className?: string;
}

export const MatchflowStepper: React.FC<MatchflowStepperProps> = ({ currentStep, className = '' }) => {
  const steps: { key: MatchflowStep; label: string; desc: string }[] = [
    { key: 'VIEWING_CANDIDATE', label: 'View Profile', desc: 'Read their signals safely.' },
    { key: 'MUTUAL_INTEREST_PENDING', label: 'Mutual Interest', desc: 'Awaiting alignment.' },
    { key: 'CONVERSATION_OPEN', label: 'Structured Chat', desc: 'Unlock topics progressively.' },
    { key: 'DECISION_PENDING', label: 'Final Decision', desc: 'Proceed or part ways.' }
  ];

  const currentIndex = steps.findIndex(s => s.key === currentStep);

  return (
    <div className={`mt-[26px] ${className}`}>
      {steps.map((step, index) => {
        const isActive = index <= currentIndex;
        return (
          <div key={step.key} className={`flex gap-[12px] items-start p-[9px_11px] rounded-[11px] transition-[0.18s] mb-[3px] ${isActive ? 'bg-[rgba(212,168,83,0.08)] shadow-[inset_0_0_0_1px_rgba(212,168,83,0.16)]' : 'hover:bg-[rgba(212,168,83,0.05)]'}`}>
            <div className={`w-[22px] h-[22px] rounded-[6px] border flex items-center justify-center font-mono text-[10px] shrink-0 mt-[1px] ${isActive ? 'bg-[#D4A853] text-[#0a0e15] border-[#D4A853]' : 'border-[rgba(212,168,83,0.16)] text-[#5f6675]'}`}>
              {index + 1}
            </div>
            <div>
              <div className={`text-[13.5px] font-medium leading-[1.25] ${isActive ? 'text-[#e7c984]' : 'text-[#9aa0ac]'}`}>
                {step.label}
              </div>
              <div className="text-[11px] text-[#5f6675] font-light mt-[2px] leading-[1.3]">
                {step.desc}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};
