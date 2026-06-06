import React from 'react';

export interface JourneyStep {
  id: string;
  number: string; // "٠", "١", "٢" etc. or icons
  title: string;
  description: string;
  status: 'done' | 'active' | 'locked';
  pinText?: string;
}

interface SakinahJourneyStepperProps {
  steps: JourneyStep[];
}

export const SakinahJourneyStepper: React.FC<SakinahJourneyStepperProps> = ({ steps }) => {
  return (
    <div className="sk-journey">
      {steps.map((step, idx) => (
        <div key={step.id} className={`sk-jstep ${step.status}`}>
          <div className="sk-jrail">
            <div className="sk-jnode">{step.number}</div>
            {idx < steps.length - 1 && <div className="sk-jline" />}
          </div>
          <div className="sk-jbody">
            <b>{step.title}</b>
            <span>{step.description}</span>
            {step.pinText && step.status === 'active' && (
              <span className="pin">● {step.pinText}</span>
            )}
          </div>
        </div>
      ))}
    </div>
  );
};
