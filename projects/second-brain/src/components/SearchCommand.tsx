'use client';

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { DocumentMeta } from '@/lib/documents';

interface SearchCommandProps {
  documents: DocumentMeta[];
}

export default function SearchCommand({ documents }: SearchCommandProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [selectedIndex, setSelectedIndex] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);
  const router = useRouter();

  const filteredDocs = query
    ? documents.filter(
        (doc) =>
          doc.title.toLowerCase().includes(query.toLowerCase()) ||
          doc.excerpt.toLowerCase().includes(query.toLowerCase()) ||
          doc.tags.some((tag) => tag.toLowerCase().includes(query.toLowerCase()))
      ).slice(0, 8)
    : documents.slice(0, 5);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setIsOpen(true);
      }
      if (e.key === 'Escape') {
        setIsOpen(false);
        setQuery('');
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, []);

  useEffect(() => {
    if (isOpen) {
      inputRef.current?.focus();
    }
  }, [isOpen]);

  useEffect(() => {
    setSelectedIndex(0);
  }, [query]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setSelectedIndex((i) => Math.min(i + 1, filteredDocs.length - 1));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setSelectedIndex((i) => Math.max(i - 1, 0));
    } else if (e.key === 'Enter' && filteredDocs[selectedIndex]) {
      router.push(`/documents/${filteredDocs[selectedIndex].slug}`);
      setIsOpen(false);
      setQuery('');
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-[15vh]">
      <div
        className="absolute inset-0 bg-black/60 backdrop-blur-sm"
        onClick={() => {
          setIsOpen(false);
          setQuery('');
        }}
      />
      <div className="relative w-full max-w-xl bg-zinc-900 border border-zinc-800 rounded-xl shadow-2xl overflow-hidden">
        <div className="flex items-center gap-3 px-4 py-3 border-b border-zinc-800">
          <span className="text-zinc-500">🔍</span>
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Search documents..."
            className="flex-1 bg-transparent text-white placeholder-zinc-500 outline-none"
          />
          <kbd className="px-1.5 py-0.5 bg-zinc-800 rounded text-xs text-zinc-500 font-mono">esc</kbd>
        </div>
        <div className="max-h-[400px] overflow-y-auto">
          {filteredDocs.length === 0 ? (
            <div className="p-8 text-center text-zinc-500">
              No documents found
            </div>
          ) : (
            <ul className="py-2">
              {filteredDocs.map((doc, index) => (
                <li key={doc.slug}>
                  <button
                    onClick={() => {
                      router.push(`/documents/${doc.slug}`);
                      setIsOpen(false);
                      setQuery('');
                    }}
                    className={`w-full px-4 py-3 flex items-start gap-3 text-left transition-colors ${
                      index === selectedIndex
                        ? 'bg-indigo-500/10'
                        : 'hover:bg-zinc-800/50'
                    }`}
                  >
                    <span className="text-base mt-0.5">
                      {doc.type === 'journal' ? '📝' : doc.type === 'concept' ? '💡' : '📋'}
                    </span>
                    <div className="flex-1 min-w-0">
                      <p className={`font-medium truncate ${
                        index === selectedIndex ? 'text-indigo-400' : 'text-white'
                      }`}>
                        {doc.title}
                      </p>
                      <p className="text-sm text-zinc-500 truncate">{doc.excerpt}</p>
                    </div>
                    <span className="text-xs text-zinc-600 font-mono shrink-0">
                      {doc.date}
                    </span>
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>
        <div className="px-4 py-2 border-t border-zinc-800 flex gap-4 text-xs text-zinc-600">
          <span><kbd className="px-1 bg-zinc-800 rounded">↑↓</kbd> navigate</span>
          <span><kbd className="px-1 bg-zinc-800 rounded">↵</kbd> open</span>
        </div>
      </div>
    </div>
  );
}
