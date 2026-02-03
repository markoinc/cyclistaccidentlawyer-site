import React from 'react';

export function StatCard({ title, value, change, icon: Icon, trend = 'up' }) {
  const trendColor = trend === 'up' ? 'text-[#00E676]' : 'text-[#ff6b6b]';
  
  return (
    <div className="bg-[#242930] border border-[#2d333b] rounded-xl p-5">
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs text-[#6e7681] uppercase tracking-wider font-medium">
          {title}
        </span>
        {Icon && <Icon size={18} className="text-[#6e7681]" />}
      </div>
      <div className="text-2xl font-bold text-white mb-1">{value}</div>
      {change && (
        <div className={`text-xs ${trendColor}`}>
          {trend === 'up' ? '↑' : '↓'} {change}
        </div>
      )}
    </div>
  );
}

export default StatCard;
