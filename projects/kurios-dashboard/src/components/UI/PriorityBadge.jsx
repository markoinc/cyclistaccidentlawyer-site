import React from 'react';

const priorityStyles = {
  p0: 'bg-[#ff6b6b]/20 text-[#ff6b6b]',
  p1: 'bg-[#ffb347]/20 text-[#ffb347]',
  p2: 'bg-[#3366FF]/20 text-[#3366FF]',
  p3: 'bg-[#6e7681]/20 text-[#6e7681]',
  high: 'bg-[#ff6b6b]/20 text-[#ff6b6b]',
  medium: 'bg-[#ffb347]/20 text-[#ffb347]',
  low: 'bg-[#6e7681]/20 text-[#6e7681]',
};

export function PriorityBadge({ priority, className = '' }) {
  const normalizedPriority = priority?.toLowerCase() || 'p2';
  const style = priorityStyles[normalizedPriority] || priorityStyles.p2;
  
  return (
    <span className={`
      inline-flex items-center px-2 py-0.5 rounded text-xs font-bold uppercase
      ${style}
      ${className}
    `}>
      {priority || 'P2'}
    </span>
  );
}

export default PriorityBadge;
