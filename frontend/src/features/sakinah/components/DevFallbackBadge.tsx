import React from 'react';

interface DevFallbackBadgeProps {
  message?: string;
}

export const DevFallbackBadge: React.FC<DevFallbackBadgeProps> = ({ 
  message = "Backend is not connected, so safe demo data is being used." 
}) => {
  return (
    <div className="bg-[#D4A853]/10 border border-[#D4A853]/30 rounded-[12px] p-4 text-center my-4">
      <h4 className="font-serif text-[14px] text-[#D4A853] mb-1 font-medium tracking-wide">
        Development Preview Mode
      </h4>
      <p className="text-[12px] text-[#D4A853]/80 leading-relaxed font-light">
        {message}
      </p>
    </div>
  );
};
