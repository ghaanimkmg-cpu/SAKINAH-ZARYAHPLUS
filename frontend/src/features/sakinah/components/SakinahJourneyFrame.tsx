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
    <div className="sk-viewport pb-0 pt-0 sm:pt-8">
      {/* Container simulating a proper web app layout, not a phone deck */}
      <div className="flex justify-center items-start gap-8 xl:gap-12 max-w-6xl mx-auto w-full px-0 sm:px-6 h-full flex-1">
        
        {/* Left Rail (Desktop only) */}
        {leftRail && (
          <aside className="hidden lg:block w-[280px] xl:w-[312px] flex-shrink-0 pt-2 shrink-0">
            {leftRail}
          </aside>
        )}

        {/* Main Content Area */}
        <div className="w-full lg:max-w-[700px] xl:max-w-[800px] flex-1 bg-transparent sm:bg-[linear-gradient(180deg,var(--sk-bg2),#070a10)] sm:border sm:border-[rgba(255,255,255,0.04)] sm:rounded-[32px] sm:shadow-[var(--sk-shadow)] relative flex flex-col shrink-0 min-h-[100dvh] sm:min-h-[calc(100vh-6rem)] sm:mb-12">
          
          {/* Viewport for screens */}
          <div className="flex-1 relative h-full">
            <div className="inset-0 px-[22px] sm:px-[48px] lg:px-[64px] pt-6 sm:pt-10 pb-[120px]">
              {children}
            </div>
          </div>
        </div>

        {/* Right Rail (Desktop only) */}
        {rightRail && (
          <aside className="hidden xl:block w-[300px] flex-shrink-0 pt-2 shrink-0">
            {rightRail}
          </aside>
        )}
      </div>
    </div>
  );
};
