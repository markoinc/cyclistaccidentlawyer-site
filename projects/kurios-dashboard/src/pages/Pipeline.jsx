import { useState } from 'react';
import { Plus, Download, RefreshCw, FileJson } from 'lucide-react';
import { useDashboard } from '../context/DashboardContext';
import { Button, ProbabilityBadge } from '../components/UI';

const stages = [
  { id: 'lead', label: 'Lead', color: 'border-[#6e7681]' },
  { id: 'qualified', label: 'Qualified', color: 'border-[#3366FF]' },
  { id: 'proposal', label: 'Proposal', color: 'border-[#ffb347]' },
  { id: 'negotiation', label: 'Negotiation', color: 'border-[#a855f7]' },
  { id: 'closed', label: 'Closed Won', color: 'border-[#00E676]' },
];

export function Pipeline() {
  const { state, dispatch, showToast } = useDashboard();
  const [draggedCard, setDraggedCard] = useState(null);
  const [dragOverStage, setDragOverStage] = useState(null);

  const getProspectsByStage = (stageId) => 
    state.prospects.filter(p => p.stage === stageId);

  const getStageValue = (stageId) => 
    getProspectsByStage(stageId).reduce((sum, p) => sum + p.amount, 0);

  const handleDragStart = (e, prospect) => {
    setDraggedCard(prospect);
    e.dataTransfer.effectAllowed = 'move';
  };

  const handleDragOver = (e, stageId) => {
    e.preventDefault();
    setDragOverStage(stageId);
  };

  const handleDragLeave = () => {
    setDragOverStage(null);
  };

  const handleDrop = (e, stageId) => {
    e.preventDefault();
    if (draggedCard && draggedCard.stage !== stageId) {
      dispatch({ type: 'MOVE_PROSPECT', payload: { id: draggedCard.id, stage: stageId } });
      showToast(`Moved ${draggedCard.name} to ${stages.find(s => s.id === stageId)?.label}`, 'success');
    }
    setDraggedCard(null);
    setDragOverStage(null);
  };

  const handleExport = (format) => {
    const data = state.prospects.map(p => ({
      name: p.name,
      company: p.company,
      amount: p.amount,
      stage: p.stage,
      probability: p.probability,
    }));

    let content, filename, type;
    if (format === 'json') {
      content = JSON.stringify(data, null, 2);
      filename = 'pipeline-export.json';
      type = 'application/json';
    } else {
      const headers = ['Name', 'Company', 'Amount', 'Stage', 'Probability'];
      const rows = data.map(p => [p.name, p.company, p.amount, p.stage, p.probability]);
      content = [headers, ...rows].map(r => r.join(',')).join('\n');
      filename = 'pipeline-export.csv';
      type = 'text/csv';
    }

    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
    showToast(`Exported ${data.length} prospects as ${format.toUpperCase()}`, 'success');
  };

  const handleSync = () => {
    showToast('Syncing with CRM...', 'info');
    setTimeout(() => showToast('CRM sync complete!', 'success'), 1500);
  };

  return (
    <div className="p-6 animate-fadeIn">
      {/* Actions Bar */}
      <div className="flex flex-wrap gap-3 mb-6">
        <Button onClick={() => dispatch({ type: 'OPEN_MODAL', payload: { type: 'addProspect' } })}>
          <Plus size={16} /> Add Prospect
        </Button>
        <Button variant="secondary" onClick={() => handleExport('csv')}>
          <Download size={16} /> Export CSV
        </Button>
        <Button variant="secondary" onClick={() => handleExport('json')}>
          <FileJson size={16} /> Export JSON
        </Button>
        <Button variant="outline" onClick={handleSync}>
          <RefreshCw size={16} /> Sync CRM
        </Button>
      </div>

      {/* Kanban Board */}
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
        {stages.map(stage => (
          <div
            key={stage.id}
            className={`
              bg-[#21262c] rounded-xl p-4 min-h-[400px] transition-all duration-200
              ${dragOverStage === stage.id ? 'ring-2 ring-[#3366FF] ring-dashed bg-[#353d47]' : ''}
            `}
            onDragOver={(e) => handleDragOver(e, stage.id)}
            onDragLeave={handleDragLeave}
            onDrop={(e) => handleDrop(e, stage.id)}
          >
            {/* Column Header */}
            <div className={`flex items-center justify-between mb-4 pb-3 border-b-2 ${stage.color}`}>
              <div>
                <div className="text-sm font-semibold uppercase tracking-wide">{stage.label}</div>
                <div className="text-xs text-[#6e7681]">
                  {getProspectsByStage(stage.id).length} deals • ${getStageValue(stage.id).toLocaleString()}
                </div>
              </div>
              <span className="bg-[#353d47] px-2 py-0.5 rounded-full text-xs font-semibold">
                {getProspectsByStage(stage.id).length}
              </span>
            </div>

            {/* Cards */}
            <div className="space-y-3">
              {getProspectsByStage(stage.id).map(prospect => (
                <div
                  key={prospect.id}
                  draggable
                  onDragStart={(e) => handleDragStart(e, prospect)}
                  onClick={() => dispatch({ type: 'OPEN_MODAL', payload: { type: 'viewProspect', data: prospect } })}
                  className={`
                    bg-[#242930] border rounded-lg p-3.5 cursor-pointer
                    transition-all duration-150 hover:border-[#3366FF] hover:shadow-md
                    ${stage.id === 'closed' ? 'border-[#00E676]' : 'border-[#2d333b]'}
                    ${draggedCard?.id === prospect.id ? 'opacity-50 rotate-2' : ''}
                  `}
                >
                  <div className="flex items-start justify-between mb-2">
                    <div className="font-semibold text-sm">{prospect.name}</div>
                    <div className="text-sm font-semibold text-[#00E676]">
                      ${prospect.amount.toLocaleString()}
                    </div>
                  </div>
                  <div className="text-xs text-[#6e7681] mb-3">{prospect.company}</div>
                  <div className="flex items-center justify-between">
                    <div className={`
                      w-6 h-6 rounded-full flex items-center justify-center text-[10px] font-semibold
                      ${stage.id === 'closed' ? 'bg-[#00E676] text-[#14171A]' : 'gradient-brand text-white'}
                    `}>
                      {prospect.avatar}
                    </div>
                    <ProbabilityBadge probability={prospect.probability} />
                  </div>
                </div>
              ))}

              {getProspectsByStage(stage.id).length === 0 && (
                <div className="text-center py-8 text-[#6e7681] text-sm">
                  No deals in this stage
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Pipeline;
