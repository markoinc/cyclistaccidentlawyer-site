import { useState } from 'react';
import { Plus, Lightbulb, ThumbsUp, ArrowUp, Flame } from 'lucide-react';
import useStore from '../stores/useStore';
import FilterTabs from '../components/UI/FilterTabs';
import SearchInput from '../components/UI/SearchInput';
import { filterBySearch, formatDate } from '../utils/helpers';

export default function Ideas() {
  const { ideas, voteIdea, updateIdea, openModal, settings } = useStore();
  const darkMode = settings.appearance.darkMode;
  const [filter, setFilter] = useState('all');
  const [search, setSearch] = useState('');

  const statusTabs = [
    { value: 'all', label: 'All', count: ideas.length },
    { value: 'backlog', label: 'Backlog', count: ideas.filter(i => i.status === 'backlog').length },
    { value: 'in_review', label: 'In Review', count: ideas.filter(i => i.status === 'in_review').length },
    { value: 'approved', label: 'Approved', count: ideas.filter(i => i.status === 'approved').length },
  ];

  let filteredIdeas = filter === 'all' 
    ? ideas 
    : ideas.filter(i => i.status === filter);

  filteredIdeas = filterBySearch(filteredIdeas, search, ['title', 'description']);

  // Sort by votes (highest first)
  filteredIdeas = [...filteredIdeas].sort((a, b) => b.votes - a.votes);

  const priorityColors = {
    high: 'text-orange-500 bg-orange-500/10 border-orange-500/30',
    medium: 'text-kurios-primary bg-kurios-primary/10 border-kurios-primary/30',
    low: 'text-gray-500 bg-gray-500/10 border-gray-500/30',
  };

  const statusColors = {
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
            <SearchInput 
              value={search} 
              onChange={setSearch} 
              placeholder="Search ideas..." 
            />
          </div>
          <button
            onClick={() => openModal('addIdea')}
            className="flex items-center gap-2 px-4 py-2 bg-kurios-primary text-white rounded-lg hover:bg-kurios-primary/90 transition-colors shadow-lg shadow-kurios-primary/30"
          >
            <Plus className="w-4 h-4" />
            Submit Idea
          </button>
        </div>
      </div>

      {/* Ideas Grid */}
      {filteredIdeas.length === 0 ? (
        <div className={`text-center py-16 ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
          <Lightbulb className="w-16 h-16 mx-auto mb-4 opacity-50" />
          <p className="text-lg font-medium">No ideas found</p>
          <p className="text-sm mt-1">Submit your first idea to get started</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {filteredIdeas.map((idea, index) => (
            <div 
              key={idea.id}
              className={`p-5 rounded-xl border transition-all hover:shadow-lg ${
                darkMode 
                  ? 'bg-gray-800 border-gray-700 hover:border-gray-600' 
                  : 'bg-white border-gray-200 hover:border-gray-300'
              } ${index === 0 ? 'ring-2 ring-kurios-secondary/50' : ''}`}
            >
              {/* Top row */}
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-2">
                  <span className={`w-2 h-2 rounded-full ${statusColors[idea.status]}`} />
                  <span className={`text-xs font-medium ${
                    idea.status === 'approved' ? 'text-kurios-secondary' :
                    idea.status === 'in_review' ? 'text-kurios-primary' :
                    darkMode ? 'text-gray-400' : 'text-gray-500'
                  }`}>
                    {idea.status.replace('_', ' ')}
                  </span>
                </div>
                <span className={`text-xs px-2 py-1 rounded-full border ${priorityColors[idea.priority]}`}>
                  {idea.priority}
                </span>
              </div>

              {/* Title */}
              <h3 className={`font-semibold text-lg mb-2 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                {index === 0 && <Flame className="w-4 h-4 inline mr-2 text-orange-500" />}
                {idea.title}
              </h3>

              {/* Description */}
              <p className={`text-sm mb-4 ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                {idea.description}
              </p>

              {/* Footer */}
              <div className="flex items-center justify-between pt-3 border-t border-gray-200 dark:border-gray-700">
                <span className={`text-xs ${darkMode ? 'text-gray-500' : 'text-gray-400'}`}>
                  {formatDate(idea.createdAt)}
                </span>
                
                <button
                  onClick={() => voteIdea(idea.id)}
                  className={`flex items-center gap-2 px-3 py-1.5 rounded-lg transition-all ${
                    darkMode 
                      ? 'bg-gray-700 hover:bg-kurios-primary/20 text-gray-300 hover:text-kurios-primary' 
                      : 'bg-gray-100 hover:bg-kurios-primary/10 text-gray-600 hover:text-kurios-primary'
                  }`}
                >
                  <ArrowUp className="w-4 h-4" />
                  <span className="font-medium">{idea.votes}</span>
                </button>
              </div>

              {/* Quick status change */}
              {idea.status !== 'approved' && (
                <div className="mt-3 flex gap-2">
                  {idea.status === 'backlog' && (
                    <button
                      onClick={() => updateIdea(idea.id, { status: 'in_review' })}
                      className={`flex-1 text-xs py-2 rounded-lg ${
                        darkMode ? 'bg-gray-700 text-gray-300 hover:bg-kurios-primary/20' : 'bg-gray-100 text-gray-600 hover:bg-kurios-primary/10'
                      } transition-colors`}
                    >
                      Move to Review
                    </button>
                  )}
                  {idea.status === 'in_review' && (
                    <button
                      onClick={() => updateIdea(idea.id, { status: 'approved' })}
                      className="flex-1 text-xs py-2 rounded-lg bg-kurios-secondary/20 text-kurios-secondary hover:bg-kurios-secondary/30 transition-colors"
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
      <div className={`p-6 rounded-xl border ${
        darkMode ? 'bg-gray-800/50 border-gray-700' : 'bg-white border-gray-200'
      }`}>
        <h3 className={`font-semibold mb-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
          Ideas Overview
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          <div>
            <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Total Ideas</p>
            <p className={`text-2xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
              {ideas.length}
            </p>
          </div>
          <div>
            <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Total Votes</p>
            <p className="text-2xl font-bold text-kurios-primary">
              {ideas.reduce((sum, i) => sum + i.votes, 0)}
            </p>
          </div>
          <div>
            <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Approved</p>
            <p className="text-2xl font-bold text-kurios-secondary">
              {ideas.filter(i => i.status === 'approved').length}
            </p>
          </div>
          <div>
            <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>High Priority</p>
            <p className="text-2xl font-bold text-orange-500">
              {ideas.filter(i => i.priority === 'high').length}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
