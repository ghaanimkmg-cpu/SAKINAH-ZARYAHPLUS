import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { SakinahShell, SakinahHeader, DevFallbackBadge, SakinahSelect } from '../components';
import { updateSakinahProfile } from '../services/sakinahApi';

export const SakinahProfileSignalsPage: React.FC = () => {
  const navigate = useNavigate();
  const [isPending, setIsPending] = useState(false);
  const [errorFallback, setErrorFallback] = useState('');

  const [approach, setApproach] = useState('');
  const [prayer, setPrayer] = useState('');
  const [timeline, setTimeline] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorFallback('');

    if (!approach || !prayer || !timeline) {
      setErrorFallback('Please complete the required fields before continuing.');
      return;
    }

    setIsPending(true);
    try {
      // In a real app we'd collect form data. For now we pass a mock payload.
      await updateSakinahProfile({ timelineToMarry: '1_year' });
      navigate('/sakinah/preferences');
    } catch (err) {
      console.warn('Backend offline, using dev fallback for SakinahProfileSignals', err);
      setErrorFallback('Backend unreachable. Proceeding in Development Preview Mode.');
      // Dev fallback: allow navigation even if backend is down
      setTimeout(() => navigate('/sakinah/preferences'), 1000);
    } finally {
      setIsPending(false);
    }
  };

  return (
    <SakinahShell>
      <SakinahHeader title="Your Profile" subtitle="CHARACTER & SIGNALS" />

      <main className="mt-6 flex flex-col gap-6">
        <p className="text-[14px] font-light text-[#9aa0ac] leading-[1.6]">
          Share your values, practices, and outlook. These signals help us find meaningful alignment, without reducing you to public labels or scores.
        </p>

        {errorFallback && <DevFallbackBadge message={errorFallback} />}

        <form className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-6" onSubmit={handleSubmit}>
          <SakinahSelect
            label="Sect / Thought"
            value={approach}
            onChange={(e) => setApproach(e.target.value)}
            placeholder="Choose your approach"
            required
            options={[
              { value: 'sunni', label: 'Sunni' },
              { value: 'shia', label: 'Shia' },
              { value: 'just_muslim', label: 'Just Muslim' },
            ]}
          />

          <SakinahSelect
            label="Prayer Frequency"
            value={prayer}
            onChange={(e) => setPrayer(e.target.value)}
            placeholder="Choose a frequency"
            required
            options={[
              { value: 'always', label: 'Always Prays' },
              { value: 'usually', label: 'Usually Prays' },
              { value: 'sometimes', label: 'Sometimes Prays' },
              { value: 'working_on_it', label: 'Working on it' },
            ]}
          />

          <SakinahSelect
            label="Timeline to Marry"
            value={timeline}
            onChange={(e) => setTimeline(e.target.value)}
            placeholder="Choose a timeline"
            required
            options={[
              { value: 'asap', label: 'As soon as possible' },
              { value: '1_year', label: 'Within 1 year' },
              { value: '2_years', label: 'Within 2 years' },
            ]}
          />

          <div className="space-y-2 md:col-span-2">
            <label className="font-mono text-[10px] tracking-[0.15em] uppercase text-[#D4A853]">A short note about your journey</label>
            <textarea 
              rows={4}
              placeholder="What are you looking to build together?"
              className="w-full bg-[#111826] border border-[rgba(255,255,255,0.06)] rounded-[14px] p-4 text-[#EDE7DA] text-[14px] font-light resize-none focus:outline-none focus:border-[#D4A853]"
            />
          </div>

          <div className="md:col-span-2">
            <button 
              type="submit" 
              disabled={isPending}
              className="w-full py-[16px] rounded-[14px] bg-[#D4A853] text-[#07090f] font-serif font-medium text-[18px] transition-opacity mt-4 hover:opacity-90 disabled:opacity-50"
            >
              {isPending ? 'Saving...' : 'Save Signals'}
            </button>
          </div>
        </form>
      </main>
    </SakinahShell>
  );
};
