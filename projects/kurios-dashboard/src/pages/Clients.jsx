import { Plus, Copy, Download, Trophy, MapPin, TrendingUp, DollarSign } from 'lucide-react';
import useStore from '../stores/useStore';
import { formatCurrency } from '../utils/helpers';
import { stateData } from '../data/sampleData';

const healthColors = {
  excellent: 'text-kurios-secondary',
  good: 'text-kurios-primary',
  'at-risk': 'text-amber-400',
  critical: 'text-red-400',
};

const gradients = [
  'from-kurios-primary to-blue-400',
  'from-kurios-secondary to-emerald-400',
  'from-kurios-accent to-pink-400',
  'from-amber-500 to-orange-400',
  'from-cyan-500 to-teal-400',
];

export default function Clients() {
  const { clients, addToast, openModal } = useStore();

  const copyPortfolioSummary = () => {
    const summary = `${clients.length} Active Clients • ${stateData.length} States • ${stateData.reduce((s, st) => s + st.casesPerMonth, 0)}+ Cases/Mo`;
    navigator.clipboard.writeText(summary);
    addToast('Portfolio summary copied!', 'success');
  };

  const handleExport = () => {
    const data = clients.map((c) => ({
      name: c.name,
      state: c.state,
      revenue: c.revenue,
      conversion: c.conversion,
      casesPerMonth: c.casesPerMonth,
    }));
    const content = JSON.stringify(data, null, 2);
    const blob = new Blob([content], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'clients-export.json';
    a.click();
    URL.revokeObjectURL(url);
    addToast('Clients exported!', 'success');
  };

  // Group clients by state for summary
  const stateGroups = {};
  clients.forEach((c) => {
    if (!stateGroups[c.state]) stateGroups[c.state] = [];
    stateGroups[c.state].push(c);
  });

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* Hero */}
      <div className="p-6 rounded-2xl bg-gradient-to-br from-kurios-card to-kurios-darker border border-kurios-secondary/20 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-kurios-secondary/5 via-transparent to-transparent pointer-events-none" />

        <div className="relative flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-kurios-secondary/15">
              <Trophy className="w-6 h-6 text-kurios-secondary" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-white">Client Portfolio</h2>
              <p className="text-sm text-gray-400">{stateData.length} states covered</p>
            </div>
          </div>
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => openModal('addClient')}
              className="flex items-center gap-2 px-4 py-2 bg-kurios-primary text-white text-sm font-medium rounded-lg hover:bg-kurios-primary/90 transition-all"
            >
              <Plus className="w-4 h-4" />
              Add Client
            </button>
            <button
              onClick={copyPortfolioSummary}
              className="flex items-center gap-2 px-4 py-2 bg-white/[0.06] text-gray-300 text-sm rounded-lg hover:bg-white/[0.1] border border-kurios-border transition-colors"
            >
              <Copy className="w-4 h-4" />
              Copy
            </button>
            <button
              onClick={handleExport}
              className="flex items-center gap-2 px-4 py-2 bg-white/[0.06] text-gray-300 text-sm rounded-lg hover:bg-white/[0.1] border border-kurios-border transition-colors"
            >
              <Download className="w-4 h-4" />
              Export
            </button>
          </div>
        </div>

        {/* Summary stats */}
        <div className="relative grid grid-cols-2 md:grid-cols-5 gap-3">
          {[
            { value: clients.length, label: 'Active Clients', icon: TrendingUp },
            { value: `${stateData.reduce((s, st) => s + st.casesPerMonth, 0)}+`, label: 'Cases/Month', icon: TrendingUp },
            { value: stateData.length, label: 'States', icon: MapPin },
            { value: '2.6x', label: 'Avg ROI', icon: TrendingUp },
            { value: formatCurrency(stateData.reduce((s, st) => s + st.totalSpend, 0)), label: 'Total Spend', icon: DollarSign },
          ].map((stat, i) => (
            <div key={i} className="p-3.5 rounded-xl bg-white/[0.04] border border-white/[0.06] text-center">
              <p className="text-xl font-bold text-white">{stat.value}</p>
              <p className="text-[11px] text-gray-500 uppercase tracking-wider mt-0.5">{stat.label}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Client Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3 stagger-children">
        {clients.map((client, i) => (
          <div
            key={client.id}
            onClick={() => openModal('viewDetails', client)}
            className="group p-5 rounded-xl border border-kurios-border bg-kurios-card hover:border-kurios-border-hover hover:bg-kurios-card-hover cursor-pointer transition-all duration-200 card-glow"
          >
            <div className="flex items-center gap-3 mb-4">
              <div
                className={`w-11 h-11 rounded-lg flex items-center justify-center font-bold text-base text-white bg-gradient-to-br ${
                  gradients[i % gradients.length]
                } shadow-lg`}
              >
                {client.state}
              </div>
              <div className="flex-1 min-w-0">
                <p className="font-semibold text-sm text-white truncate group-hover:text-kurios-primary transition-colors">
                  {client.name}
                </p>
                <p className="text-xs text-gray-500">
                  {client.casesPerMonth} cases/mo • {client.industry}
                </p>
              </div>
            </div>

            <div className="grid grid-cols-3 gap-3 pt-3 border-t border-kurios-border">
              <div className="text-center">
                <p className="text-sm font-bold text-kurios-primary">${client.revenue}</p>
                <p className="text-[10px] text-gray-600 uppercase">Case $</p>
              </div>
              <div className="text-center">
                <p className="text-sm font-bold text-amber-400">{client.conversion}%</p>
                <p className="text-[10px] text-gray-600 uppercase">Conv.</p>
              </div>
              <div className="text-center">
                <p className="text-sm font-bold text-kurios-secondary">{client.casesPerMonth}</p>
                <p className="text-[10px] text-gray-600 uppercase">Cases/Mo</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
