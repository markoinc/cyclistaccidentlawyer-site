import React from 'react';

const statusStyles = {
  'active': 'bg-[#00E676]/20 text-[#00E676]',
  'in-progress': 'bg-[#3366FF]/20 text-[#3366FF]',
  'completed': 'bg-[#00E676]/20 text-[#00E676]',
  'planning': 'bg-[#ffb347]/20 text-[#ffb347]',
  'paused': 'bg-[#6e7681]/20 text-[#6e7681]',
  'blocked': 'bg-[#ff6b6b]/20 text-[#ff6b6b]',
  'pending': 'bg-[#ffb347]/20 text-[#ffb347]',
  'done': 'bg-[#00E676]/20 text-[#00E676]',
};

export function StatusPill({ status, className = '' }) {
  const normalizedStatus = status?.toLowerCase() || 'pending';
  const style = statusStyles[normalizedStatus] || statusStyles.pending;
  
  return (
    <span className={`
      inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium capitalize
      ${style}
      ${className}
    `}>
      {status?.replace(/-/g, ' ') || 'Pending'}
    </span>
  );
}

export default StatusPill;
