'use client';

import { useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { format } from 'date-fns';

const ALL_TAGS = [
  'revenue-idea',
  'client-work',
  'automation',
  'content',
  'strategy',
  'learning',
  'action-item',
];

const tagColors: Record<string, string> = {
  'revenue-idea': 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30',
  'client-work': 'bg-blue-500/20 text-blue-400 border-blue-500/30',
  'automation': 'bg-purple-500/20 text-purple-400 border-purple-500/30',
  'content': 'bg-orange-500/20 text-orange-400 border-orange-500/30',
  'strategy': 'bg-rose-500/20 text-rose-400 border-rose-500/30',
  'learning': 'bg-cyan-500/20 text-cyan-400 border-cyan-500/30',
  'action-item': 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
};

export default function NewDocumentPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const typeParam = searchParams.get('type') as 'journal' | 'concept' | 'note' | null;
  
  const today = format(new Date(), 'yyyy-MM-dd');
  const defaultTitle = typeParam === 'journal' ? `Journal - ${today}` : '';

  const [type, setType] = useState<'journal' | 'concept' | 'note'>(typeParam || 'note');
  const [title, setTitle] = useState(defaultTitle);
  const [content, setContent] = useState('');
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const toggleTag = (tag: string) => {
    setSelectedTags((prev) =>
      prev.includes(tag) ? prev.filter((t) => t !== tag) : [...prev, tag]
    );
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      const response = await fetch('/api/documents', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title,
          content,
          tags: selectedTags,
          type,
        }),
      });

      if (response.ok) {
        const { slug } = await response.json();
        router.push(`/documents/${slug}`);
      }
    } catch (error) {
      console.error('Failed to create document:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="p-8 max-w-3xl">
      <h1 className="text-2xl font-semibold text-white tracking-tight mb-8">
        New Document
      </h1>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Type Selection */}
        <div>
          <label className="block text-sm font-medium text-zinc-400 mb-2">
            Document Type
          </label>
          <div className="flex gap-3">
            {[
              { value: 'journal', label: '📝 Journal', desc: 'Daily log' },
              { value: 'concept', label: '💡 Concept', desc: 'Deep dive' },
              { value: 'note', label: '📋 Note', desc: 'Quick capture' },
            ].map((option) => (
              <button
                key={option.value}
                type="button"
                onClick={() => {
                  setType(option.value as typeof type);
                  if (option.value === 'journal' && !title) {
                    setTitle(`Journal - ${today}`);
                  }
                }}
                className={`flex-1 p-4 rounded-xl border text-left transition-all ${
                  type === option.value
                    ? 'bg-indigo-500/10 border-indigo-500/50 text-white'
                    : 'bg-zinc-900/50 border-zinc-800/50 text-zinc-400 hover:border-zinc-700/50'
                }`}
              >
                <span className="block text-lg mb-1">{option.label}</span>
                <span className="text-xs text-zinc-500">{option.desc}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Title */}
        <div>
          <label className="block text-sm font-medium text-zinc-400 mb-2">
            Title
          </label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            placeholder="Enter a title..."
            className="w-full px-4 py-3 bg-zinc-900/50 border border-zinc-800/50 rounded-xl text-white placeholder-zinc-600 outline-none focus:border-indigo-500/50 transition-colors"
          />
        </div>

        {/* Tags */}
        <div>
          <label className="block text-sm font-medium text-zinc-400 mb-2">
            Tags
          </label>
          <div className="flex flex-wrap gap-2">
            {ALL_TAGS.map((tag) => {
              const isSelected = selectedTags.includes(tag);
              const colorClass = tagColors[tag] || 'bg-zinc-700/50 text-zinc-300 border-zinc-600/30';
              return (
                <button
                  key={tag}
                  type="button"
                  onClick={() => toggleTag(tag)}
                  className={`px-3 py-1.5 rounded-full border text-sm font-medium transition-all ${
                    isSelected
                      ? colorClass
                      : 'bg-zinc-900/50 text-zinc-500 border-zinc-800/50 hover:border-zinc-700/50'
                  }`}
                >
                  {isSelected && '✓ '}
                  {tag}
                </button>
              );
            })}
          </div>
        </div>

        {/* Content */}
        <div>
          <label className="block text-sm font-medium text-zinc-400 mb-2">
            Content (Markdown)
          </label>
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            required
            rows={16}
            placeholder="Start writing..."
            className="w-full px-4 py-3 bg-zinc-900/50 border border-zinc-800/50 rounded-xl text-white placeholder-zinc-600 outline-none focus:border-indigo-500/50 transition-colors font-mono text-sm resize-none"
          />
        </div>

        {/* Submit */}
        <div className="flex justify-end gap-3 pt-4">
          <button
            type="button"
            onClick={() => router.back()}
            className="px-4 py-2 text-zinc-400 hover:text-white transition-colors"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={isSubmitting}
            className="px-6 py-2 bg-indigo-500 text-white rounded-lg hover:bg-indigo-600 transition-colors font-medium disabled:opacity-50"
          >
            {isSubmitting ? 'Creating...' : 'Create Document'}
          </button>
        </div>
      </form>
    </div>
  );
}
