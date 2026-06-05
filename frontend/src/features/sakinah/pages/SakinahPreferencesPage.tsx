import React from 'react';
import { SakinahShell, SakinahHeader } from '../components';

export const SakinahPreferencesPage: React.FC = () => {
  return (
    <SakinahShell>
      <SakinahHeader title="Preferences" subtitle="MATCH ALIGNMENT" />

      <main className="mt-6 flex flex-col gap-6">
        <p className="text-[14px] font-light text-[#9aa0ac] leading-[1.6]">
          Define the qualities that are essential for your marriage. We use these to gently filter candidates so you only see those who align with your core boundaries.
        </p>

        <form className="space-y-6 mt-4" onSubmit={(e) => e.preventDefault()}>
          <div className="space-y-2">
            <label className="font-mono text-[10px] tracking-[0.15em] uppercase text-[#D4A853]">Age Range Preference</label>
            <div className="flex gap-4">
              <input 
                type="number" 
                placeholder="Min"
                className="w-full bg-[#111826] border border-[rgba(255,255,255,0.06)] rounded-[14px] p-4 text-[#EDE7DA] text-[14px] font-light focus:outline-none focus:border-[#D4A853]"
              />
              <input 
                type="number" 
                placeholder="Max"
                className="w-full bg-[#111826] border border-[rgba(255,255,255,0.06)] rounded-[14px] p-4 text-[#EDE7DA] text-[14px] font-light focus:outline-none focus:border-[#D4A853]"
              />
            </div>
          </div>

          <div className="space-y-2">
            <label className="font-mono text-[10px] tracking-[0.15em] uppercase text-[#D4A853]">Willingness to Relocate</label>
            <select className="w-full bg-[#111826] border border-[rgba(255,255,255,0.06)] rounded-[14px] p-4 text-[#EDE7DA] text-[14px] font-light focus:outline-none focus:border-[#D4A853]">
              <option value="">Select an option</option>
              <option value="yes">Yes, open to relocating</option>
              <option value="no">No, prefer to stay locally</option>
              <option value="flexible">Flexible / Let's discuss</option>
            </select>
          </div>

          <div className="space-y-2 pt-4">
            <label className="font-mono text-[10px] tracking-[0.15em] uppercase text-[#C98A8A]">Non-Negotiable Boundaries</label>
            <p className="text-[12px] text-[#5f6675] mb-3">
              Check the boundaries that are absolute requirements for you.
            </p>
            <div className="flex flex-col gap-3">
              <label className="flex items-center gap-3 cursor-pointer">
                <input type="checkbox" className="w-5 h-5 accent-[#D4A853] bg-[#111826] border-[rgba(255,255,255,0.06)]" />
                <span className="text-[14px] text-[#EDE7DA] font-light">Must pray regularly</span>
              </label>
              <label className="flex items-center gap-3 cursor-pointer">
                <input type="checkbox" className="w-5 h-5 accent-[#D4A853] bg-[#111826] border-[rgba(255,255,255,0.06)]" />
                <span className="text-[14px] text-[#EDE7DA] font-light">Must not smoke</span>
              </label>
            </div>
          </div>

          <button type="submit" className="w-full py-[16px] rounded-[14px] bg-[#D4A853] text-[#07090f] font-serif font-medium text-[18px] transition-opacity mt-6 hover:opacity-90">
            Save Preferences
          </button>
        </form>
      </main>
    </SakinahShell>
  );
};
