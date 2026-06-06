import React from 'react';
import { SakinahShell, SakinahHeader, RayaOrb, RayaScriptCard } from '../components';

import { useNavigate } from 'react-router-dom';

export const SakinahEntryPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <SakinahShell>
      <SakinahHeader />
      
      <main className="flex flex-col items-center justify-center text-center mt-8 px-4">
        <RayaOrb size="lg" className="mb-10 mt-8" />
        
        <h2 className="font-serif text-[26px] font-medium text-[#D4A853] mb-4">
          Bismillah. Welcome to Sakinah.
        </h2>
        
        <p className="text-[15px] font-light text-[#9aa0ac] leading-[1.6] mb-8 max-w-sm mx-auto">
          A sincere space for those seeking half their deen. Here, we prioritize safety, alignment in values, and character over endless profiles.
        </p>

        <RayaScriptCard 
          scriptText="I will guide you through this journey. I am here to help you articulate what matters most in your faith and life, not to judge or score you."
          className="w-full text-left mb-10"
        />

        <button 
          onClick={() => navigate('/sakinah/eligibility')}
          className="w-full py-[16px] rounded-[14px] bg-[#D4A853] text-[#07090f] font-serif font-medium text-[20px] transition-opacity hover:opacity-90"
        >
          Begin with Sincerity
        </button>
      </main>
    </SakinahShell>
  );
};
