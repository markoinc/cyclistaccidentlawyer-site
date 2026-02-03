import React from 'react';

const colorMap = {
  blue: 'bg-[#3366FF]/20 text-[#3366FF]',
  green: 'bg-[#00E676]/20 text-[#00E676]',
  red: 'bg-[#ff6b6b]/20 text-[#ff6b6b]',
  yellow: 'bg-[#ffb347]/20 text-[#ffb347]',
  purple: 'bg-[#a855f7]/20 text-[#a855f7]',
  gray: 'bg-[#6e7681]/20 text-[#6e7681]',
};

export function Badge({ children, color = 'blue', className = '' }) {
  return (
    <span className={`
      inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium
      ${colorMap[color] || colorMap.blue}
      ${className}
    `}>
      {children}
    </span>
  );
}

export default Badge;
