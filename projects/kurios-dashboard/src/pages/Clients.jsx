import { Plus, Copy, Download, Trophy } from 'lucide-react';
import { useDashboard } from '../context/DashboardContext';
import { Button, Badge } from '../components/UI';

const healthColors = {
  excellent: 'bg-[#00E676]/15 text-[#00E676]',
  good: 'bg-[#3366FF]/15 text-[#3366FF]',
  'at-risk': 'bg-[#ffb347]/15 text-[#ffb347]',
  critical: 'bg-[#ff6b6b]/15 text-[#ff6b6b]',
};

const gradients = [
  'from-[#3366FF] to-[#00E676]',
  'from-[#ff6b6b] to-[#ffb347]',
  'from-[#a855f7] to-[#3366FF]',
  'from-[#00E676] to-[#3366FF]',
];

export function Clients() {
  const { state, dispatch, showToast } = useDashboard();

  const copyPortfolioSummary = () => {
    const summary = '24 Active Clients • $10M+ Total Spend • 5,000+ Cases Signed • 15 States • 5+ Years';
    navigator.clipboard.writeText(summary);
    showToast('Portfolio summary copied!', 'success');
  };

  const handleExport = () => {
    const data = state.clients.map(c => ({
      state: c.state,
      name: c.name,
      clients: c.clients,
      roi: c.roi,
      leadCost: c.leadCost,
      caseCost: c.caseCost,
      conversion: c.conversion,
    }));
    const content = JSON.stringify(data, null, 2);
    const blob = new Blob([content], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'clients-export.json';
    a.click();
    URL.revokeObjectURL(url);
    showToast('Clients exported!', 'success');
  };

  return (
    <div className="p-6 animate-fadeIn">
      {/* Hero Section */}
      <div className="bg-gradient-to-br from-[#242930] to-[#21262c] border border-[#00E676] rounded-2xl p-6 mb-6">
        <div className="flex flex-wrap items-center justify-between gap-4 mb-6">
          <div className="flex items-center gap-3">
            <Trophy size={24} className="text-[#00E676]" />
            <h2 className="text-xl font-bold">Client Portfolio — 15+ States Covered</h2>
          </div>
          <div className="flex gap-2">
            <Button onClick={() => dispatch({ type: 'OPEN_MODAL', payload: { type: 'addClient' } })}>
              <Plus size={16} /> Add Client
            </Button>
            <Button variant="secondary" onClick={copyPortfolioSummary}>
              <Copy size={16} /> Copy Summary
            </Button>
            <Button variant="outline" onClick={handleExport}>
              <Download size={16} /> Export
            </Button>
          </div>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          {[
            { value: '24', label: 'Active Clients', positive: true },
            { value: '$10M+', label: 'Total Spend', positive: true },
            { value: '5,000+', label: 'Cases Signed', positive: true },
            { value: '2.6x', label: 'Avg Client ROI', positive: true },
            { value: '5+ Years', label: 'Track Record', positive: false },
          ].map((stat, i) => (
            <div key={i} className="text-center p-4 bg-[#14171A] rounded-lg">
              <div className={`text-2xl font-extrabold ${stat.positive ? 'text-[#00E676]' : 'text-[#f0f6fc]'}`}>
                {stat.value}
              </div>
              <div className="text-xs text-[#6e7681] uppercase tracking-wide">{stat.label}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Client Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {state.clients.map((client, i) => (
          <div
            key={client.id}
            className={`
              bg-[#242930] border rounded-xl p-5 cursor-pointer
              transition-all duration-150 hover:border-[#3366FF] hover:shadow-lg hover:shadow-[#3366FF]/10 hover:-translate-y-0.5
              ${client.favorite ? 'border-[#3366FF]' : 'border-[#2d333b]'}
            `}
            onClick={() => dispatch({ type: 'OPEN_MODAL', payload: { type: 'viewClient', data: client } })}
          >
            <div className="flex items-center gap-3 mb-4">
              <div className={`
                w-12 h-12 rounded-lg flex items-center justify-center font-bold text-lg text-white
                bg-gradient-to-br ${gradients[i % gradients.length]}
              `}>
                {client.state}
              </div>
              <div className="flex-1 min-w-0">
                <div className="font-semibold truncate">{client.name}</div>
                <div className="text-xs text-[#6e7681]">
                  {client.favorite ? '⭐ FAVORITE - 100+ cases/mo' : `${client.clients} Active Clients`}
                </div>
              </div>
              <span className={`px-2.5 py-1 rounded-full text-xs font-semibold ${healthColors[client.health]}`}>
                {client.roi} ROI
              </span>
            </div>

            <div className="grid grid-cols-3 gap-3 pt-4 border-t border-[#2d333b]">
              <div className="text-center">
                <div className="text-base font-bold text-[#3366FF]">${client.leadCost}</div>
                <div className="text-[10px] text-[#6e7681] uppercase">Lead Cost</div>
              </div>
              <div className="text-center">
                <div className="text-base font-bold text-[#ffb347]">${client.caseCost.toLocaleString()}</div>
                <div className="text-[10px] text-[#6e7681] uppercase">Case Cost</div>
              </div>
              <div className="text-center">
                <div className="text-base font-bold text-[#00E676]">
                  {typeof client.conversion === 'number' && client.conversion > 50 ? '100+' : `${client.conversion}%`}
                </div>
                <div className="text-[10px] text-[#6e7681] uppercase">
                  {typeof client.conversion === 'number' && client.conversion > 50 ? 'Cases/Mo' : 'Conversion'}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Clients;
