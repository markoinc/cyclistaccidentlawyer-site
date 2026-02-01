import Link from 'next/link';
import { DocumentMeta } from '@/lib/documents';
import TagBadge from './TagBadge';

interface DocumentCardProps {
  document: DocumentMeta;
}

export default function DocumentCard({ document }: DocumentCardProps) {
  const typeIcons = {
    journal: '📝',
    concept: '💡',
    note: '📋',
  };

  return (
    <Link
      href={`/documents/${document.slug}`}
      className="block p-4 rounded-xl bg-zinc-900/50 border border-zinc-800/50 hover:border-zinc-700/50 hover:bg-zinc-800/30 transition-all group"
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <span className="text-base">{typeIcons[document.type]}</span>
            <h3 className="font-medium text-white truncate group-hover:text-indigo-400 transition-colors">
              {document.title}
            </h3>
          </div>
          <p className="text-sm text-zinc-500 line-clamp-2 mb-3">
            {document.excerpt}
          </p>
          <div className="flex items-center gap-2 flex-wrap">
            {document.tags.slice(0, 3).map((tag) => (
              <TagBadge key={tag} tag={tag} size="sm" />
            ))}
            {document.tags.length > 3 && (
              <span className="text-xs text-zinc-600">+{document.tags.length - 3}</span>
            )}
          </div>
        </div>
        <div className="text-right shrink-0">
          <span className="text-xs text-zinc-600 font-mono">{document.date}</span>
          {document.folder && (
            <p className="text-xs text-zinc-700 mt-1">{document.folder}/</p>
          )}
        </div>
      </div>
    </Link>
  );
}
