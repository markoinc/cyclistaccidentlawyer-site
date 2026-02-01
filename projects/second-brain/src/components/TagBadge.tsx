interface TagBadgeProps {
  tag: string;
  size?: 'sm' | 'md';
  onClick?: () => void;
}

const tagColors: Record<string, string> = {
  'revenue-idea': 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30',
  'client-work': 'bg-blue-500/20 text-blue-400 border-blue-500/30',
  'automation': 'bg-purple-500/20 text-purple-400 border-purple-500/30',
  'content': 'bg-orange-500/20 text-orange-400 border-orange-500/30',
  'strategy': 'bg-rose-500/20 text-rose-400 border-rose-500/30',
  'learning': 'bg-cyan-500/20 text-cyan-400 border-cyan-500/30',
  'action-item': 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
};

export default function TagBadge({ tag, size = 'md', onClick }: TagBadgeProps) {
  const sizeClasses = size === 'sm' ? 'px-1.5 py-0.5 text-xs' : 'px-2 py-1 text-sm';
  const colorClass = tagColors[tag] || 'bg-zinc-700/50 text-zinc-300 border-zinc-600/30';

  const Component = onClick ? 'button' : 'span';

  return (
    <Component
      onClick={onClick}
      className={`inline-flex items-center rounded-full border ${sizeClasses} ${colorClass} font-medium transition-all ${
        onClick ? 'hover:scale-105 cursor-pointer' : ''
      }`}
    >
      {tag}
    </Component>
  );
}
