import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  SakinahJourneyFrame, 
  SakinahHeader, 
  SakinahButton,
  DevFallbackBadge
} from '../components';

export const SakinahLivenessPage: React.FC = () => {
  const navigate = useNavigate();
  const [isVerified, setIsVerified] = useState(false);

  const handleVerify = () => {
    // In dev mode, we just simulate success.
    setIsVerified(true);
  };

  return (
    <SakinahJourneyFrame>
      <SakinahHeader 
        title="One quick look" 
        subtitle="Liveness · stays private" 
        onBack={() => navigate(-1)} 
      />

      <div className="mb-4">
        <DevFallbackBadge message="Production Liveness vendor pending. No real selfie collected." />
      </div>

      <div className="sk-portrait sk-fx sk-d1">
        <div className="aura" style={{ borderStyle: 'dashed', color: 'var(--sk-gold-dim)' }}>
          ◉
        </div>
      </div>

      <p className="text-[13px] text-[var(--sk-ink-dim)] font-light leading-[1.6] mb-[14px] text-center sk-fx sk-d2">
        Center your face and blink once — proves you're real and matches your ID. <b style={{ color: '#9cc596', fontWeight: 500 }}>No one but the system ever sees it.</b>
      </p>

      {!isVerified ? (
        <div className="sk-fx sk-d3 mt-4">
          <SakinahButton variant="primary" onClick={handleVerify}>
            Capture & verify
          </SakinahButton>
        </div>
      ) : (
        <div className="sk-fx sk-rise mt-4">
          <div className="flex flex-wrap gap-[7px] justify-center my-[14px]">
            <span className="inline-flex items-center gap-[6px] text-[11px] text-[var(--sk-green)] border border-[rgba(127,176,122,0.25)] rounded-[30px] px-[12px] py-[5px] bg-[rgba(212,168,83,0.05)]">
              ✓ Phone
            </span>
            <span className="inline-flex items-center gap-[6px] text-[11px] text-[var(--sk-green)] border border-[rgba(127,176,122,0.25)] rounded-[30px] px-[12px] py-[5px] bg-[rgba(212,168,83,0.05)]">
              ✓ ID verified
            </span>
            <span className="inline-flex items-center gap-[6px] text-[11px] text-[var(--sk-green)] border border-[rgba(127,176,122,0.25)] rounded-[30px] px-[12px] py-[5px] bg-[rgba(212,168,83,0.05)]">
              ✓ Photo-matched
            </span>
          </div>
          <SakinahButton variant="primary" onClick={() => navigate('/sakinah/home')}>
            Enter Sakinah →
          </SakinahButton>
        </div>
      )}
    </SakinahJourneyFrame>
  );
};
