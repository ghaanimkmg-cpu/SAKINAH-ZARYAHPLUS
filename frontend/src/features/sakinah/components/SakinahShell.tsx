import React from 'react';

interface SakinahShellProps {
  children: React.ReactNode;
}

export const SakinahShell: React.FC<SakinahShellProps> = ({ children }) => {
  return (
    <div className="sk-viewport px-6 pt-[6px] pb-[120px] relative overflow-hidden">
      <div className="w-full max-w-md mx-auto relative flex flex-col min-h-full">
        {children}
      </div>
    </div>
  );
};
