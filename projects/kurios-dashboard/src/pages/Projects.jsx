import { Plus, Filter, Download, CheckCircle2, Circle, Clock } from 'lucide-react';
import useStore from '../stores/useStore';
import { formatDate } from '../utils/helpers';

const priorityConfig = {
  p0: { label: 'P0', color: 'text-red-400', dot: 'bg-red-400' },
  p1: { label: 'P1', color: 'text-amber-400', dot: 'bg-amber-400' },
  p2: { label: 'P2', color: 'text-kurios-primary', dot: 'bg-kurios-primary' },
  p3: { label: 'P3', color: 'text-gray-500', dot: 'bg-gray-500' },
};

const statusConfig = {
  'in_progress': { label: 'In Progress', color: 'bg-kurios-primary/15 text-kurios-primary' },
  'in-progress': { label: 'In Progress', color: 'bg-kurios-primary/15 text-kurios-primary' },
  completed: { label: 'Completed', color: 'bg-kurios-secondary/15 text-kurios-secondary' },
  planning: { label: 'Planning', color: 'bg-amber-500/15 text-amber-400' },
  paused: { label: 'Paused', color: 'bg-gray-500/15 text-gray-400' },
};

export default function Projects() {
  const { projects, addToast, openModal } = useStore();

  const handleExport = () => {
    const data = projects.map((p) => ({
      name: p.name,
      description: p.description,
      status: p.status,
      progress: p.progress,
      dueDate: p.dueDate,
    }));
    const content = JSON.stringify(data, null, 2);
    const blob = new Blob([content], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'projects-export.json';
    a.click();
    URL.revokeObjectURL(url);
    addToast('Projects exported!', 'success');
  };

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* Actions */}
      <div className="flex flex-wrap items-center gap-3">
        <button
          onClick={() => openModal('addProject')}
          className="flex items-center gap-2 px-4 py-2.5 bg-kurios-primary text-white text-sm font-medium rounded-lg hover:bg-kurios-primary/90 transition-all shadow-lg shadow-kurios-primary/20"
        >
          <Plus className="w-4 h-4" />
          New Project
        </button>
        <button
          onClick={handleExport}
          className="flex items-center gap-2 px-4 py-2.5 bg-white/[0.06] text-gray-300 text-sm font-medium rounded-lg hover:bg-white/[0.1] border border-kurios-border transition-colors"
        >
          <Download className="w-4 h-4" />
          Export
        </button>
      </div>

      {/* Projects Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-4 stagger-children">
        {projects.map((project) => {
          const status = statusConfig[project.status] || statusConfig.planning;
          const completedTasks = project.tasks?.filter((t) => t.completed).length || 0;
          const totalTasks = project.tasks?.length || 0;
          const pct = project.progress || 0;

          return (
            <div
              key={project.id}
              onClick={() => openModal('viewDetails', project)}
              className="group p-5 rounded-xl border border-kurios-border bg-kurios-card hover:border-kurios-border-hover hover:bg-kurios-card-hover cursor-pointer transition-all duration-200 card-glow"
            >
              {/* Top row */}
              <div className="flex items-start justify-between mb-3">
                <div className="flex-1 min-w-0">
                  <h3 className="font-semibold text-white text-[15px] leading-tight truncate group-hover:text-kurios-primary transition-colors">
                    {project.name}
                  </h3>
                  <p className="text-xs text-gray-500 mt-1 line-clamp-1">
                    {project.description}
                  </p>
                </div>
                <span
                  className={`shrink-0 ml-3 text-[11px] font-medium px-2.5 py-1 rounded-full ${status.color}`}
                >
                  {status.label}
                </span>
              </div>

              {/* Progress bar */}
              <div className="mb-3">
                <div className="flex items-center justify-between text-xs mb-1.5">
                  <span className="text-gray-500">
                    {completedTasks}/{totalTasks} tasks
                  </span>
                  <span className={`font-medium ${pct >= 75 ? 'text-kurios-secondary' : pct >= 50 ? 'text-kurios-primary' : 'text-amber-400'}`}>
                    {pct}%
                  </span>
                </div>
                <div className="h-1.5 bg-white/[0.06] rounded-full overflow-hidden">
                  <div
                    className={`h-full rounded-full transition-all duration-500 ${
                      pct >= 75
                        ? 'bg-gradient-to-r from-kurios-secondary to-emerald-400'
                        : pct >= 50
                        ? 'bg-gradient-to-r from-kurios-primary to-blue-400'
                        : 'bg-gradient-to-r from-amber-500 to-orange-400'
                    }`}
                    style={{ width: `${pct}%` }}
                  />
                </div>
              </div>

              {/* Tasks preview */}
              {project.tasks && project.tasks.length > 0 && (
                <div className="space-y-1.5 mb-3">
                  {project.tasks.slice(0, 3).map((task) => (
                    <div key={task.id} className="flex items-center gap-2 text-xs">
                      {task.completed ? (
                        <CheckCircle2 className="w-3.5 h-3.5 text-kurios-secondary shrink-0" />
                      ) : (
                        <Circle className="w-3.5 h-3.5 text-gray-600 shrink-0" />
                      )}
                      <span className={task.completed ? 'text-gray-500 line-through' : 'text-gray-400'}>
                        {task.name}
                      </span>
                    </div>
                  ))}
                  {project.tasks.length > 3 && (
                    <p className="text-[11px] text-gray-600 pl-5">
                      +{project.tasks.length - 3} more
                    </p>
                  )}
                </div>
              )}

              {/* Footer */}
              <div className="flex items-center justify-between pt-3 border-t border-kurios-border">
                <div className="flex items-center gap-1.5 text-xs text-gray-500">
                  <Clock className="w-3.5 h-3.5" />
                  <span>Due {project.dueDate || 'TBD'}</span>
                </div>
                {project.client && (
                  <span className="text-[11px] text-gray-600">{project.client}</span>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {projects.length === 0 && (
        <div className="text-center py-16 text-gray-500">
          <p className="text-lg font-medium mb-1">No projects yet</p>
          <p className="text-sm">Create your first project to get started</p>
        </div>
      )}
    </div>
  );
}
