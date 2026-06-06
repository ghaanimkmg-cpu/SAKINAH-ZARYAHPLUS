import React, { useState } from 'react';
import { SakinahShell, SakinahHeader, SafetyNotice, DevFallbackBadge, SakinahCard, SakinahButton, SakinahSelect, SakinahTextarea } from '../components';
import { submitReport } from '../services/sakinahApi';

export const SakinahSafetyPage: React.FC = () => {
  const [isPending, setIsPending] = useState(false);
  const [reportStatus, setReportStatus] = useState<'IDLE' | 'SUCCESS' | 'FALLBACK'>('IDLE');
  
  const [reasonType, setReasonType] = useState('');
  const [details, setDetails] = useState('');
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});
  const [errorFallback, setErrorFallback] = useState('');

  const handleReport = async (e: React.FormEvent) => {
    e.preventDefault();
    setFieldErrors({});
    setErrorFallback('');

    const errors: Record<string, string> = {};
    if (!reasonType) errors.reasonType = 'Please select a reason.';
    if (!details.trim()) errors.details = 'Please provide details about the incident.';

    if (Object.keys(errors).length > 0) {
      setFieldErrors(errors);
      setErrorFallback('Please complete all required fields before continuing.');
      return;
    }

    setIsPending(true);
    setReportStatus('IDLE');
    try {
      await submitReport({
        targetUserId: 'mock_target',
        reason: `${reasonType}: ${details}`,
        timestamp: new Date().toISOString()
      });
      setReportStatus('SUCCESS');
      setReasonType('');
      setDetails('');
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
          
          <form className="bg-[#111826] border border-[rgba(255,255,255,0.06)] rounded-[22px] p-5 space-y-4" onSubmit={handleReport} noValidate>
            <h3 className="font-mono text-[10px] tracking-[0.15em] uppercase text-[#C98A8A] mb-3">Report an Incident</h3>
            
            {errorFallback && <DevFallbackBadge message={errorFallback} />}
            
            {reportStatus === 'SUCCESS' && (
              <div className="bg-green-500/10 border border-green-500/30 rounded-[12px] p-3 text-center text-[12px] text-green-400">
                Report submitted successfully. Our safety team will review this immediately.
              </div>
            )}

            {reportStatus === 'FALLBACK' && <DevFallbackBadge message="Backend unreachable. Report mock processed." />}

            <SakinahSelect
              label="Reason for Report"
              value={reasonType}
              onChange={(e) => { setReasonType(e.target.value); setFieldErrors(prev => ({...prev, reasonType: ''})); }}
              placeholder="Select a reason"
              required
              error={fieldErrors.reasonType}
              options={[
                { value: 'inappropriate_behavior', label: 'Inappropriate Behavior' },
                { value: 'pressure', label: 'Pressure or Coercion' },
                { value: 'financial', label: 'Request for Money' },
                { value: 'other', label: 'Other' },
              ]}
            />

            <SakinahTextarea
              label="Details"
              value={details}
              onChange={(e) => { setDetails(e.target.value); setFieldErrors(prev => ({...prev, details: ''})); }}
              rows={4}
              placeholder="Please describe what happened..."
              required
              error={fieldErrors.details}
            />

            <SakinahButton 
              type="submit"
              variant="danger"
              disabled={isPending}
              className="mt-2"
            >
              {isPending ? 'Submitting...' : 'Submit Report'}
            </SakinahButton>
          </form>
        </div>
      </main>
    </SakinahShell>
  );
};
