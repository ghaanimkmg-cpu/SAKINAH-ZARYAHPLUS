import React from 'react';

interface SakinahShellProps {
  children: React.ReactNode;
}

export const SakinahShell: React.FC<SakinahShellProps> = ({ children }) => {
  return (
    <div className="min-h-screen bg-[#07090f] text-[#EDE7DA] font-sans px-6 py-8 pb-20 relative overflow-hidden">
      {/* Background radial gradient overlay imitating the HTML reference */}
      <div 
        className="absolute inset-0 pointer-events-none" 
        style={{ background: 'radial-gradient(1200px 800px at 50% -10%, rgba(212,168,83,0.07), transparent 60%)' }}
      />
      <div className="relative z-10 max-w-xl mx-auto h-full">
        {children}
      </div>
    </div>
  );
};
