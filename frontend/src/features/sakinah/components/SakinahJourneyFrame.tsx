import React from 'react';

interface SakinahJourneyFrameProps {
  children: React.ReactNode;
  leftRail?: React.ReactNode;
  rightRail?: React.ReactNode;
}

export const SakinahJourneyFrame: React.FC<SakinahJourneyFrameProps> = ({ 
  children, 
  leftRail, 
  rightRail 
}) => {
  return (
    <div className="sk-viewport pb-0 pt-0 sm:pt-6">
      {/* Container simulating .deck from dev reference */}
      <div className="flex justify-center items-start gap-12 max-w-[1560px] mx-auto w-full px-0 sm:px-6 h-full">
        
        {/* Left Rail (Desktop only) */}
        {leftRail && (
          <aside className="hidden lg:block w-[312px] flex-shrink-0 pt-2 shrink-0">
            {leftRail}
          </aside>
        )}

        {/* Center Phone (The main interactive area) */}
        <div className="w-full sm:w-[392px] max-w-full sm:h-[846px] max-h-[100dvh] bg-[linear-gradient(180deg,var(--sk-bg2),#070a10)] sm:border sm:border-[var(--sk-line)] sm:rounded-[46px] sm:shadow-[var(--sk-shadow),0_0_0_9px_#04060a,0_0_0_10px_rgba(212,168,83,0.1)] relative overflow-hidden flex flex-col shrink-0">
          
          {/* Simulated hardware notch & status bar (only visible on desktop wrapper) */}
          <div className="hidden sm:block absolute top-0 left-1/2 -translate-x-1/2 w-[128px] h-[26px] bg-[#04060a] rounded-b-[18px] z-[60]" />
          <div className="hidden sm:flex h-[42px] items-center justify-between px-[26px] text-[12px] text-[var(--sk-ink-dim)] shrink-0 z-[50]">
            <span>9:41</span>
            <span className="font-serif text-[13px] text-[var(--sk-gold-dim)]">سكينة</span>
            <div className="flex gap-[5px] items-center">
              <span className="w-[5px] h-[5px] rounded-full bg-[var(--sk-gold-dim)]" />
              <span className="w-[5px] h-[5px] rounded-full bg-[var(--sk-gold-dim)]" />
              <span className="w-[5px] h-[5px] rounded-full bg-[var(--sk-gold-dim)]" />
              <span className="ml-1">5G</span>
            </div>
          </div>

          {/* Viewport for screens */}
          <div className="flex-1 relative overflow-hidden h-full">
            {/* Inner scroll container matching .screen */}
            <div className="absolute inset-0 overflow-y-auto px-[22px] pt-6 pb-[120px] scrollbar-hide">
              {children}
            </div>
          </div>
        </div>

        {/* Right Rail (Desktop only, mostly for notes) */}
        {rightRail && (
          <aside className="hidden xl:block w-[344px] flex-shrink-0 pt-2 shrink-0">
            {rightRail}
          </aside>
        )}
      </div>
    </div>
  );
};
