import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { SakinahShell, SakinahHeader, DevFallbackBadge, SakinahSelect, SakinahInput, SakinahButton } from '../components';
import { updateSakinahPreferences } from '../services/sakinahApi';

export const SakinahPreferencesPage: React.FC = () => {
  const navigate = useNavigate();
  const [isPending, setIsPending] = useState(false);
  const [errorFallback, setErrorFallback] = useState('');

  const [relocation, setRelocation] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorFallback('');

    if (!relocation) {
      setErrorFallback('Please complete the required fields before continuing.');
      return;
    }

    setIsPending(true);
    try {
      // In a real app we'd collect form data. For now we pass a mock payload.
      await updateSakinahPreferences({ relocationWillingness: true });
      navigate('/sakinah/considered-few');
    } catch (err) {
      console.warn('Backend offline, using dev fallback for SakinahPreferences', err);
      setErrorFallback('Backend unreachable. Proceeding in Development Preview Mode.');
      setTimeout(() => navigate('/sakinah/considered-few'), 1000);
    } finally {
      setIsPending(false);
    }
  };

  return (
    <SakinahShell>
      <SakinahHeader title="Preferences" subtitle="MATCH ALIGNMENT" />

      <main className="mt-6 flex flex-col gap-6">
        <p className="text-[14px] font-light text-[#9aa0ac] leading-[1.6]">
          Define the qualities that are essential for your marriage. We use these to gently filter candidates so you only see those who align with your core boundaries.
        </p>

        {errorFallback && <DevFallbackBadge message={errorFallback} />}

        <form className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-6 items-start" onSubmit={handleSubmit}>
          <div className="space-y-2">
            <label className="font-mono text-[10px] tracking-[0.15em] uppercase text-[#D4A853]">Age Range Preference</label>
            <div className="flex gap-4">
              <SakinahInput 
                type="number" 
                placeholder="Min"
                className="flex-1"
              />
              <SakinahInput 
                type="number" 
                placeholder="Max"
                className="flex-1"
              />
            </div>
          </div>

          <SakinahSelect
            label="Willingness to Relocate"
            value={relocation}
            onChange={(e) => setRelocation(e.target.value)}
            placeholder="Choose an option"
            required
            options={[
              { value: 'yes', label: 'Yes, open to relocating' },
              { value: 'no', label: 'No, prefer to stay locally' },
              { value: 'flexible', label: "Flexible / Let's discuss" },
            ]}
          />

          <div className="space-y-2 pt-4 md:col-span-2">
            <label className="font-mono text-[10px] tracking-[0.15em] uppercase text-[#C98A8A]">Non-Negotiable Boundaries</label>
            <p className="text-[12px] text-[#5f6675] mb-3">
              Check the boundaries that are absolute requirements for you.
            </p>
            <div className="flex flex-col gap-3">
              <label className="flex items-center gap-3 cursor-pointer group">
                <input type="checkbox" className="w-5 h-5 accent-[#D4A853] bg-[#111826] border-[rgba(255,255,255,0.06)] rounded-[4px]" />
                <span className="text-[14px] text-[#EDE7DA] font-light group-hover:text-[#D4A853] transition-colors">Must pray regularly</span>
              </label>
              <label className="flex items-center gap-3 cursor-pointer group">
                <input type="checkbox" className="w-5 h-5 accent-[#D4A853] bg-[#111826] border-[rgba(255,255,255,0.06)] rounded-[4px]" />
                <span className="text-[14px] text-[#EDE7DA] font-light group-hover:text-[#D4A853] transition-colors">Must not smoke</span>
              </label>
            </div>
          </div>

          <div className="md:col-span-2">
            <SakinahButton 
              type="submit" 
              disabled={isPending}
              size="lg"
              className="mt-4"
            >
              {isPending ? 'Saving...' : 'Save Preferences'}
            </SakinahButton>
          </div>
        </form>
      </main>
    </SakinahShell>
  );
};
