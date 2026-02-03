import { 
  Phone, 
  DollarSign, 
  Target,
  TrendingUp,
  Plus,
  ArrowRight,
  Calendar,
  CheckCircle,
  AlertCircle,
  Clock,
  Flame,
  Music,
  Zap
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import useStore from '../stores/useStore';
import KPICard from '../components/UI/KPICard';
import { formatCurrency, formatRelativeTime } from '../utils/helpers';
import { GOAL, callData, milestones, activityFeed, stateData } from '../data/sampleData';

export default function Dashboard() {
  const { deals, clients, settings, openModal } = useStore();
  const darkMode = settings.appearance.darkMode;

  // Calculate real KPIs
  const closedDeals = deals.filter(d => d.stage === 'closed');
  const totalClosed = closedDeals.reduce((sum, d) => sum + d.value, 0);
  const kuriosMargin = closedDeals.reduce((sum, d) => sum + (d.kuriosMargin || d.value * 0.3), 0);
  
  // Pipeline (not closed)
  const pipelineDeals = deals.filter(d => d.stage !== 'closed');
  const pipelineValue = pipelineDeals.reduce((sum, d) => sum + d.value, 0);
  const weightedPipeline = pipelineDeals.reduce((sum, d) => sum + (d.value * (d.probability / 100)), 0);
  const weightedMargin = weightedPipeline * GOAL.margin;

  // High priority deals
  const hotDeals = deals.filter(d => d.priority === 'high' && d.stage !== 'closed');

  // $9.6M Goal Progress
  const goalProgress = (kuriosMargin / GOAL.total) * 100;
  const projectedTotal = kuriosMargin + weightedMargin;
  const projectedProgress = (projectedTotal / GOAL.total) * 100;

  // Next milestone
  const nextMilestone = milestones.find(m => m.amount > kuriosMargin) || milestones[milestones.length - 1];
  const milestoneProgress = (kuriosMargin / nextMilestone.amount) * 100;

  // Time to goal
  const monthsToGoal = Math.ceil((GOAL.total - kuriosMargin) / (kuriosMargin || 10000));
  const targetDate = new Date(GOAL.deadline);
  const monthsRemaining = Math.ceil((targetDate - new Date()) / (1000 * 60 * 60 * 24 * 30));

  const activityIcons = {
    'plus': Plus,
    'check-circle': CheckCircle,
    'trending-up': TrendingUp,
    'phone': Phone,
    'alert-circle': AlertCircle,
  };

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* $9.6M GOAL - PROMINENT */}
      <div className={`p-6 rounded-2xl border-2 ${
        darkMode 
          ? 'bg-gradient-to-r from-kurios-primary/20 via-purple-900/20 to-kurios-secondary/20 border-kurios-primary/50' 
          : 'bg-gradient-to-r from-kurios-primary/10 to-kurios-secondary/10 border-kurios-primary/30'
      }`}>
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 mb-6">
          <div className="flex items-center gap-4">
            <div className="p-3 rounded-xl bg-gradient-to-br from-kurios-primary to-purple-600">
              <Music className="w-8 h-8 text-white" />
            </div>
            <div>
              <h2 className={`text-2xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                $9.6M → Music 🎵
              </h2>
              <p className={`${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                Exit by Dec 2026, then retire to music
              </p>
            </div>
          </div>
          <div className="flex items-center gap-6">
            <div className="text-center">
              <p className="text-4xl font-black text-kurios-secondary">{goalProgress.toFixed(2)}%</p>
              <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Complete</p>
            </div>
            <div className="text-center">
              <p className={`text-2xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                {formatCurrency(kuriosMargin)}
              </p>
              <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Earned (30%)</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-kurios-primary">
                {formatCurrency(GOAL.total - kuriosMargin)}
              </p>
              <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>To Go</p>
            </div>
          </div>
        </div>
        
        {/* Progress bar with milestones */}
        <div className="relative">
          <div className={`h-6 rounded-full ${darkMode ? 'bg-gray-700' : 'bg-gray-200'} overflow-hidden`}>
            <div 
              className="h-full rounded-full bg-gradient-to-r from-kurios-primary via-purple-500 to-kurios-secondary transition-all duration-1000 relative"
              style={{ width: `${Math.min(goalProgress, 100)}%` }}
            >
              <div className="absolute inset-0 bg-white/20 animate-pulse" />
            </div>
          </div>
          {/* Milestone markers */}
          <div className="absolute top-0 left-0 w-full h-6 flex items-center">
            {milestones.slice(0, -1).map((m, i) => (
              <div 
                key={m.label}
                className="absolute h-6 w-px bg-white/30"
                style={{ left: `${(m.amount / GOAL.total) * 100}%` }}
              />
            ))}
          </div>
        </div>
        
        {/* Next milestone */}
        <div className="flex items-center justify-between mt-4">
          <div className="flex items-center gap-2">
            <Target className="w-5 h-5 text-kurios-primary" />
            <span className={darkMode ? 'text-gray-300' : 'text-gray-700'}>
              Next: <span className="font-bold">{nextMilestone.label}</span>
            </span>
            <span className={`text-sm ${darkMode ? 'text-gray-500' : 'text-gray-400'}`}>
              ({formatCurrency(nextMilestone.amount - kuriosMargin)} away)
            </span>
          </div>
          <div className="flex items-center gap-2">
            <Clock className="w-4 h-4 text-gray-400" />
            <span className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
              {monthsRemaining} months remaining
            </span>
          </div>
        </div>
      </div>

      {/* Primary KPIs - Calls focused */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className={`p-5 rounded-xl border ${
          darkMode ? 'bg-gray-800/50 border-gray-700' : 'bg-white border-gray-200'
        }`}>
          <div className="flex items-center justify-between">
            <div>
              <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Calls Today</p>
              <p className={`text-3xl font-bold ${
                callData.today >= callData.target.daily ? 'text-kurios-secondary' : darkMode ? 'text-white' : 'text-gray-900'
              }`}>
                {callData.today}/{callData.target.daily}
              </p>
            </div>
            <div className={`p-3 rounded-xl ${callData.today >= callData.target.daily ? 'bg-kurios-secondary' : 'bg-kurios-primary'}`}>
              <Phone className="w-6 h-6 text-white" />
            </div>
          </div>
        </div>

        <div className={`p-5 rounded-xl border ${
          darkMode ? 'bg-gray-800/50 border-gray-700' : 'bg-white border-gray-200'
        }`}>
          <div className="flex items-center justify-between">
            <div>
              <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Cost/Call</p>
              <p className={`text-3xl font-bold ${
                callData.avgCostPerCall <= callData.targetCostPerCall ? 'text-kurios-secondary' : 'text-orange-500'
              }`}>
                ${callData.avgCostPerCall}
              </p>
              <p className={`text-xs ${darkMode ? 'text-gray-500' : 'text-gray-400'}`}>
                Target: &lt;${callData.targetCostPerCall}
              </p>
            </div>
            <div className={`p-3 rounded-xl ${
              callData.avgCostPerCall <= callData.targetCostPerCall ? 'bg-kurios-secondary' : 'bg-orange-500'
            }`}>
              <DollarSign className="w-6 h-6 text-white" />
            </div>
          </div>
        </div>

        <div className={`p-5 rounded-xl border ${
          darkMode ? 'bg-gray-800/50 border-gray-700' : 'bg-white border-gray-200'
        }`}>
          <div className="flex items-center justify-between">
            <div>
              <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Pipeline (30%)</p>
              <p className={`text-3xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                {formatCurrency(weightedMargin)}
              </p>
              <p className={`text-xs ${darkMode ? 'text-gray-500' : 'text-gray-400'}`}>
                {pipelineDeals.length} deals
              </p>
            </div>
            <div className="p-3 rounded-xl bg-purple-500">
              <TrendingUp className="w-6 h-6 text-white" />
            </div>
          </div>
        </div>

        <div className={`p-5 rounded-xl border ${
          darkMode ? 'bg-gray-800/50 border-gray-700' : 'bg-white border-gray-200'
        }`}>
          <div className="flex items-center justify-between">
            <div>
              <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>This Week</p>
              <p className={`text-3xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                {callData.thisWeek}/{callData.target.weekly}
              </p>
              <p className={`text-xs ${darkMode ? 'text-gray-500' : 'text-gray-400'}`}>
                calls
              </p>
            </div>
            <div className="p-3 rounded-xl bg-kurios-primary">
              <Calendar className="w-6 h-6 text-white" />
            </div>
          </div>
        </div>
      </div>

      {/* Hot Deals & Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* 🔥 HOT DEALS */}
        <div className={`p-6 rounded-xl border ${
          darkMode ? 'bg-gray-800/50 border-gray-700' : 'bg-white border-gray-200'
        }`}>
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Flame className="w-5 h-5 text-orange-500" />
              <h2 className={`text-lg font-semibold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                Hot Deals
              </h2>
            </div>
            <Link to="/pipeline" className="text-sm text-kurios-primary hover:underline">
              View all →
            </Link>
          </div>
          
          <div className="space-y-3">
            {hotDeals.map((deal) => (
              <div 
                key={deal.id}
                className={`p-4 rounded-lg border-l-4 ${
                  deal.priority === 'high' ? 'border-l-orange-500' : 'border-l-kurios-primary'
                } ${darkMode ? 'bg-gray-700/50' : 'bg-gray-50'}`}
              >
                <div className="flex items-start justify-between">
                  <div>
                    <p className={`font-semibold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                      {deal.name}
                    </p>
                    <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                      {deal.company} • {deal.state}
                    </p>
                    <p className={`text-xs mt-1 ${darkMode ? 'text-gray-500' : 'text-gray-400'}`}>
                      {deal.notes}
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="font-bold text-kurios-secondary">
                      {formatCurrency(deal.kuriosMargin || deal.value * 0.3)}
                    </p>
                    <p className={`text-xs ${darkMode ? 'text-gray-500' : 'text-gray-400'}`}>
                      margin
                    </p>
                  </div>
                </div>
                <div className="flex items-center justify-between mt-3">
                  <span className={`text-xs px-2 py-1 rounded-full ${
                    darkMode ? 'bg-gray-600 text-gray-300' : 'bg-gray-200 text-gray-600'
                  }`}>
                    {deal.nextAction}
                  </span>
                  <span className={`text-xs ${darkMode ? 'text-gray-500' : 'text-gray-400'}`}>
                    {deal.probability}% likely
                  </span>
                </div>
              </div>
            ))}
            {hotDeals.length === 0 && (
              <p className={`text-center py-4 ${darkMode ? 'text-gray-500' : 'text-gray-400'}`}>
                No hot deals right now
              </p>
            )}
          </div>
        </div>

        {/* Activity Feed */}
        <div className={`p-6 rounded-xl border ${
          darkMode ? 'bg-gray-800/50 border-gray-700' : 'bg-white border-gray-200'
        }`}>
          <div className="flex items-center justify-between mb-4">
            <h2 className={`text-lg font-semibold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
              Recent Activity
            </h2>
          </div>
          
          <div className="space-y-4">
            {activityFeed.slice(0, 5).map((activity) => {
              const Icon = activityIcons[activity.icon] || Clock;
              return (
                <div key={activity.id} className="flex items-start gap-3">
                  <div className={`p-2 rounded-lg ${
                    activity.type === 'deal' ? 'bg-kurios-secondary/20' :
                    activity.type === 'call' ? 'bg-kurios-primary/20' :
                    'bg-gray-100 dark:bg-gray-700'
                  }`}>
                    <Icon className={`w-4 h-4 ${
                      activity.type === 'deal' ? 'text-kurios-secondary' :
                      activity.type === 'call' ? 'text-kurios-primary' :
                      'text-gray-500'
                    }`} />
                  </div>
                  <div className="flex-1">
                    <p className={`text-sm ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                      {activity.message}
                    </p>
                    <p className={`text-xs mt-1 ${darkMode ? 'text-gray-500' : 'text-gray-400'}`}>
                      {formatRelativeTime(activity.timestamp)}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {[
          { label: 'Log Call', modal: 'addCall', icon: Phone, color: 'bg-kurios-primary' },
          { label: 'Add Deal', modal: 'addDeal', icon: Plus, color: 'bg-purple-500' },
          { label: 'New Lead', modal: 'addContact', icon: Zap, color: 'bg-orange-500' },
          { label: 'View Pipeline', link: '/pipeline', icon: TrendingUp, color: 'bg-kurios-secondary' },
        ].map((action) => (
          action.link ? (
            <Link
              key={action.label}
              to={action.link}
              className={`flex items-center gap-3 p-4 rounded-xl ${
                darkMode ? 'bg-gray-800 hover:bg-gray-700' : 'bg-white hover:bg-gray-50'
              } border ${darkMode ? 'border-gray-700' : 'border-gray-200'} transition-all hover:scale-[1.02]`}
            >
              <div className={`p-2 rounded-lg ${action.color}`}>
                <action.icon className="w-5 h-5 text-white" />
              </div>
              <span className={`font-medium ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                {action.label}
              </span>
            </Link>
          ) : (
            <button
              key={action.label}
              onClick={() => openModal(action.modal)}
              className={`flex items-center gap-3 p-4 rounded-xl ${
                darkMode ? 'bg-gray-800 hover:bg-gray-700' : 'bg-white hover:bg-gray-50'
              } border ${darkMode ? 'border-gray-700' : 'border-gray-200'} transition-all hover:scale-[1.02]`}
            >
              <div className={`p-2 rounded-lg ${action.color}`}>
                <action.icon className="w-5 h-5 text-white" />
              </div>
              <span className={`font-medium ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                {action.label}
              </span>
            </button>
          )
        ))}
      </div>

      {/* State Performance Preview */}
      <div className={`p-6 rounded-xl border ${
        darkMode ? 'bg-gray-800/50 border-gray-700' : 'bg-white border-gray-200'
      }`}>
        <div className="flex items-center justify-between mb-4">
          <h2 className={`text-lg font-semibold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
            State Performance
          </h2>
          <Link to="/clients" className="text-sm text-kurios-primary hover:underline">
            View details →
          </Link>
        </div>
        
        <div className="grid grid-cols-3 md:grid-cols-5 gap-4">
          {stateData.slice(0, 5).map((state) => (
            <div key={state.state} className={`p-3 rounded-lg text-center ${
              darkMode ? 'bg-gray-700' : 'bg-gray-50'
            }`}>
              <p className={`text-2xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                {state.state}
              </p>
              <p className="text-sm text-kurios-secondary font-medium">
                {state.conversion}% conv
              </p>
              <p className={`text-xs ${darkMode ? 'text-gray-500' : 'text-gray-400'}`}>
                {state.clients} client{state.clients > 1 ? 's' : ''}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
