import Link from 'next/link';
import { getAllDocuments } from '@/lib/documents';
import { format, parseISO, startOfMonth, endOfMonth, eachDayOfInterval, isSameMonth, isToday, isSameDay } from 'date-fns';

export const dynamic = 'force-dynamic';

export default function JournalPage() {
  const documents = getAllDocuments();
  const journalDocs = documents.filter(d => d.type === 'journal');
  
  // Get current month's calendar
  const today = new Date();
  const monthStart = startOfMonth(today);
  const monthEnd = endOfMonth(today);
  const daysInMonth = eachDayOfInterval({ start: monthStart, end: monthEnd });
  
  // Create a set of dates that have journal entries
  const journalDates = new Set(journalDocs.map(d => d.date));
  
  // Get the starting day of the week (0 = Sunday)
  const startDayOfWeek = monthStart.getDay();
  
  return (
    <div className="p-8 max-w-5xl">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-semibold text-white tracking-tight mb-2">Journal</h1>
          <p className="text-zinc-500">
            {journalDocs.length} journal entries
          </p>
        </div>
        <Link
          href="/new?type=journal"
          className="px-4 py-2 bg-indigo-500 text-white rounded-lg hover:bg-indigo-600 transition-colors text-sm font-medium"
        >
          + New Entry
        </Link>
      </div>

      <div className="grid grid-cols-3 gap-8">
        {/* Calendar */}
        <div className="col-span-1">
          <div className="p-4 rounded-xl bg-zinc-900/50 border border-zinc-800/50">
            <h3 className="text-lg font-semibold text-white mb-4">
              {format(today, 'MMMM yyyy')}
            </h3>
            
            {/* Weekday headers */}
            <div className="grid grid-cols-7 gap-1 mb-2">
              {['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'].map((day) => (
                <div key={day} className="text-center text-xs text-zinc-600 font-medium py-1">
                  {day}
                </div>
              ))}
            </div>
            
            {/* Calendar days */}
            <div className="grid grid-cols-7 gap-1">
              {/* Empty cells for days before month starts */}
              {Array.from({ length: startDayOfWeek }).map((_, i) => (
                <div key={`empty-${i}`} className="aspect-square" />
              ))}
              
              {/* Days of the month */}
              {daysInMonth.map((day) => {
                const dateStr = format(day, 'yyyy-MM-dd');
                const hasEntry = journalDates.has(dateStr);
                const isCurrentDay = isToday(day);
                
                return (
                  <div key={dateStr} className="aspect-square">
                    {hasEntry ? (
                      <Link
                        href={`/documents/journal/${dateStr}`}
                        className={`w-full h-full flex items-center justify-center text-sm rounded-lg transition-colors ${
                          isCurrentDay
                            ? 'bg-indigo-500 text-white'
                            : 'bg-indigo-500/20 text-indigo-400 hover:bg-indigo-500/30'
                        }`}
                      >
                        {format(day, 'd')}
                      </Link>
                    ) : (
                      <div
                        className={`w-full h-full flex items-center justify-center text-sm rounded-lg ${
                          isCurrentDay
                            ? 'bg-zinc-700 text-white'
                            : 'text-zinc-600 hover:bg-zinc-800/50'
                        }`}
                      >
                        {format(day, 'd')}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
            
            <div className="mt-4 pt-4 border-t border-zinc-800/50 flex items-center gap-2 text-xs text-zinc-600">
              <span className="w-3 h-3 bg-indigo-500/20 rounded"></span>
              <span>Has entry</span>
            </div>
          </div>
        </div>

        {/* Journal Entries List */}
        <div className="col-span-2">
          <div className="space-y-4">
            {journalDocs.map((doc) => (
              <Link
                key={doc.slug}
                href={`/documents/${doc.slug}`}
                className="block p-5 rounded-xl bg-zinc-900/50 border border-zinc-800/50 hover:border-zinc-700/50 hover:bg-zinc-800/30 transition-all group"
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <span className="text-lg">📝</span>
                      <h3 className="font-medium text-white group-hover:text-indigo-400 transition-colors">
                        {doc.title}
                      </h3>
                    </div>
                    <p className="text-sm text-zinc-500 line-clamp-2">{doc.excerpt}</p>
                    {doc.tags.length > 0 && (
                      <div className="flex gap-1.5 mt-3">
                        {doc.tags.slice(0, 4).map((tag) => (
                          <span
                            key={tag}
                            className="px-1.5 py-0.5 text-xs bg-zinc-800 text-zinc-400 rounded"
                          >
                            {tag}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                  <div className="text-right shrink-0">
                    <span className="text-sm text-zinc-600 font-mono">{doc.date}</span>
                    <p className="text-xs text-zinc-700 mt-1">
                      {format(parseISO(doc.date), 'EEEE')}
                    </p>
                  </div>
                </div>
              </Link>
            ))}
            
            {journalDocs.length === 0 && (
              <div className="p-12 text-center rounded-xl bg-zinc-900/30 border border-zinc-800/50 border-dashed">
                <p className="text-zinc-500 mb-3">No journal entries yet</p>
                <Link
                  href="/new?type=journal"
                  className="text-indigo-400 hover:text-indigo-300 text-sm"
                >
                  Create your first journal entry →
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
