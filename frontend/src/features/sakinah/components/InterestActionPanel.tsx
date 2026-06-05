import React from 'react';

interface InterestActionPanelProps {
  onExpressInterest: () => void;
  onSilentPass: () => void;
  isPending?: boolean;
}

export const InterestActionPanel: React.FC<InterestActionPanelProps> = ({ 
  onExpressInterest, 
  onSilentPass,
  isPending = false
}) => {
  return (
    <div className="mt-8 pt-6 border-t border-[rgba(255,255,255,0.06)] flex flex-col gap-4">
      <p className="text-center text-[12px] text-[#9aa0ac] font-light mb-2">
        If you feel aligned with their values, express your interest. They will not see this unless they also express interest.
      </p>
      <button 
        onClick={onExpressInterest}
        disabled={isPending}
        className="w-full py-[16px] rounded-[14px] bg-[#D4A853] text-[#07090f] font-serif font-medium text-[20px] transition-opacity disabled:opacity-50 hover:opacity-90"
      >
        {isPending ? 'Processing...' : 'Express Interest'}
      </button>
      <button 
        onClick={onSilentPass}
        disabled={isPending}
        className="w-full py-[14px] rounded-[14px] border border-[rgba(255,255,255,0.1)] text-[#9aa0ac] font-sans text-[14px] font-medium transition-colors hover:bg-[rgba(255,255,255,0.02)] hover:text-[#EDE7DA] disabled:opacity-50"
      >
        Silent Pass
      </button>
    </div>
  );
};
