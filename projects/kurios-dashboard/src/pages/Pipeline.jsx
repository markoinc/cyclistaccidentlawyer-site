import { useState } from 'react';
import { Plus, Download, RefreshCw, FileJson, GripVertical } from 'lucide-react';
import useStore from '../stores/useStore';
import { formatCurrency } from '../utils/helpers';
import { pipelineStages } from '../data/sampleData';

const stages = [
  { id: 'lead', label: 'Lead', color: '#6366f1', bg: 'bg-indigo-500/10' },
  { id: 'qualified', label: 'Qualified', color: '#4F7BFF', bg: 'bg-kurios-primary/10' },
  { id: 'proposal', label: 'Proposal', color: '#F59E0B', bg: 'bg-amber-500/10' },
  { id: 'negotiation', label: 'Negotiation', color: '#A855F7', bg: 'bg-purple-500/10' },
  { id: 'closed', label: 'Closed Won', color: '#00E676', bg: 'bg-kurios-secondary/10' },
];

export default function Pipeline() {
  const { deals, moveDeal, addToast, openModal } = useStore();
  const [draggedCard, setDraggedCard] = useState(null);
  const [dragOverStage, setDragOverStage] = useState(null);

  const getDealsByStage = (stageId) => deals.filter((d) => d.stage === stageId);
  const getStageMargin = (stageId) =>
    getDealsByStage(stageId).reduce(
      (sum, d) => sum + (d.kuriosMargin || d.value * 0.3),
      0
    );

  const handleDragStart = (e, deal) => {
    setDraggedCard(deal);
    e.dataTransfer.effectAllowed = 'move';
  };
  const handleDragOver = (e, stageId) => {
    e.preventDefault();
    setDragOverStage(stageId);
  };
  const handleDragLeave = () => setDragOverStage(null);
  const handleDrop = (e, stageId) => {
    e.preventDefault();
    if (draggedCard && draggedCard.stage !== stageId) {
      moveDeal(draggedCard.id, stageId);
      addToast(
        `Moved ${draggedCard.name} to ${stages.find((s) => s.id === stageId)?.label}`,
        'success'
      );
    }
    setDraggedCard(null);
    setDragOverStage(null);
  };

  const handleExport = (format) => {
    const data = deals.map((d) => ({
      name: d.name,
      company: d.company,
      value: d.value,
      margin: d.kuriosMargin,
      stage: d.stage,
      probability: d.probability,
    }));
    let content, filename, type;
    if (format === 'json') {
      content = JSON.stringify(data, null, 2);
      filename = 'pipeline-export.json';
      type = 'application/json';
    } else {
      const headers = ['Name', 'Company', 'Value', 'Margin', 'Stage', 'Probability'];
      const rows = data.map((d) => [d.name, d.company, d.value, d.margin, d.stage, d.probability]);
      content = [headers, ...rows].map((r) => r.join(',')).join('\n');
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
    addToast(`Exported ${data.length} deals as ${format.toUpperCase()}`, 'success');
  };

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* Actions Bar */}
      <div className="flex flex-wrap items-center gap-3">
        <button
          onClick={() => openModal('addDeal')}
          className="flex items-center gap-2 px-4 py-2.5 bg-kurios-primary text-white text-sm font-medium rounded-lg hover:bg-kurios-primary/90 transition-all shadow-lg shadow-kurios-primary/20"
        >
          <Plus className="w-4 h-4" />
          Add Deal
        </button>
        <button
          onClick={() => handleExport('csv')}
          className="flex items-center gap-2 px-4 py-2.5 bg-white/[0.06] text-gray-300 text-sm font-medium rounded-lg hover:bg-white/[0.1] border border-kurios-border transition-colors"
        >
          <Download className="w-4 h-4" />
          CSV
        </button>
        <button
          onClick={() => handleExport('json')}
          className="flex items-center gap-2 px-4 py-2.5 bg-white/[0.06] text-gray-300 text-sm font-medium rounded-lg hover:bg-white/[0.1] border border-kurios-border transition-colors"
        >
          <FileJson className="w-4 h-4" />
          JSON
        </button>
      </div>

      {/* Kanban Board */}
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
        {stages.map((stage) => {
          const stageDeals = getDealsByStage(stage.id);
          const stageMargin = getStageMargin(stage.id);
          return (
            <div
              key={stage.id}
              className={`rounded-xl min-h-[420px] transition-all duration-200 bg-kurios-card border ${
                dragOverStage === stage.id
                  ? 'border-kurios-primary/50 bg-kurios-primary/5 ring-1 ring-kurios-primary/20'
                  : 'border-kurios-border'
              }`}
              onDragOver={(e) => handleDragOver(e, stage.id)}
              onDragLeave={handleDragLeave}
              onDrop={(e) => handleDrop(e, stage.id)}
            >
              {/* Column Header */}
              <div className="px-4 py-3 border-b border-kurios-border">
                <div className="flex items-center justify-between mb-1">
                  <div className="flex items-center gap-2">
                    <div
                      className="w-2 h-2 rounded-full"
                      style={{ backgroundColor: stage.color }}
                    />
                    <span className="text-xs font-semibold uppercase tracking-wider text-gray-300">
                      {stage.label}
                    </span>
                  </div>
                  <span className="text-xs font-medium text-gray-500 bg-white/[0.06] px-2 py-0.5 rounded-full">
                    {stageDeals.length}
                  </span>
                </div>
                <p className="text-xs text-gray-500">
                  {formatCurrency(stageMargin)} margin
                </p>
              </div>

              {/* Cards */}
              <div className="p-3 space-y-2.5">
                {stageDeals.map((deal) => (
                  <div
                    key={deal.id}
                    draggable
                    onDragStart={(e) => handleDragStart(e, deal)}
                    onClick={() => openModal('viewDetails', deal)}
                    className={`group p-3.5 rounded-lg border cursor-pointer transition-all duration-150 hover:-translate-y-0.5 hover:shadow-lg hover:shadow-black/20 card-glow ${
                      stage.id === 'closed'
                        ? 'border-kurios-secondary/30 bg-kurios-secondary/[0.04]'
                        : 'border-kurios-border hover:border-kurios-border-hover bg-kurios-darker/60'
                    } ${draggedCard?.id === deal.id ? 'opacity-40 rotate-1 scale-[1.02]' : ''}`}
                  >
                    <div className="flex items-start justify-between mb-1.5">
                      <p className="font-medium text-sm text-white leading-tight">
                        {deal.name}
                      </p>
                      <p className="text-sm font-semibold text-kurios-secondary whitespace-nowrap ml-2">
                        {formatCurrency(deal.kuriosMargin || deal.value * 0.3)}
                      </p>
                    </div>
                    <p className="text-xs text-gray-500 mb-2">
                      {deal.company} • {deal.state}
                    </p>
                    <div className="flex items-center justify-between">
                      <span className="text-[11px] text-gray-500 truncate max-w-[120px]">
                        {deal.nextAction}
                      </span>
                      <span
                        className={`text-[11px] font-semibold px-1.5 py-0.5 rounded ${
                          deal.probability >= 75
                            ? 'bg-kurios-secondary/15 text-kurios-secondary'
                            : deal.probability >= 50
                            ? 'bg-kurios-primary/15 text-kurios-primary'
                            : deal.probability >= 25
                            ? 'bg-amber-500/15 text-amber-400'
                            : 'bg-gray-500/15 text-gray-400'
                        }`}
                      >
                        {deal.probability}%
                      </span>
                    </div>
                  </div>
                ))}

                {stageDeals.length === 0 && (
                  <div className="text-center py-10 text-gray-600 text-xs">
                    No deals in this stage
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
