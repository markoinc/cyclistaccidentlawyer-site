import { useState } from 'react';
import { Plus, Lightbulb, ArrowUp, Flame } from 'lucide-react';
import useStore from '../stores/useStore';
import FilterTabs from '../components/UI/FilterTabs';
import SearchInput from '../components/UI/SearchInput';
import { filterBySearch, formatDate } from '../utils/helpers';

export default function Ideas() {
  const { ideas, voteIdea, updateIdea, openModal } = useStore();
  const [filter, setFilter] = useState('all');
  const [search, setSearch] = useState('');

  const statusTabs = [
    { value: 'all', label: 'All', count: ideas.length },
    { value: 'backlog', label: 'Backlog', count: ideas.filter((i) => i.status === 'backlog').length },
    { value: 'in_review', label: 'In Review', count: ideas.filter((i) => i.status === 'in_review').length },
    { value: 'approved', label: 'Approved', count: ideas.filter((i) => i.status === 'approved').length },
  ];

  let filteredIdeas =
    filter === 'all' ? ideas : ideas.filter((i) => i.status === filter);
  filteredIdeas = filterBySearch(filteredIdeas, search, ['title', 'description']);
  filteredIdeas = [...filteredIdeas].sort((a, b) => b.votes - a.votes);

  const priorityColors = {
    high: 'text-amber-400 bg-amber-500/10 border-amber-500/20',
    medium: 'text-kurios-primary bg-kurios-primary/10 border-kurios-primary/20',
    low: 'text-gray-500 bg-white/[0.04] border-white/[0.06]',
  };

  const statusDot = {
    backlog: 'bg-gray-500',
    in_review: 'bg-kurios-primary',
    approved: 'bg-kurios-secondary',
  };

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <FilterTabs tabs={statusTabs} activeTab={filter} onChange={setFilter} />
        <div className="flex items-center gap-3">
          <div className="w-64">
            <SearchInput value={search} onChange={setSearch} placeholder="Search ideas…" />
          </div>
          <button
            onClick={() => openModal('addIdea')}
            className="flex items-center gap-2 px-4 py-2.5 bg-kurios-primary text-white text-sm font-medium rounded-lg hover:bg-kurios-primary/90 transition-all shadow-lg shadow-kurios-primary/20"
          >
            <Plus className="w-4 h-4" />
            Submit Idea
          </button>
        </div>
      </div>

      {/* Ideas Grid */}
      {filteredIdeas.length === 0 ? (
        <div className="text-center py-20 text-gray-500">
          <Lightbulb className="w-14 h-14 mx-auto mb-4 opacity-30" />
          <p className="text-lg font-medium mb-1">No ideas found</p>
          <p className="text-sm">Submit your first idea to get started</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 stagger-children">
          {filteredIdeas.map((idea, index) => (
            <div
              key={idea.id}
              className={`group p-5 rounded-xl border transition-all duration-200 card-glow ${
                index === 0
                  ? 'border-kurios-secondary/30 bg-kurios-secondary/[0.03]'
                  : 'border-kurios-border bg-kurios-card hover:border-kurios-border-hover hover:bg-kurios-card-hover'
              }`}
            >
              {/* Status + priority */}
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                  <span className={`w-2 h-2 rounded-full ${statusDot[idea.status]}`} />
                  <span
                    className={`text-[11px] font-medium ${
                      idea.status === 'approved'
                        ? 'text-kurios-secondary'
                        : idea.status === 'in_review'
                        ? 'text-kurios-primary'
                        : 'text-gray-500'
                    }`}
                  >
                    {idea.status.replace('_', ' ')}
                  </span>
                </div>
                <span className={`text-[10px] px-2 py-0.5 rounded-full border ${priorityColors[idea.priority]}`}>
                  {idea.priority}
                </span>
              </div>

              {/* Title */}
              <h3 className="font-semibold text-[15px] text-white mb-1.5 leading-tight">
                {index === 0 && <Flame className="w-4 h-4 inline mr-1.5 text-orange-400" />}
                {idea.title}
              </h3>

              {/* Description */}
              <p className="text-sm text-gray-400 mb-4 line-clamp-2 leading-relaxed">
                {idea.description}
              </p>

              {/* Footer */}
              <div className="flex items-center justify-between pt-3 border-t border-kurios-border">
                <span className="text-[11px] text-gray-600">{formatDate(idea.createdAt)}</span>
                <button
                  onClick={() => voteIdea(idea.id)}
                  className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-white/[0.04] hover:bg-kurios-primary/15 text-gray-400 hover:text-kurios-primary transition-all"
                >
                  <ArrowUp className="w-3.5 h-3.5" />
                  <span className="text-xs font-medium">{idea.votes}</span>
                </button>
              </div>

              {/* Quick status change */}
              {idea.status !== 'approved' && (
                <div className="mt-3">
                  {idea.status === 'backlog' && (
                    <button
                      onClick={() => updateIdea(idea.id, { status: 'in_review' })}
                      className="w-full text-xs py-2 rounded-lg bg-white/[0.04] text-gray-400 hover:bg-kurios-primary/10 hover:text-kurios-primary transition-colors"
                    >
                      Move to Review
                    </button>
                  )}
                  {idea.status === 'in_review' && (
                    <button
                      onClick={() => updateIdea(idea.id, { status: 'approved' })}
                      className="w-full text-xs py-2 rounded-lg bg-kurios-secondary/10 text-kurios-secondary hover:bg-kurios-secondary/20 transition-colors"
                    >
                      Approve
                    </button>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Stats */}
      <div className="p-5 rounded-xl border border-kurios-border bg-kurios-card">
        <h3 className="font-semibold text-white mb-4">Ideas Overview</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          {[
            { label: 'Total Ideas', value: ideas.length, color: 'text-white' },
            { label: 'Total Votes', value: ideas.reduce((sum, i) => sum + i.votes, 0), color: 'text-kurios-primary' },
            { label: 'Approved', value: ideas.filter((i) => i.status === 'approved').length, color: 'text-kurios-secondary' },
            { label: 'High Priority', value: ideas.filter((i) => i.priority === 'high').length, color: 'text-amber-400' },
          ].map((stat) => (
            <div key={stat.label}>
              <p className="text-xs text-gray-500">{stat.label}</p>
              <p className={`text-2xl font-bold ${stat.color}`}>{stat.value}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
