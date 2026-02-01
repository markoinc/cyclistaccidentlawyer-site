import Link from 'next/link';
import { getAllDocuments, getAllTags } from '@/lib/documents';
import DocumentCard from '@/components/DocumentCard';
import TagBadge from '@/components/TagBadge';

export const dynamic = 'force-dynamic';

export default function Dashboard() {
  const documents = getAllDocuments();
  const tags = getAllTags();
  const recentDocs = documents.slice(0, 6);
  const journalDocs = documents.filter(d => d.type === 'journal').slice(0, 3);
  const conceptDocs = documents.filter(d => d.type === 'concept').slice(0, 3);

  const stats = {
    total: documents.length,
    journals: documents.filter(d => d.type === 'journal').length,
    concepts: documents.filter(d => d.type === 'concept').length,
    notes: documents.filter(d => d.type === 'note').length,
  };

  return (
    <div className="p-8 max-w-6xl">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-semibold text-white tracking-tight mb-2">
          Welcome back
        </h1>
        <p className="text-zinc-500">
          Your second brain has <span className="text-white font-medium">{stats.total} documents</span> waiting for you.
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-4 gap-4 mb-8">
        {[
          { label: 'Total', value: stats.total, icon: '◈' },
          { label: 'Journals', value: stats.journals, icon: '📝' },
          { label: 'Concepts', value: stats.concepts, icon: '💡' },
          { label: 'Notes', value: stats.notes, icon: '📋' },
        ].map((stat) => (
          <div
            key={stat.label}
            className="p-4 rounded-xl bg-zinc-900/50 border border-zinc-800/50"
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-2xl">{stat.icon}</span>
              <span className="text-2xl font-semibold text-white">{stat.value}</span>
            </div>
            <p className="text-sm text-zinc-500">{stat.label}</p>
          </div>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="flex gap-3 mb-8">
        <Link
          href="/new?type=journal"
          className="px-4 py-2 bg-indigo-500/10 text-indigo-400 rounded-lg border border-indigo-500/20 hover:bg-indigo-500/20 transition-all text-sm font-medium"
        >
          + New Journal Entry
        </Link>
        <Link
          href="/new?type=concept"
          className="px-4 py-2 bg-zinc-800/50 text-zinc-300 rounded-lg border border-zinc-700/50 hover:bg-zinc-700/50 transition-all text-sm font-medium"
        >
          + New Concept
        </Link>
        <Link
          href="/new?type=note"
          className="px-4 py-2 bg-zinc-800/50 text-zinc-300 rounded-lg border border-zinc-700/50 hover:bg-zinc-700/50 transition-all text-sm font-medium"
        >
          + Quick Note
        </Link>
      </div>

      {/* Recent Documents */}
      <section className="mb-10">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-white">Recent Documents</h2>
          <Link href="/documents" className="text-sm text-zinc-500 hover:text-white transition-colors">
            View all →
          </Link>
        </div>
        <div className="grid grid-cols-2 gap-4">
          {recentDocs.map((doc) => (
            <DocumentCard key={doc.slug} document={doc} />
          ))}
        </div>
        {recentDocs.length === 0 && (
          <div className="p-8 text-center rounded-xl bg-zinc-900/30 border border-zinc-800/50 border-dashed">
            <p className="text-zinc-500 mb-3">No documents yet</p>
            <Link
              href="/new"
              className="text-indigo-400 hover:text-indigo-300 text-sm"
            >
              Create your first document →
            </Link>
          </div>
        )}
      </section>

      {/* Two Column Layout */}
      <div className="grid grid-cols-2 gap-8">
        {/* Latest Journals */}
        <section>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-white">📝 Latest Journals</h2>
            <Link href="/journal" className="text-sm text-zinc-500 hover:text-white transition-colors">
              View all →
            </Link>
          </div>
          <div className="space-y-3">
            {journalDocs.map((doc) => (
              <Link
                key={doc.slug}
                href={`/documents/${doc.slug}`}
                className="block p-3 rounded-lg bg-zinc-900/30 border border-zinc-800/50 hover:border-zinc-700/50 hover:bg-zinc-800/30 transition-all"
              >
                <div className="flex items-center justify-between">
                  <span className="text-sm text-white">{doc.title}</span>
                  <span className="text-xs text-zinc-600 font-mono">{doc.date}</span>
                </div>
              </Link>
            ))}
            {journalDocs.length === 0 && (
              <p className="text-sm text-zinc-600 py-4">No journal entries yet</p>
            )}
          </div>
        </section>

        {/* Top Tags */}
        <section>
          <h2 className="text-lg font-semibold text-white mb-4">🏷️ Top Tags</h2>
          <div className="flex flex-wrap gap-2">
            {tags.slice(0, 12).map(({ tag, count }) => (
              <Link key={tag} href={`/documents?tag=${tag}`}>
                <TagBadge tag={tag} size="md" />
              </Link>
            ))}
            {tags.length === 0 && (
              <p className="text-sm text-zinc-600">No tags yet</p>
            )}
          </div>
        </section>
      </div>
    </div>
  );
}
