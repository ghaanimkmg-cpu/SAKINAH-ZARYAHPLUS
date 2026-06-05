import React from 'react';

interface DecisionPanelProps {
  onProceed: () => void;
  onPartWays: () => void;
  isPending?: boolean;
}

export const DecisionPanel: React.FC<DecisionPanelProps> = ({ onProceed, onPartWays, isPending = false }) => {
  return (
    <div className="mt-8 pt-6 border-t border-[rgba(255,255,255,0.06)] flex flex-col gap-4">
      <div className="text-center mb-2">
        <h3 className="font-serif text-[21px] font-medium text-[#EDE7DA] mb-1">Final Decision</h3>
        <p className="text-[12px] text-[#9aa0ac] font-light leading-[1.5]">
          Make your choice with intention. Once a decision is made, it cannot be reversed.
        </p>
      </div>
      <button 
        onClick={onProceed}
        disabled={isPending}
        className="w-full py-[16px] rounded-[14px] bg-[#D4A853] text-[#07090f] font-serif font-medium text-[20px] transition-opacity disabled:opacity-50 hover:opacity-90"
      >
        {isPending ? 'Processing...' : 'Proceed to Next Phase'}
      </button>
      <button 
        onClick={onPartWays}
        disabled={isPending}
        className="w-full py-[14px] rounded-[14px] border border-[rgba(255,255,255,0.1)] text-[#C98A8A] font-sans text-[14px] font-medium transition-colors hover:bg-[rgba(201,138,138,0.1)] hover:border-[rgba(201,138,138,0.3)] disabled:opacity-50"
      >
        Part Ways Respectfully
      </button>
    </div>
  );
};
