import React from 'react';

interface SakinahHeaderProps {
  title?: string;
  subtitle?: string;
  onBack?: () => void;
}

export const SakinahHeader: React.FC<SakinahHeaderProps> = ({ 
  title = 'Sakinah', 
  subtitle = 'NEXUS INTELLIGENCE SYSTEM',
  onBack 
}) => {
  return (
    <header className="flex items-center gap-3 py-2 mb-6">
      {onBack && (
        <button 
          onClick={onBack}
          className="w-[34px] h-[34px] rounded-full border border-[rgba(212,168,83,0.16)] bg-transparent text-[#D4A853] flex items-center justify-center cursor-pointer shrink-0"
        >
          {/* Simple back icon representation */}
          <span className="text-sm">←</span>
        </button>
      )}
      <div>
        <h1 className="font-serif text-[22px] font-medium text-[#EDE7DA] leading-none">{title}</h1>
        <p className="font-mono text-[9px] tracking-[0.2em] uppercase text-[#5f6675] mt-1">{subtitle}</p>
      </div>
    </header>
  );
};
