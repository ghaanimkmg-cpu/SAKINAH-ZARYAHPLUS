import React, { useEffect, useState } from 'react';
import { SakinahJourneyFrame } from '../components/SakinahJourneyFrame';
import { SakinahCard } from '../components/SakinahCard';
import { SakinahNotice } from '../components/SakinahNotice';
import { SakinahMetaRow } from '../components/SakinahMetaRow';
import { DevFallbackBadge } from '../components/DevFallbackBadge';
import { getNisProofReport } from '../services/sakinahApi';

interface ProofResult {
  candidate_id: string;
  expected: string;
  actual: string;
  reason: string;
}

interface ProofReport {
  current_user: string;
  nis_passed: boolean;
  results: ProofResult[];
}

const humanLabels: Record<string, string> = {
  'demo_candidate_strong': 'Strong Candidate',
  'demo_candidate_banned': 'Banned Candidate',
  'demo_candidate_angry': 'Angry / Weak Repair Candidate',
  'demo_candidate_age_mismatch': 'Age Mismatch Candidate',
  'demo_candidate_weak': 'Weak Compatibility Candidate',
  'demo_candidate_insufficient': 'Insufficient Data Candidate',
};

export const SakinahNisProofPage: React.FC = () => {
  const [report, setReport] = useState<ProofReport | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadProof() {
      try {
        const data = await getNisProofReport();
        setReport(data);
      } catch (err: any) {
        if (err.message && (err.message.includes('Forbidden') || err.message.includes('403') || err.message.includes('404'))) {
          setError('Proof report is disabled outside development mode.');
        } else {
          setError('Failed to connect to the NIS backend engine. Please ensure the backend is running.');
        }
      } finally {
        setLoading(false);
      }
    }
    loadProof();
  }, []);

  const getBadgeColor = (expected: string, actual: string) => {
    if (expected !== actual) return 'var(--sakinah-error, #f44336)';
    if (actual === 'SHOWN') return 'var(--sakinah-success, #4CAF50)';
    return 'var(--sakinah-gold, #CFA870)';
  };

  return (
    <SakinahJourneyFrame
      title="NIS Practical Proof Report"
      subtitle="A controlled backend demonstration showing how NIS accepts or blocks candidates."
      currentStep={1}
      totalSteps={1}
      hideProgress
    >
      <div style={{ marginBottom: '24px' }}>
        <DevFallbackBadge message="Development Proof Mode: This page is for internal demo/testing only and must not be exposed in production." />
      </div>

      {loading && (
        <SakinahCard variant="ghost">
          <p style={{ textAlign: 'center', color: 'var(--sakinah-text-muted)' }}>Executing NIS Proof Engine...</p>
        </SakinahCard>
      )}

      {error && (
        <SakinahNotice title="Production Safety Active" intent="warning">
          {error}
        </SakinahNotice>
      )}

      {report && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
          
          <SakinahCard variant="premium" title="Proof Status">
            <SakinahMetaRow label="Current demo user" value={report.current_user} />
            <SakinahMetaRow 
              label="NIS proof status" 
              value={report.nis_passed ? 'PASSED' : 'FAILED'} 
              valueStyle={{ color: report.nis_passed ? 'var(--sakinah-success, #4CAF50)' : 'var(--sakinah-error, #f44336)', fontWeight: 600 }}
            />
            <SakinahMetaRow label="Backend authority" value="Enabled" />
            <SakinahMetaRow label="Frontend decision-making" value="Disabled" />
          </SakinahCard>

          <div>
            <h3 style={{ color: 'var(--sakinah-gold)', marginBottom: '16px', fontSize: '1.2rem', fontWeight: 600 }}>Candidate Outcomes</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              {report.results.map((r, idx) => (
                <SakinahCard key={idx} variant="bordered" title={humanLabels[r.candidate_id] || r.candidate_id}>
                  <div style={{ display: 'flex', gap: '16px', marginBottom: '12px', flexWrap: 'wrap' }}>
                    <div style={{ 
                      padding: '4px 8px', 
                      borderRadius: '4px', 
                      backgroundColor: 'rgba(255,255,255,0.05)',
                      border: `1px solid ${getBadgeColor(r.expected, r.actual)}`,
                      color: getBadgeColor(r.expected, r.actual),
                      fontSize: '0.85rem',
                      fontWeight: 500
                    }}>
                      Expected: {r.expected}
                    </div>
                    <div style={{ 
                      padding: '4px 8px', 
                      borderRadius: '4px', 
                      backgroundColor: 'rgba(255,255,255,0.05)',
                      border: `1px solid ${getBadgeColor(r.expected, r.actual)}`,
                      color: getBadgeColor(r.expected, r.actual),
                      fontSize: '0.85rem',
                      fontWeight: 500
                    }}>
                      Actual: {r.actual}
                    </div>
                  </div>
                  <SakinahMetaRow label="Reason" value={r.reason} />
                </SakinahCard>
              ))}
            </div>
          </div>

          <SakinahCard variant="ghost" title="How this proves NIS is working">
            <ol style={{ paddingLeft: '20px', margin: 0, color: 'var(--sakinah-text-muted)', display: 'flex', flexDirection: 'column', gap: '8px' }}>
              <li>NIS receives multiple controlled candidates.</li>
              <li>It does not show everyone.</li>
              <li>It applies hard filters first.</li>
              <li>It checks psychological pair dynamics.</li>
              <li>It applies confidence/no-match rules.</li>
              <li>It only allows candidates that pass.</li>
              <li>The frontend only displays backend-approved results.</li>
            </ol>
          </SakinahCard>

          <SakinahNotice title="Privacy Proof" intent="info">
            <ul style={{ paddingLeft: '20px', margin: 0, display: 'flex', flexDirection: 'column', gap: '4px' }}>
              <li>No Aadhaar</li>
              <li>No selfie</li>
              <li>No raw Raya conversation</li>
              <li>No raw Barakah entries</li>
              <li>No compatibility percentage</li>
              <li>No spiritual score</li>
              <li>No "perfect match" claim</li>
            </ul>
          </SakinahNotice>

        </div>
      )}
    </SakinahJourneyFrame>
  );
};
