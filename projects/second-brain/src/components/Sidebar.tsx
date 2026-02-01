'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useState } from 'react';

interface SidebarProps {
  folders: { name: string; count: number }[];
  tags: { tag: string; count: number }[];
}

export default function Sidebar({ folders, tags }: SidebarProps) {
  const pathname = usePathname();
  const [foldersOpen, setFoldersOpen] = useState(true);
  const [tagsOpen, setTagsOpen] = useState(true);

  const navItems = [
    { href: '/', label: 'Dashboard', icon: '◈' },
    { href: '/documents', label: 'All Documents', icon: '◇' },
    { href: '/journal', label: 'Journal', icon: '◎' },
    { href: '/new', label: 'New Document', icon: '+' },
  ];

  const tagColors: Record<string, string> = {
    'revenue-idea': 'bg-emerald-500/20 text-emerald-400',
    'client-work': 'bg-blue-500/20 text-blue-400',
    'automation': 'bg-purple-500/20 text-purple-400',
    'content': 'bg-orange-500/20 text-orange-400',
    'strategy': 'bg-rose-500/20 text-rose-400',
    'learning': 'bg-cyan-500/20 text-cyan-400',
    'action-item': 'bg-yellow-500/20 text-yellow-400',
  };

  return (
    <aside className="w-64 h-screen bg-[#0f0f10] border-r border-zinc-800/50 flex flex-col fixed left-0 top-0">
      {/* Logo */}
      <div className="p-4 border-b border-zinc-800/50">
        <Link href="/" className="flex items-center gap-2">
          <span className="text-xl font-semibold tracking-tight text-white">Second Brain</span>
        </Link>
        <p className="text-xs text-zinc-500 mt-1">Never lose an idea again</p>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto p-3">
        <div className="space-y-1">
          {navItems.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-all ${
                  isActive
                    ? 'bg-indigo-500/10 text-indigo-400'
                    : 'text-zinc-400 hover:text-white hover:bg-zinc-800/50'
                }`}
              >
                <span className="w-5 text-center font-mono">{item.icon}</span>
                {item.label}
              </Link>
            );
          })}
        </div>

        {/* Folders */}
        <div className="mt-6">
          <button
            onClick={() => setFoldersOpen(!foldersOpen)}
            className="flex items-center justify-between w-full px-3 py-2 text-xs font-medium text-zinc-500 uppercase tracking-wider hover:text-zinc-300"
          >
            <span>Folders</span>
            <span className="font-mono">{foldersOpen ? '−' : '+'}</span>
          </button>
          {foldersOpen && (
            <div className="mt-1 space-y-1">
              {folders.map((folder) => (
                <Link
                  key={folder.name}
                  href={`/documents?folder=${folder.name}`}
                  className="flex items-center justify-between px-3 py-1.5 rounded-lg text-sm text-zinc-400 hover:text-white hover:bg-zinc-800/50 transition-all"
                >
                  <span className="flex items-center gap-2">
                    <span className="text-zinc-600">📁</span>
                    {folder.name || 'root'}
                  </span>
                  <span className="text-xs text-zinc-600">{folder.count}</span>
                </Link>
              ))}
            </div>
          )}
        </div>

        {/* Tags */}
        <div className="mt-6">
          <button
            onClick={() => setTagsOpen(!tagsOpen)}
            className="flex items-center justify-between w-full px-3 py-2 text-xs font-medium text-zinc-500 uppercase tracking-wider hover:text-zinc-300"
          >
            <span>Tags</span>
            <span className="font-mono">{tagsOpen ? '−' : '+'}</span>
          </button>
          {tagsOpen && (
            <div className="mt-1 flex flex-wrap gap-1.5 px-3">
              {tags.slice(0, 10).map(({ tag, count }) => (
                <Link
                  key={tag}
                  href={`/documents?tag=${tag}`}
                  className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs transition-all hover:scale-105 ${
                    tagColors[tag] || 'bg-zinc-700/50 text-zinc-300'
                  }`}
                >
                  {tag}
                  <span className="opacity-60">{count}</span>
                </Link>
              ))}
            </div>
          )}
        </div>
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-zinc-800/50">
        <div className="text-xs text-zinc-600">
          <kbd className="px-1.5 py-0.5 bg-zinc-800 rounded text-zinc-400 font-mono">⌘K</kbd>
          <span className="ml-2">Quick search</span>
        </div>
      </div>
    </aside>
  );
}
