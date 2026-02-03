import { 
  BarChart, Bar, PieChart, Pie, Cell, AreaChart, Area,
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend 
} from 'recharts';
import { Target, DollarSign, Phone, TrendingUp, Users, MapPin, Music, Calendar } from 'lucide-react';
import useStore from '../stores/useStore';
import { GOAL, stateData, milestones, callData } from '../data/sampleData';
import { formatCurrency } from '../utils/helpers';

export default function Analytics() {
  const { deals, clients, settings } = useStore();
  const darkMode = settings.appearance.darkMode;

  // Calculate real metrics
  const closedDeals = deals.filter(d => d.stage === 'closed');
  const totalClosed = closedDeals.reduce((sum, d) => sum + d.value, 0);
  const kuriosMargin = closedDeals.reduce((sum, d) => sum + (d.kuriosMargin || d.value * 0.3), 0);
  
  const pipelineDeals = deals.filter(d => d.stage !== 'closed');
  const pipelineValue = pipelineDeals.reduce((sum, d) => sum + d.value, 0);
  const weightedPipeline = pipelineDeals.reduce((sum, d) => sum + (d.value * (d.probability / 100)), 0);
  const weightedMargin = weightedPipeline * GOAL.margin;

  // Goal progress
  const goalProgress = (kuriosMargin / GOAL.total) * 100;
  const projectedTotal = kuriosMargin + weightedMargin;

  // Pipeline by stage
  const pipelineByStage = [
    { name: 'Lead', value: deals.filter(d => d.stage === 'lead').reduce((s, d) => s + (d.kuriosMargin || d.value * 0.3), 0), deals: deals.filter(d => d.stage === 'lead').length, color: '#6366f1' },
    { name: 'Qualified', value: deals.filter(d => d.stage === 'qualified').reduce((s, d) => s + (d.kuriosMargin || d.value * 0.3), 0), deals: deals.filter(d => d.stage === 'qualified').length, color: '#8b5cf6' },
    { name: 'Proposal', value: deals.filter(d => d.stage === 'proposal').reduce((s, d) => s + (d.kuriosMargin || d.value * 0.3), 0), deals: deals.filter(d => d.stage === 'proposal').length, color: '#3366FF' },
    { name: 'Negotiation', value: deals.filter(d => d.stage === 'negotiation').reduce((s, d) => s + (d.kuriosMargin || d.value * 0.3), 0), deals: deals.filter(d => d.stage === 'negotiation').length, color: '#f59e0b' },
    { name: 'Closed', value: deals.filter(d => d.stage === 'closed').reduce((s, d) => s + (d.kuriosMargin || d.value * 0.3), 0), deals: deals.filter(d => d.stage === 'closed').length, color: '#00E676' },
  ];

  // Priority breakdown
  const priorityData = [
    { name: 'High', value: deals.filter(d => d.priority === 'high' && d.stage !== 'closed').length, color: '#ef4444' },
    { name: 'Medium', value: deals.filter(d => d.priority === 'medium' && d.stage !== 'closed').length, color: '#f59e0b' },
    { name: 'Low', value: deals.filter(d => d.priority === 'low' && d.stage !== 'closed').length, color: '#6b7280' },
  ];

  // Monthly projection (simple linear based on first month)
  const monthlyProjection = [];
  let cumulative = kuriosMargin;
  const monthlyTarget = (GOAL.total / 36); // 3 years
  for (let i = 1; i <= 12; i++) {
    cumulative += monthlyTarget;
    monthlyProjection.push({
      month: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][i - 1],
      actual: i === 1 ? kuriosMargin : null,
      projected: cumulative,
      target: GOAL.total / 36 * i,
    });
  }
  monthlyProjection[0].actual = kuriosMargin;

  // Milestone tracking
  const milestonesWithProgress = milestones.map(m => ({
    ...m,
    achieved: kuriosMargin >= m.amount,
    progress: Math.min((kuriosMargin / m.amount) * 100, 100),
  }));

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* $9.6M Goal Tracker - HERO */}
      <div className={`p-6 rounded-2xl border-2 ${
        darkMode 
          ? 'bg-gradient-to-br from-kurios-primary/20 via-purple-900/20 to-kurios-secondary/20 border-kurios-primary/50' 
          : 'bg-gradient-to-br from-kurios-primary/10 to-kurios-secondary/10 border-kurios-primary/30'
      }`}>
        <div className="flex items-center gap-4 mb-6">
          <div className="p-3 rounded-xl bg-gradient-to-br from-kurios-primary to-purple-600">
            <Music className="w-8 h-8 text-white" />
          </div>
          <div>
            <h2 className={`text-2xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
              $9.6M Goal Tracker
            </h2>
            <p className={darkMode ? 'text-gray-400' : 'text-gray-500'}>
              Exit by Dec 2026 → Full-time music
            </p>
          </div>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div className={`p-4 rounded-xl ${darkMode ? 'bg-gray-800/50' : 'bg-white/50'}`}>
            <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Earned (30%)</p>
            <p className="text-2xl font-bold text-kurios-secondary">{formatCurrency(kuriosMargin)}</p>
          </div>
          <div className={`p-4 rounded-xl ${darkMode ? 'bg-gray-800/50' : 'bg-white/50'}`}>
            <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Pipeline (30%)</p>
            <p className="text-2xl font-bold text-kurios-primary">{formatCurrency(weightedMargin)}</p>
          </div>
          <div className={`p-4 rounded-xl ${darkMode ? 'bg-gray-800/50' : 'bg-white/50'}`}>
            <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Progress</p>
            <p className={`text-2xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>{goalProgress.toFixed(2)}%</p>
          </div>
          <div className={`p-4 rounded-xl ${darkMode ? 'bg-gray-800/50' : 'bg-white/50'}`}>
            <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Remaining</p>
            <p className="text-2xl font-bold text-orange-500">{formatCurrency(GOAL.total - kuriosMargin)}</p>
          </div>
        </div>

        {/* Milestones */}
        <div className="space-y-3">
          <h3 className={`font-semibold ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>Milestones</h3>
          <div className="flex flex-wrap gap-3">
            {milestonesWithProgress.map((m) => (
              <div 
                key={m.label}
                className={`px-4 py-2 rounded-lg border ${
                  m.achieved
                    ? 'bg-kurios-secondary/20 border-kurios-secondary text-kurios-secondary'
                    : darkMode
                    ? 'bg-gray-800 border-gray-700 text-gray-400'
                    : 'bg-gray-100 border-gray-200 text-gray-500'
                }`}
              >
                <span className="font-semibold">{m.label}</span>
                {m.achieved && <span className="ml-2">✓</span>}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className={`p-5 rounded-xl border ${
          darkMode ? 'bg-gray-800/50 border-gray-700' : 'bg-white border-gray-200'
        }`}>
          <div className="flex items-center justify-between">
            <div>
              <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Avg Deal Size</p>
              <p className={`text-2xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                {formatCurrency(Math.round(deals.reduce((s, d) => s + d.value, 0) / deals.length))}
              </p>
            </div>
            <DollarSign className="w-8 h-8 text-kurios-primary" />
          </div>
        </div>
        <div className={`p-5 rounded-xl border ${
          darkMode ? 'bg-gray-800/50 border-gray-700' : 'bg-white border-gray-200'
        }`}>
          <div className="flex items-center justify-between">
            <div>
              <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Cost/Call</p>
              <p className={`text-2xl font-bold ${
                callData.avgCostPerCall <= callData.targetCostPerCall ? 'text-kurios-secondary' : 'text-orange-500'
              }`}>
                ${callData.avgCostPerCall}
              </p>
            </div>
            <Phone className="w-8 h-8 text-purple-500" />
          </div>
        </div>
        <div className={`p-5 rounded-xl border ${
          darkMode ? 'bg-gray-800/50 border-gray-700' : 'bg-white border-gray-200'
        }`}>
          <div className="flex items-center justify-between">
            <div>
              <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Win Rate</p>
              <p className={`text-2xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                {Math.round((closedDeals.length / deals.length) * 100)}%
              </p>
            </div>
            <Target className="w-8 h-8 text-kurios-secondary" />
          </div>
        </div>
        <div className={`p-5 rounded-xl border ${
          darkMode ? 'bg-gray-800/50 border-gray-700' : 'bg-white border-gray-200'
        }`}>
          <div className="flex items-center justify-between">
            <div>
              <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Active States</p>
              <p className={`text-2xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                {stateData.length}
              </p>
            </div>
            <MapPin className="w-8 h-8 text-orange-500" />
          </div>
        </div>
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Pipeline by Stage */}
        <div className={`p-6 rounded-xl border ${
          darkMode ? 'bg-gray-800/50 border-gray-700' : 'bg-white border-gray-200'
        }`}>
          <h3 className={`font-semibold mb-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
            Pipeline by Stage (30% Margin)
          </h3>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={pipelineByStage} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke={darkMode ? '#374151' : '#e5e7eb'} />
                <XAxis type="number" stroke={darkMode ? '#9ca3af' : '#6b7280'} fontSize={12} tickFormatter={(v) => `$${v/1000}k`} />
                <YAxis type="category" dataKey="name" stroke={darkMode ? '#9ca3af' : '#6b7280'} fontSize={12} width={80} />
                <Tooltip 
                  contentStyle={{
                    backgroundColor: darkMode ? '#1f2937' : '#ffffff',
                    border: `1px solid ${darkMode ? '#374151' : '#e5e7eb'}`,
                    borderRadius: '8px',
                  }}
                  formatter={(value, name, props) => [formatCurrency(value), `Margin (${props.payload.deals} deals)`]}
                />
                <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                  {pipelineByStage.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* State Performance */}
        <div className={`p-6 rounded-xl border ${
          darkMode ? 'bg-gray-800/50 border-gray-700' : 'bg-white border-gray-200'
        }`}>
          <h3 className={`font-semibold mb-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
            State Performance (Conversion %)
          </h3>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={stateData}>
                <CartesianGrid strokeDasharray="3 3" stroke={darkMode ? '#374151' : '#e5e7eb'} />
                <XAxis dataKey="state" stroke={darkMode ? '#9ca3af' : '#6b7280'} fontSize={12} />
                <YAxis stroke={darkMode ? '#9ca3af' : '#6b7280'} fontSize={12} />
                <Tooltip 
                  contentStyle={{
                    backgroundColor: darkMode ? '#1f2937' : '#ffffff',
                    border: `1px solid ${darkMode ? '#374151' : '#e5e7eb'}`,
                    borderRadius: '8px',
                  }}
                  formatter={(value, name) => [
                    name === 'conversion' ? `${value}%` : formatCurrency(value),
                    name === 'conversion' ? 'Conversion' : 'Avg Case Value'
                  ]}
                />
                <Bar dataKey="conversion" fill="#00E676" radius={[4, 4, 0, 0]} name="Conversion %" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* State Details Table */}
      <div className={`p-6 rounded-xl border ${
        darkMode ? 'bg-gray-800/50 border-gray-700' : 'bg-white border-gray-200'
      }`}>
        <h3 className={`font-semibold mb-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
          State-by-State Performance
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className={darkMode ? 'text-gray-400' : 'text-gray-500'}>
                <th className="text-left py-3 px-4 font-medium">State</th>
                <th className="text-right py-3 px-4 font-medium">Clients</th>
                <th className="text-right py-3 px-4 font-medium">Avg Case Value</th>
                <th className="text-right py-3 px-4 font-medium">Conversion</th>
                <th className="text-right py-3 px-4 font-medium">Cases/Mo</th>
                <th className="text-right py-3 px-4 font-medium">Total Spend</th>
              </tr>
            </thead>
            <tbody>
              {stateData.map((state) => (
                <tr 
                  key={state.state}
                  className={`border-t ${darkMode ? 'border-gray-700' : 'border-gray-200'}`}
                >
                  <td className={`py-3 px-4 font-semibold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                    {state.state}
                  </td>
                  <td className={`py-3 px-4 text-right ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                    {state.clients}
                  </td>
                  <td className={`py-3 px-4 text-right ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                    ${state.avgCaseValue.toLocaleString()}
                  </td>
                  <td className="py-3 px-4 text-right">
                    <span className={`font-medium ${
                      state.conversion >= 20 ? 'text-kurios-secondary' :
                      state.conversion >= 15 ? 'text-kurios-primary' :
                      'text-orange-500'
                    }`}>
                      {state.conversion}%
                    </span>
                  </td>
                  <td className={`py-3 px-4 text-right ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                    {state.casesPerMonth}
                  </td>
                  <td className={`py-3 px-4 text-right font-medium ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                    {formatCurrency(state.totalSpend)}
                  </td>
                </tr>
              ))}
            </tbody>
            <tfoot>
              <tr className={`border-t-2 ${darkMode ? 'border-gray-600' : 'border-gray-300'}`}>
                <td className={`py-3 px-4 font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                  Total
                </td>
                <td className={`py-3 px-4 text-right font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                  {stateData.reduce((s, st) => s + st.clients, 0)}
                </td>
                <td className={`py-3 px-4 text-right font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                  ${Math.round(stateData.reduce((s, st) => s + st.avgCaseValue, 0) / stateData.length).toLocaleString()}
                </td>
                <td className={`py-3 px-4 text-right font-bold text-kurios-secondary`}>
                  {Math.round(stateData.reduce((s, st) => s + st.conversion, 0) / stateData.length)}%
                </td>
                <td className={`py-3 px-4 text-right font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                  {stateData.reduce((s, st) => s + st.casesPerMonth, 0)}
                </td>
                <td className={`py-3 px-4 text-right font-bold text-kurios-primary`}>
                  {formatCurrency(stateData.reduce((s, st) => s + st.totalSpend, 0))}
                </td>
              </tr>
            </tfoot>
          </table>
        </div>
      </div>

      {/* Deal Priority */}
      <div className={`p-6 rounded-xl border ${
        darkMode ? 'bg-gray-800/50 border-gray-700' : 'bg-white border-gray-200'
      }`}>
        <h3 className={`font-semibold mb-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
          Pipeline Priority Mix
        </h3>
        <div className="flex items-center gap-8">
          <div className="w-48 h-48">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={priorityData}
                  cx="50%"
                  cy="50%"
                  innerRadius={50}
                  outerRadius={80}
                  paddingAngle={2}
                  dataKey="value"
                >
                  {priorityData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="space-y-3">
            {priorityData.map((p) => (
              <div key={p.name} className="flex items-center gap-3">
                <div className="w-4 h-4 rounded" style={{ backgroundColor: p.color }} />
                <span className={darkMode ? 'text-gray-300' : 'text-gray-700'}>
                  {p.name}: {p.value} deals
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
