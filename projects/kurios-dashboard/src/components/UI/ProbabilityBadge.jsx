import React from 'react';

export function ProbabilityBadge({ probability, className = '' }) {
  const value = typeof probability === 'number' ? probability : parseInt(probability) || 0;
  
  let colorClass = 'bg-[#6e7681]/20 text-[#6e7681]';
  if (value >= 75) {
    colorClass = 'bg-[#00E676]/20 text-[#00E676]';
  } else if (value >= 50) {
    colorClass = 'bg-[#3366FF]/20 text-[#3366FF]';
  } else if (value >= 25) {
    colorClass = 'bg-[#ffb347]/20 text-[#ffb347]';
  }
  
  return (
    <span className={`
      inline-flex items-center px-2 py-0.5 rounded text-xs font-bold
      ${colorClass}
      ${className}
    `}>
      {value}%
    </span>
  );
}

export default ProbabilityBadge;
