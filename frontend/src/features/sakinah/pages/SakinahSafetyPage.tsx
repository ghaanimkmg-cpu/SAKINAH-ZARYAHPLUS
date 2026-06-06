import React, { useState } from 'react';
import { SakinahShell, SakinahHeader, SafetyNotice, DevFallbackBadge, SakinahCard, SakinahButton } from '../components';
import { submitReport } from '../services/sakinahApi';

export const SakinahSafetyPage: React.FC = () => {
  const [isPending, setIsPending] = useState(false);
  const [reportStatus, setReportStatus] = useState<'IDLE' | 'SUCCESS' | 'FALLBACK'>('IDLE');

  const handleReport = async () => {
    setIsPending(true);
    setReportStatus('IDLE');
    try {
      await submitReport({
        targetUserId: 'mock_target',
        reason: 'Inappropriate behavior',
        timestamp: new Date().toISOString()
      });
      setReportStatus('SUCCESS');
    } catch (err) {
      console.warn('Backend offline, using dev fallback for submitReport', err);
      setReportStatus('FALLBACK');
    } finally {
      setIsPending(false);
    }
  };

  return (
    <SakinahShell>
      <SakinahHeader title="Trust & Safety" subtitle="OUR COMMITMENT" onBack={() => window.history.back()} />

      <main className="mt-6 flex flex-col gap-6">
        <h2 className="font-serif text-[24px] text-[#EDE7DA] mb-2">
          Safety First
        </h2>

        <div className="space-y-6">
          <SafetyNotice message="Sakinah is monitored for your safety. Report any inappropriate behavior, pressure, or requests for money immediately." />

          <SakinahCard padding="md">
            <h3 className="font-mono text-[10px] tracking-[0.15em] uppercase text-[#D4A853] mb-3">Privacy & Communication</h3>
            <p className="text-[13.5px] font-light text-[#9aa0ac] leading-[1.6]">
              Never share your private phone number, home address, or financial information. Keep all communication inside Sakinah until both parties, and their families, have agreed to proceed towards nikah.
            </p>
          </SakinahCard>

          <SakinahCard padding="md">
            <h3 className="font-mono text-[10px] tracking-[0.15em] uppercase text-[#D4A853] mb-3">Wali / Family Support</h3>
            <p className="text-[13.5px] font-light text-[#9aa0ac] leading-[1.6]">
              We strongly encourage involving your wali or trusted family members early in the process. True alignment respects family bonds.
            </p>
          </SakinahCard>
          
          {reportStatus === 'SUCCESS' && (
            <div className="bg-green-500/10 border border-green-500/30 rounded-[12px] p-3 text-center text-[12px] text-green-400">
              Report submitted successfully. Our safety team will review this immediately.
            </div>
          )}

          {reportStatus === 'FALLBACK' && <DevFallbackBadge message="Backend unreachable. Report mock processed." />}

          <SakinahButton 
            variant="danger"
            onClick={handleReport}
            disabled={isPending}
            className="mt-4"
          >
            {isPending ? 'Submitting...' : 'Report an Incident'}
          </SakinahButton>
        </div>
      </main>
    </SakinahShell>
  );
};
