import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { SakinahShell, SakinahHeader } from '../components';
import { updateSakinahProfile } from '../services/sakinahApi';

export const SakinahProfileSignalsPage: React.FC = () => {
  const navigate = useNavigate();
  const [isPending, setIsPending] = useState(false);
  const [errorFallback, setErrorFallback] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsPending(true);
    setErrorFallback('');
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

        {errorFallback && (
          <div className="bg-[#D4A853]/10 border border-[#D4A853]/30 rounded-[12px] p-3 text-center text-[12px] text-[#D4A853]">
            {errorFallback}
          </div>
        )}

        <form className="space-y-6 mt-4" onSubmit={handleSubmit}>
          <div className="space-y-2">
            <label className="font-mono text-[10px] tracking-[0.15em] uppercase text-[#D4A853]">Sect / Thought</label>
            <select className="w-full bg-[#111826] border border-[rgba(255,255,255,0.06)] rounded-[14px] p-4 text-[#EDE7DA] text-[14px] font-light focus:outline-none focus:border-[#D4A853]">
              <option value="">Select your approach</option>
              <option value="sunni">Sunni</option>
              <option value="shia">Shia</option>
              <option value="just_muslim">Just Muslim</option>
            </select>
          </div>

          <div className="space-y-2">
            <label className="font-mono text-[10px] tracking-[0.15em] uppercase text-[#D4A853]">Prayer Frequency</label>
            <select className="w-full bg-[#111826] border border-[rgba(255,255,255,0.06)] rounded-[14px] p-4 text-[#EDE7DA] text-[14px] font-light focus:outline-none focus:border-[#D4A853]">
              <option value="">Select frequency</option>
              <option value="always">Always Prays</option>
              <option value="usually">Usually Prays</option>
              <option value="sometimes">Sometimes Prays</option>
              <option value="working_on_it">Working on it</option>
            </select>
          </div>

          <div className="space-y-2">
            <label className="font-mono text-[10px] tracking-[0.15em] uppercase text-[#D4A853]">Timeline to Marry</label>
            <select className="w-full bg-[#111826] border border-[rgba(255,255,255,0.06)] rounded-[14px] p-4 text-[#EDE7DA] text-[14px] font-light focus:outline-none focus:border-[#D4A853]">
              <option value="">Select timeline</option>
              <option value="asap">As soon as possible</option>
              <option value="1_year">Within 1 year</option>
              <option value="2_years">Within 2 years</option>
            </select>
          </div>

          <div className="space-y-2">
            <label className="font-mono text-[10px] tracking-[0.15em] uppercase text-[#D4A853]">A short note about your journey</label>
            <textarea 
              rows={4}
              placeholder="What are you looking to build together?"
              className="w-full bg-[#111826] border border-[rgba(255,255,255,0.06)] rounded-[14px] p-4 text-[#EDE7DA] text-[14px] font-light resize-none focus:outline-none focus:border-[#D4A853]"
            />
          </div>

          <button 
            type="submit" 
            disabled={isPending}
            className="w-full py-[16px] rounded-[14px] bg-[#D4A853] text-[#07090f] font-serif font-medium text-[18px] transition-opacity mt-4 hover:opacity-90 disabled:opacity-50"
          >
            {isPending ? 'Saving...' : 'Save Signals'}
          </button>
        </form>
      </main>
    </SakinahShell>
  );
};
