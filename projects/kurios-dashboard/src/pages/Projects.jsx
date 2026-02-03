import { Plus, Filter, Download } from 'lucide-react';
import { useDashboard } from '../context/DashboardContext';
import { Button, StatusPill, PriorityBadge } from '../components/UI';

const priorityColors = {
  p0: 'bg-[#ff6b6b]',
  p1: 'bg-[#ffb347]',
  p2: 'bg-[#3366FF]',
  p3: 'bg-[#6e7681]',
};

const progressColors = {
  high: 'bg-[#00E676]',
  medium: 'bg-[#3366FF]',
  low: 'bg-[#ffb347]',
};

export function Projects() {
  const { state, dispatch, showToast } = useDashboard();

  const handleExport = () => {
    const data = state.projects.map(p => ({
      name: p.name,
      description: p.description,
      status: p.status,
      priority: p.priority,
      progress: p.progress,
      due: p.due,
    }));
    const content = JSON.stringify(data, null, 2);
    const blob = new Blob([content], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'projects-export.json';
    a.click();
    URL.revokeObjectURL(url);
    showToast('Projects exported!', 'success');
  };

  return (
    <div className="p-6 animate-fadeIn">
      {/* Actions Bar */}
      <div className="flex flex-wrap gap-3 mb-6">
        <Button onClick={() => dispatch({ type: 'OPEN_MODAL', payload: { type: 'addProject' } })}>
          <Plus size={16} /> New Project
        </Button>
        <Button variant="secondary" onClick={() => showToast('Filter options coming soon', 'info')}>
          <Filter size={16} /> Filter
        </Button>
        <Button variant="outline" onClick={handleExport}>
          <Download size={16} /> Export
        </Button>
      </div>

      {/* Projects Table */}
      <div className="bg-[#242930] border border-[#2d333b] rounded-xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="bg-[#21262c] text-[11px] font-semibold text-[#6e7681] uppercase tracking-wider">
                <th className="text-left px-5 py-3">Project</th>
                <th className="text-left px-5 py-3">Status</th>
                <th className="text-left px-5 py-3">Priority</th>
                <th className="text-left px-5 py-3">Progress</th>
                <th className="text-left px-5 py-3">Assignees</th>
                <th className="text-left px-5 py-3">Due</th>
                <th className="text-left px-5 py-3">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#2d333b]">
              {state.projects.map(project => (
                <tr 
                  key={project.id} 
                  className="hover:bg-[#353d47] transition-colors cursor-pointer"
                  onClick={() => dispatch({ type: 'OPEN_MODAL', payload: { type: 'viewProject', data: project } })}
                >
                  <td className="px-5 py-4">
                    <div className="flex items-center gap-3">
                      <div className={`w-1 h-8 rounded ${priorityColors[project.priority]}`} />
                      <div>
                        <div className="font-semibold">{project.name}</div>
                        <div className="text-xs text-[#6e7681]">{project.description}</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-5 py-4">
                    <StatusPill status={project.status} />
                  </td>
                  <td className="px-5 py-4">
                    <span className={`font-semibold ${
                      project.priority === 'p0' ? 'text-[#ff6b6b]' :
                      project.priority === 'p1' ? 'text-[#ffb347]' : 'text-[#3366FF]'
                    }`}>
                      {project.priority.toUpperCase()}
                    </span>
                  </td>
                  <td className="px-5 py-4">
                    <div className="w-full max-w-[120px]">
                      <div className="h-2 bg-[#353d47] rounded-full overflow-hidden">
                        <div
                          className={`h-full rounded-full ${
                            project.progress >= 75 ? progressColors.high :
                            project.progress >= 50 ? progressColors.medium : progressColors.low
                          }`}
                          style={{ width: `${project.progress}%` }}
                        />
                      </div>
                      <div className="text-xs text-[#6e7681] mt-1">{project.progress}%</div>
                    </div>
                  </td>
                  <td className="px-5 py-4">
                    <div className="flex -space-x-2">
                      {project.assignees.map((assignee, i) => (
                        <div
                          key={i}
                          className={`
                            w-7 h-7 rounded-full flex items-center justify-center text-[10px] font-semibold
                            border-2 border-[#242930]
                            ${assignee === 'AI' ? 'bg-[#a855f7] text-white' : 'gradient-brand text-white'}
                          `}
                        >
                          {assignee}
                        </div>
                      ))}
                    </div>
                  </td>
                  <td className="px-5 py-4 text-sm text-[#6e7681]">{project.due}</td>
                  <td className="px-5 py-4" onClick={(e) => e.stopPropagation()}>
                    <div className="flex gap-2">
                      <Button
                        size="sm"
                        variant={project.status === 'in-progress' ? 'primary' : 'ghost'}
                        onClick={() => dispatch({ type: 'OPEN_MODAL', payload: { type: 'editProject', data: project } })}
                      >
                        {project.status === 'in-progress' ? 'Continue' : 'Open'}
                      </Button>
                      <Button
                        size="sm"
                        variant="ghost"
                        className="text-[#ff6b6b] hover:bg-[#ff6b6b]/10"
                        onClick={() => dispatch({ type: 'OPEN_MODAL', payload: { type: 'deleteProject', data: project } })}
                      >
                        Delete
                      </Button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default Projects;
