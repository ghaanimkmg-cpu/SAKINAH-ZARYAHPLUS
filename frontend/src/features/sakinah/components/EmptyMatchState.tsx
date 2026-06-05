import React from 'react';

export const EmptyMatchState: React.FC = () => {
  return (
    <div className="flex flex-col items-center justify-center text-center py-[60px] px-[20px]">
      <div className="w-[80px] h-[80px] rounded-full border border-[rgba(212,168,83,0.16)] flex items-center justify-center mb-[24px]">
        <span className="font-serif text-[32px] text-[rgba(212,168,83,0.4)]">?</span>
      </div>
      <h2 className="font-serif text-[28px] text-[#EDE7DA] mb-[12px]">No Matches Right Now</h2>
      <p className="text-[14px] text-[#9aa0ac] font-light leading-[1.6] max-w-[280px]">
        We do not have someone suitable enough to show right now. We would rather wait than show the wrong person.
      </p>
    </div>
  );
};
