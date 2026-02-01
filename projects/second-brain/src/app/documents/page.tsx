import { getAllDocuments, getDocumentsByTag, getDocumentsByFolder } from '@/lib/documents';
import DocumentCard from '@/components/DocumentCard';

export const dynamic = 'force-dynamic';

interface PageProps {
  searchParams: Promise<{ tag?: string; folder?: string; q?: string }>;
}

export default async function DocumentsPage({ searchParams }: PageProps) {
  const params = await searchParams;
  const tag = params.tag;
  const folder = params.folder;
  const query = params.q;

  let documents = getAllDocuments();
  let title = 'All Documents';
  let subtitle = `${documents.length} documents in your second brain`;

  if (tag) {
    documents = getDocumentsByTag(tag);
    title = `Tagged: ${tag}`;
    subtitle = `${documents.length} documents with this tag`;
  } else if (folder) {
    documents = getDocumentsByFolder(folder);
    title = `Folder: ${folder}`;
    subtitle = `${documents.length} documents in this folder`;
  } else if (query) {
    const lowerQuery = query.toLowerCase();
    documents = documents.filter(
      (doc) =>
        doc.title.toLowerCase().includes(lowerQuery) ||
        doc.excerpt.toLowerCase().includes(lowerQuery) ||
        doc.tags.some((t) => t.toLowerCase().includes(lowerQuery))
    );
    title = `Search: "${query}"`;
    subtitle = `${documents.length} results found`;
  }

  return (
    <div className="p-8 max-w-5xl">
      <div className="mb-8">
        <h1 className="text-2xl font-semibold text-white tracking-tight mb-2">{title}</h1>
        <p className="text-zinc-500">{subtitle}</p>
      </div>

      {/* Search Bar */}
      <form className="mb-6">
        <div className="relative">
          <input
            type="text"
            name="q"
            defaultValue={query}
            placeholder="Search documents..."
            className="w-full px-4 py-3 bg-zinc-900/50 border border-zinc-800/50 rounded-xl text-white placeholder-zinc-500 outline-none focus:border-indigo-500/50 transition-colors"
          />
          <button
            type="submit"
            className="absolute right-3 top-1/2 -translate-y-1/2 px-3 py-1 bg-zinc-800 rounded-lg text-sm text-zinc-400 hover:text-white transition-colors"
          >
            Search
          </button>
        </div>
      </form>

      {/* Document List */}
      <div className="space-y-3">
        {documents.map((doc) => (
          <DocumentCard key={doc.slug} document={doc} />
        ))}
      </div>

      {documents.length === 0 && (
        <div className="p-12 text-center rounded-xl bg-zinc-900/30 border border-zinc-800/50 border-dashed">
          <p className="text-zinc-500 mb-2">No documents found</p>
          <p className="text-sm text-zinc-600">Try a different search or create a new document</p>
        </div>
      )}
    </div>
  );
}
