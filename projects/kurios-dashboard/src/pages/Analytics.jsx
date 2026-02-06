import {
  BarChart, Bar, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
} from 'recharts';
import { Target, DollarSign, Phone, MapPin, Music } from 'lucide-react';
import useStore from '../stores/useStore';
import { GOAL, stateData, milestones, callData } from '../data/sampleData';
import { formatCurrency } from '../utils/helpers';

const chartTooltipStyle = {
  backgroundColor: '#181C26',
  border: '1px solid #1E2330',
  borderRadius: '10px',
  boxShadow: '0 8px 32px rgba(0,0,0,0.4)',
  padding: '10px 14px',
};

export default function Analytics() {
  const { deals } = useStore();

  const closedDeals = deals.filter((d) => d.stage === 'closed');
  const kuriosMargin = closedDeals.reduce(
    (sum, d) => sum + (d.kuriosMargin || d.value * 0.3),
    0
  );
  const pipelineDeals = deals.filter((d) => d.stage !== 'closed');
  const weightedPipeline = pipelineDeals.reduce(
    (sum, d) => sum + d.value * (d.probability / 100),
    0
  );
  const weightedMargin = weightedPipeline * GOAL.margin;
  const goalProgress = (kuriosMargin / GOAL.total) * 100;

  const pipelineByStage = [
    { name: 'Lead', value: deals.filter((d) => d.stage === 'lead').reduce((s, d) => s + (d.kuriosMargin || d.value * 0.3), 0), deals: deals.filter((d) => d.stage === 'lead').length, color: '#6366f1' },
    { name: 'Qualified', value: deals.filter((d) => d.stage === 'qualified').reduce((s, d) => s + (d.kuriosMargin || d.value * 0.3), 0), deals: deals.filter((d) => d.stage === 'qualified').length, color: '#4F7BFF' },
    { name: 'Proposal', value: deals.filter((d) => d.stage === 'proposal').reduce((s, d) => s + (d.kuriosMargin || d.value * 0.3), 0), deals: deals.filter((d) => d.stage === 'proposal').length, color: '#F59E0B' },
    { name: 'Negotiation', value: deals.filter((d) => d.stage === 'negotiation').reduce((s, d) => s + (d.kuriosMargin || d.value * 0.3), 0), deals: deals.filter((d) => d.stage === 'negotiation').length, color: '#A855F7' },
    { name: 'Closed', value: deals.filter((d) => d.stage === 'closed').reduce((s, d) => s + (d.kuriosMargin || d.value * 0.3), 0), deals: deals.filter((d) => d.stage === 'closed').length, color: '#00E676' },
  ];

  const priorityData = [
    { name: 'High', value: deals.filter((d) => d.priority === 'high' && d.stage !== 'closed').length, color: '#EF4444' },
    { name: 'Medium', value: deals.filter((d) => d.priority === 'medium' && d.stage !== 'closed').length, color: '#F59E0B' },
    { name: 'Low', value: deals.filter((d) => d.priority === 'low' && d.stage !== 'closed').length, color: '#6B7280' },
  ];

  const milestonesWithProgress = milestones.map((m) => ({
    ...m,
    achieved: kuriosMargin >= m.amount,
  }));

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* Goal Tracker Hero */}
      <div className="p-6 rounded-2xl border border-kurios-primary/25 bg-gradient-to-br from-kurios-primary/[0.08] via-kurios-accent/[0.04] to-transparent relative overflow-hidden">
        <div className="absolute -top-24 -right-24 w-64 h-64 bg-kurios-primary/10 rounded-full blur-3xl pointer-events-none" />

        <div className="relative flex items-center gap-4 mb-6">
          <div className="p-3 rounded-xl bg-gradient-to-br from-kurios-primary to-kurios-accent shadow-lg shadow-kurios-primary/20">
            <Music className="w-7 h-7 text-white" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-white">$9.6M Goal Tracker</h2>
            <p className="text-sm text-gray-400">Exit by Dec 2026 → Full-time music</p>
          </div>
        </div>

        <div className="relative grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
          {[
            { label: 'Earned (30%)', value: formatCurrency(kuriosMargin), color: 'text-kurios-secondary' },
            { label: 'Pipeline (30%)', value: formatCurrency(weightedMargin), color: 'text-kurios-primary' },
            { label: 'Progress', value: `${goalProgress.toFixed(2)}%`, color: 'text-white' },
            { label: 'Remaining', value: formatCurrency(GOAL.total - kuriosMargin), color: 'text-amber-400' },
          ].map((m) => (
            <div key={m.label} className="p-4 rounded-xl bg-white/[0.04] border border-white/[0.06]">
              <p className="text-xs text-gray-500">{m.label}</p>
              <p className={`text-xl font-bold mt-1 tabular-nums ${m.color}`}>{m.value}</p>
            </div>
          ))}
        </div>

        {/* Milestones */}
        <div className="relative">
          <h3 className="text-sm font-medium text-gray-400 mb-3">Milestones</h3>
          <div className="flex flex-wrap gap-2">
            {milestonesWithProgress.map((m) => (
              <span
                key={m.label}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors ${
                  m.achieved
                    ? 'bg-kurios-secondary/15 border-kurios-secondary/30 text-kurios-secondary'
                    : 'bg-white/[0.03] border-kurios-border text-gray-500'
                }`}
              >
                {m.label} {m.achieved && '✓'}
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 stagger-children">
        {[
          { label: 'Avg Deal Size', value: formatCurrency(Math.round(deals.reduce((s, d) => s + d.value, 0) / (deals.length || 1))), icon: DollarSign, iconColor: 'text-kurios-primary' },
          { label: 'Cost/Call', value: `$${callData.avgCostPerCall}`, icon: Phone, iconColor: callData.avgCostPerCall <= callData.targetCostPerCall ? 'text-kurios-secondary' : 'text-amber-400' },
          { label: 'Win Rate', value: `${Math.round((closedDeals.length / (deals.length || 1)) * 100)}%`, icon: Target, iconColor: 'text-kurios-secondary' },
          { label: 'Active States', value: stateData.length, icon: MapPin, iconColor: 'text-amber-400' },
        ].map((m) => (
          <div key={m.label} className="p-5 rounded-xl border border-kurios-border bg-kurios-card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs font-medium text-gray-500 uppercase tracking-wider">{m.label}</p>
                <p className="text-2xl font-bold text-white mt-1 tabular-nums">{m.value}</p>
              </div>
              <m.icon className={`w-7 h-7 ${m.iconColor} opacity-60`} />
            </div>
          </div>
        ))}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Pipeline by Stage */}
        <div className="p-5 rounded-xl border border-kurios-border bg-kurios-card">
          <h3 className="font-semibold text-white mb-4">Pipeline by Stage (30% Margin)</h3>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={pipelineByStage} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="#1E2330" />
                <XAxis
                  type="number"
                  stroke="#4B5563"
                  fontSize={11}
                  tickFormatter={(v) => `$${v / 1000}k`}
                  axisLine={false}
                  tickLine={false}
                />
                <YAxis
                  type="category"
                  dataKey="name"
                  stroke="#4B5563"
                  fontSize={11}
                  width={80}
                  axisLine={false}
                  tickLine={false}
                />
                <Tooltip
                  contentStyle={chartTooltipStyle}
                  itemStyle={{ color: '#E5E7EB', fontSize: 12 }}
                  labelStyle={{ color: '#9CA3AF', fontSize: 11 }}
                  formatter={(value, name, props) => [
                    formatCurrency(value),
                    `Margin (${props.payload.deals} deals)`,
                  ]}
                />
                <Bar dataKey="value" radius={[0, 6, 6, 0]} barSize={20}>
                  {pipelineByStage.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* State Performance */}
        <div className="p-5 rounded-xl border border-kurios-border bg-kurios-card">
          <h3 className="font-semibold text-white mb-4">State Performance (Conversion %)</h3>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={stateData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1E2330" />
                <XAxis
                  dataKey="state"
                  stroke="#4B5563"
                  fontSize={11}
                  axisLine={false}
                  tickLine={false}
                />
                <YAxis
                  stroke="#4B5563"
                  fontSize={11}
                  axisLine={false}
                  tickLine={false}
                />
                <Tooltip
                  contentStyle={chartTooltipStyle}
                  itemStyle={{ color: '#E5E7EB', fontSize: 12 }}
                  labelStyle={{ color: '#9CA3AF', fontSize: 11 }}
                  formatter={(value) => [`${value}%`, 'Conversion']}
                />
                <Bar dataKey="conversion" fill="#00E676" radius={[6, 6, 0, 0]} barSize={28} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* State Table */}
      <div className="rounded-xl border border-kurios-border bg-kurios-card overflow-hidden">
        <div className="px-5 py-4 border-b border-kurios-border">
          <h3 className="font-semibold text-white">State-by-State Performance</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="text-[11px] font-medium text-gray-500 uppercase tracking-wider">
                <th className="text-left py-3 px-5">State</th>
                <th className="text-right py-3 px-5">Clients</th>
                <th className="text-right py-3 px-5">Avg Case $</th>
                <th className="text-right py-3 px-5">Conversion</th>
                <th className="text-right py-3 px-5">Cases/Mo</th>
                <th className="text-right py-3 px-5">Total Spend</th>
              </tr>
            </thead>
            <tbody>
              {stateData.map((s) => (
                <tr key={s.state} className="border-t border-kurios-border hover:bg-white/[0.02] transition-colors">
                  <td className="py-3 px-5 font-semibold text-sm text-white">{s.state}</td>
                  <td className="py-3 px-5 text-right text-sm text-gray-300">{s.clients}</td>
                  <td className="py-3 px-5 text-right text-sm text-gray-300">
                    ${s.avgCaseValue.toLocaleString()}
                  </td>
                  <td className="py-3 px-5 text-right">
                    <span
                      className={`text-sm font-medium ${
                        s.conversion >= 20
                          ? 'text-kurios-secondary'
                          : s.conversion >= 15
                          ? 'text-kurios-primary'
                          : 'text-amber-400'
                      }`}
                    >
                      {s.conversion}%
                    </span>
                  </td>
                  <td className="py-3 px-5 text-right text-sm text-gray-300">{s.casesPerMonth}</td>
                  <td className="py-3 px-5 text-right text-sm font-medium text-white">
                    {formatCurrency(s.totalSpend)}
                  </td>
                </tr>
              ))}
            </tbody>
            <tfoot>
              <tr className="border-t-2 border-kurios-border-hover bg-white/[0.02]">
                <td className="py-3 px-5 font-bold text-sm text-white">Total</td>
                <td className="py-3 px-5 text-right font-bold text-sm text-white">
                  {stateData.reduce((s, st) => s + st.clients, 0)}
                </td>
                <td className="py-3 px-5 text-right font-bold text-sm text-white">
                  ${Math.round(stateData.reduce((s, st) => s + st.avgCaseValue, 0) / stateData.length).toLocaleString()}
                </td>
                <td className="py-3 px-5 text-right font-bold text-sm text-kurios-secondary">
                  {Math.round(stateData.reduce((s, st) => s + st.conversion, 0) / stateData.length)}%
                </td>
                <td className="py-3 px-5 text-right font-bold text-sm text-white">
                  {stateData.reduce((s, st) => s + st.casesPerMonth, 0)}
                </td>
                <td className="py-3 px-5 text-right font-bold text-sm text-kurios-primary">
                  {formatCurrency(stateData.reduce((s, st) => s + st.totalSpend, 0))}
                </td>
              </tr>
            </tfoot>
          </table>
        </div>
      </div>

      {/* Priority Pie */}
      <div className="p-5 rounded-xl border border-kurios-border bg-kurios-card">
        <h3 className="font-semibold text-white mb-4">Pipeline Priority Mix</h3>
        <div className="flex flex-col sm:flex-row items-center gap-8">
          <div className="w-48 h-48">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={priorityData}
                  cx="50%"
                  cy="50%"
                  innerRadius={55}
                  outerRadius={80}
                  paddingAngle={3}
                  dataKey="value"
                  strokeWidth={0}
                >
                  {priorityData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={chartTooltipStyle}
                  itemStyle={{ color: '#E5E7EB', fontSize: 12 }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="space-y-3">
            {priorityData.map((p) => (
              <div key={p.name} className="flex items-center gap-3">
                <div className="w-3 h-3 rounded-sm" style={{ backgroundColor: p.color }} />
                <span className="text-sm text-gray-300">
                  <span className="font-medium text-white">{p.name}</span> — {p.value} deal
                  {p.value !== 1 ? 's' : ''}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
