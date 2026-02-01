import { notFound } from 'next/navigation';
import Link from 'next/link';
import { getDocument, getAllDocuments } from '@/lib/documents';
import TagBadge from '@/components/TagBadge';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

export const dynamic = 'force-dynamic';

interface PageProps {
  params: Promise<{ slug: string[] }>;
}

export default async function DocumentPage({ params }: PageProps) {
  const { slug } = await params;
  const slugPath = slug.join('/');
  const document = getDocument(slugPath);

  if (!document) {
    notFound();
  }

  const typeIcons = {
    journal: '📝',
    concept: '💡',
    note: '📋',
  };

  return (
    <div className="p-8 max-w-4xl">
      {/* Breadcrumb */}
      <nav className="flex items-center gap-2 text-sm text-zinc-500 mb-6">
        <Link href="/documents" className="hover:text-white transition-colors">
          Documents
        </Link>
        {document.folder && (
          <>
            <span>/</span>
            <Link
              href={`/documents?folder=${document.folder}`}
              className="hover:text-white transition-colors"
            >
              {document.folder}
            </Link>
          </>
        )}
        <span>/</span>
        <span className="text-zinc-400">{document.title}</span>
      </nav>

      {/* Header */}
      <header className="mb-8 pb-6 border-b border-zinc-800/50">
        <div className="flex items-start justify-between gap-4">
          <div>
            <div className="flex items-center gap-3 mb-3">
              <span className="text-2xl">{typeIcons[document.type]}</span>
              <h1 className="text-3xl font-semibold text-white tracking-tight">
                {document.title}
              </h1>
            </div>
            <div className="flex items-center gap-4 text-sm text-zinc-500">
              <span className="font-mono">{document.date}</span>
              <span>•</span>
              <span className="capitalize">{document.type}</span>
              {document.folder && (
                <>
                  <span>•</span>
                  <span>{document.folder}/</span>
                </>
              )}
            </div>
          </div>
          <div className="flex gap-2">
            <Link
              href={`/edit/${slugPath}`}
              className="px-3 py-1.5 bg-zinc-800 text-zinc-300 rounded-lg text-sm hover:bg-zinc-700 transition-colors"
            >
              Edit
            </Link>
          </div>
        </div>
        
        {/* Tags */}
        {document.tags.length > 0 && (
          <div className="flex gap-2 mt-4 flex-wrap">
            {document.tags.map((tag) => (
              <Link key={tag} href={`/documents?tag=${tag}`}>
                <TagBadge tag={tag} />
              </Link>
            ))}
          </div>
        )}
      </header>

      {/* Content */}
      <article className="prose">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>
          {document.content}
        </ReactMarkdown>
      </article>

      {/* Footer */}
      <footer className="mt-12 pt-6 border-t border-zinc-800/50">
        <div className="flex items-center justify-between">
          <Link
            href="/documents"
            className="text-sm text-zinc-500 hover:text-white transition-colors"
          >
            ← Back to Documents
          </Link>
          <div className="text-xs text-zinc-600">
            Last updated: {document.date}
          </div>
        </div>
      </footer>
    </div>
  );
}

export async function generateStaticParams() {
  const documents = getAllDocuments();
  return documents.map((doc) => ({
    slug: doc.slug.split('/'),
  }));
}
