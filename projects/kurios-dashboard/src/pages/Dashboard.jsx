import {
  Phone,
  DollarSign,
  Target,
  TrendingUp,
  Plus,
  Calendar,
  CheckCircle,
  AlertCircle,
  Clock,
  Flame,
  Music,
  Zap,
} from 'lucide-react';
import { Link } from 'react-router-dom';
import useStore from '../stores/useStore';
import { formatCurrency, formatRelativeTime } from '../utils/helpers';
import { GOAL, callData, milestones, activityFeed, stateData } from '../data/sampleData';

export default function Dashboard() {
  const { deals, openModal } = useStore();

  // Calculate real KPIs
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

  const hotDeals = deals.filter(
    (d) => d.priority === 'high' && d.stage !== 'closed'
  );

  const goalProgress = (kuriosMargin / GOAL.total) * 100;
  const nextMilestone =
    milestones.find((m) => m.amount > kuriosMargin) ||
    milestones[milestones.length - 1];
  const targetDate = new Date(GOAL.deadline);
  const monthsRemaining = Math.ceil(
    (targetDate - new Date()) / (1000 * 60 * 60 * 24 * 30)
  );

  const activityIcons = {
    plus: Plus,
    'check-circle': CheckCircle,
    'trending-up': TrendingUp,
    phone: Phone,
    'alert-circle': AlertCircle,
  };

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* ── $9.6M GOAL — HERO ────────────────────────────── */}
      <div className="p-6 rounded-2xl border border-kurios-primary/25 bg-gradient-to-br from-kurios-primary/[0.08] via-kurios-accent/[0.04] to-transparent relative overflow-hidden">
        {/* Decorative glow */}
        <div className="absolute -top-24 -right-24 w-64 h-64 bg-kurios-primary/10 rounded-full blur-3xl pointer-events-none" />

        <div className="relative flex flex-col lg:flex-row lg:items-center justify-between gap-5 mb-6">
          <div className="flex items-center gap-4">
            <div className="p-3 rounded-xl bg-gradient-to-br from-kurios-primary to-kurios-accent shadow-lg shadow-kurios-primary/20">
              <Music className="w-7 h-7 text-white" />
            </div>
            <div>
              <h2 className="text-xl md:text-2xl font-bold text-white tracking-tight">
                $9.6M → Music 🎵
              </h2>
              <p className="text-sm text-gray-400">
                Exit by Dec 2026, then retire to music
              </p>
            </div>
          </div>
          <div className="flex items-center gap-6 lg:gap-8">
            <div className="text-center">
              <p className="text-3xl md:text-4xl font-black text-kurios-secondary tabular-nums">
                {goalProgress.toFixed(2)}%
              </p>
              <p className="text-xs text-gray-500 mt-0.5">Complete</p>
            </div>
            <div className="text-center">
              <p className="text-xl md:text-2xl font-bold text-white tabular-nums">
                {formatCurrency(kuriosMargin)}
              </p>
              <p className="text-xs text-gray-500 mt-0.5">Earned (30%)</p>
            </div>
            <div className="text-center">
              <p className="text-xl md:text-2xl font-bold text-kurios-primary tabular-nums">
                {formatCurrency(GOAL.total - kuriosMargin)}
              </p>
              <p className="text-xs text-gray-500 mt-0.5">To Go</p>
            </div>
          </div>
        </div>

        {/* Progress bar */}
        <div className="relative">
          <div className="h-5 rounded-full bg-white/[0.06] overflow-hidden backdrop-blur-sm">
            <div
              className="h-full rounded-full bg-gradient-to-r from-kurios-primary via-kurios-accent to-kurios-secondary transition-all duration-1000 relative"
              style={{ width: `${Math.min(goalProgress, 100)}%`, minWidth: goalProgress > 0 ? '2rem' : 0 }}
            >
              <div className="absolute inset-0 bg-gradient-to-r from-white/0 via-white/20 to-white/0 animate-[shimmer_2.5s_infinite]" style={{ backgroundSize: '200% 100%' }} />
            </div>
          </div>
          {/* Milestone markers */}
          {milestones.slice(0, -1).map((m) => (
            <div
              key={m.label}
              className="absolute top-0 h-5 w-px bg-white/10"
              style={{ left: `${(m.amount / GOAL.total) * 100}%` }}
            />
          ))}
        </div>

        {/* Next milestone + time */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between mt-4 gap-2">
          <div className="flex items-center gap-2">
            <Target className="w-4 h-4 text-kurios-primary" />
            <span className="text-sm text-gray-300">
              Next: <span className="font-semibold text-white">{nextMilestone.label}</span>
            </span>
            <span className="text-xs text-gray-500">
              ({formatCurrency(nextMilestone.amount - kuriosMargin)} away)
            </span>
          </div>
          <div className="flex items-center gap-1.5">
            <Clock className="w-3.5 h-3.5 text-gray-500" />
            <span className="text-xs text-gray-500">
              {monthsRemaining} months remaining
            </span>
          </div>
        </div>
      </div>

      {/* ── KPI Row ──────────────────────────────────────── */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 stagger-children">
        {[
          {
            label: 'Calls Today',
            value: `${callData.today}/${callData.target.daily}`,
            hit: callData.today >= callData.target.daily,
            icon: Phone,
            color: callData.today >= callData.target.daily ? 'kurios-secondary' : 'kurios-primary',
          },
          {
            label: 'Cost/Call',
            value: `$${callData.avgCostPerCall}`,
            sub: `Target: <$${callData.targetCostPerCall}`,
            hit: callData.avgCostPerCall <= callData.targetCostPerCall,
            icon: DollarSign,
            color: callData.avgCostPerCall <= callData.targetCostPerCall ? 'kurios-secondary' : 'amber-500',
          },
          {
            label: 'Pipeline (30%)',
            value: formatCurrency(weightedMargin),
            sub: `${pipelineDeals.length} deals`,
            icon: TrendingUp,
            color: 'kurios-accent',
          },
          {
            label: 'This Week',
            value: `${callData.thisWeek}/${callData.target.weekly}`,
            sub: 'calls',
            icon: Calendar,
            color: 'kurios-primary',
          },
        ].map((kpi) => (
          <div
            key={kpi.label}
            className="p-5 rounded-xl border border-kurios-border bg-kurios-card hover:bg-kurios-card-hover transition-colors"
          >
            <div className="flex items-start justify-between">
              <div>
                <p className="text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {kpi.label}
                </p>
                <p className={`text-2xl md:text-3xl font-bold mt-1.5 tabular-nums ${
                  kpi.hit === true ? 'text-kurios-secondary' : kpi.hit === false ? 'text-amber-400' : 'text-white'
                }`}>
                  {kpi.value}
                </p>
                {kpi.sub && <p className="text-[11px] text-gray-600 mt-1">{kpi.sub}</p>}
              </div>
              <div className={`p-2.5 rounded-lg bg-${kpi.color}/15`}>
                <kpi.icon className={`w-5 h-5 text-${kpi.color}`} />
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* ── Hot Deals + Activity ─────────────────────────── */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Hot Deals */}
        <div className="p-5 rounded-xl border border-kurios-border bg-kurios-card">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Flame className="w-5 h-5 text-orange-400" />
              <h2 className="font-semibold text-white">Hot Deals</h2>
            </div>
            <Link
              to="/pipeline"
              className="text-xs text-kurios-primary hover:text-kurios-primary/80 font-medium transition-colors"
            >
              View all →
            </Link>
          </div>

          <div className="space-y-2.5">
            {hotDeals.length === 0 ? (
              <p className="text-center py-8 text-gray-600 text-sm">No hot deals right now</p>
            ) : (
              hotDeals.map((deal) => (
                <div
                  key={deal.id}
                  onClick={() => openModal('viewDetails', deal)}
                  className="p-3.5 rounded-lg border-l-[3px] border-l-orange-400 bg-white/[0.02] hover:bg-white/[0.04] transition-colors cursor-pointer"
                >
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="font-medium text-sm text-white">{deal.name}</p>
                      <p className="text-xs text-gray-500 mt-0.5">
                        {deal.company} • {deal.state}
                      </p>
                      <p className="text-[11px] text-gray-600 mt-1">{deal.notes}</p>
                    </div>
                    <div className="text-right ml-3">
                      <p className="font-bold text-sm text-kurios-secondary">
                        {formatCurrency(deal.kuriosMargin || deal.value * 0.3)}
                      </p>
                      <p className="text-[10px] text-gray-600">margin</p>
                    </div>
                  </div>
                  <div className="flex items-center justify-between mt-2.5">
                    <span className="text-[11px] text-gray-500 bg-white/[0.04] px-2 py-0.5 rounded">
                      {deal.nextAction}
                    </span>
                    <span className="text-[11px] text-gray-500">{deal.probability}% likely</span>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Activity Feed */}
        <div className="p-5 rounded-xl border border-kurios-border bg-kurios-card">
          <h2 className="font-semibold text-white mb-4">Recent Activity</h2>
          <div className="space-y-3.5">
            {activityFeed.slice(0, 5).map((activity) => {
              const Icon = activityIcons[activity.icon] || Clock;
              return (
                <div key={activity.id} className="flex items-start gap-3">
                  <div
                    className={`p-2 rounded-lg shrink-0 ${
                      activity.type === 'deal'
                        ? 'bg-kurios-secondary/10'
                        : activity.type === 'call'
                        ? 'bg-kurios-primary/10'
                        : 'bg-white/[0.04]'
                    }`}
                  >
                    <Icon
                      className={`w-4 h-4 ${
                        activity.type === 'deal'
                          ? 'text-kurios-secondary'
                          : activity.type === 'call'
                          ? 'text-kurios-primary'
                          : 'text-gray-500'
                      }`}
                    />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm text-gray-300 leading-snug">{activity.message}</p>
                    <p className="text-[11px] text-gray-600 mt-0.5">
                      {formatRelativeTime(activity.timestamp)}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* ── Quick Actions ────────────────────────────────── */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {[
          { label: 'Log Call', modal: 'addCall', icon: Phone, gradient: 'from-kurios-primary to-blue-600' },
          { label: 'Add Deal', modal: 'addDeal', icon: Plus, gradient: 'from-kurios-accent to-purple-600' },
          { label: 'New Lead', modal: 'addContact', icon: Zap, gradient: 'from-amber-500 to-orange-600' },
          { label: 'View Pipeline', link: '/pipeline', icon: TrendingUp, gradient: 'from-kurios-secondary to-emerald-600' },
        ].map((action) =>
          action.link ? (
            <Link
              key={action.label}
              to={action.link}
              className="flex items-center gap-3 p-4 rounded-xl border border-kurios-border bg-kurios-card hover:bg-kurios-card-hover hover:border-kurios-border-hover transition-all group"
            >
              <div className={`p-2 rounded-lg bg-gradient-to-br ${action.gradient} shadow-lg`}>
                <action.icon className="w-5 h-5 text-white" />
              </div>
              <span className="font-medium text-sm text-gray-300 group-hover:text-white transition-colors">
                {action.label}
              </span>
            </Link>
          ) : (
            <button
              key={action.label}
              onClick={() => openModal(action.modal)}
              className="flex items-center gap-3 p-4 rounded-xl border border-kurios-border bg-kurios-card hover:bg-kurios-card-hover hover:border-kurios-border-hover transition-all group text-left"
            >
              <div className={`p-2 rounded-lg bg-gradient-to-br ${action.gradient} shadow-lg`}>
                <action.icon className="w-5 h-5 text-white" />
              </div>
              <span className="font-medium text-sm text-gray-300 group-hover:text-white transition-colors">
                {action.label}
              </span>
            </button>
          )
        )}
      </div>

      {/* ── State Performance ────────────────────────────── */}
      <div className="p-5 rounded-xl border border-kurios-border bg-kurios-card">
        <div className="flex items-center justify-between mb-4">
          <h2 className="font-semibold text-white">State Performance</h2>
          <Link
            to="/analytics"
            className="text-xs text-kurios-primary hover:text-kurios-primary/80 font-medium transition-colors"
          >
            View details →
          </Link>
        </div>
        <div className="grid grid-cols-3 md:grid-cols-5 lg:grid-cols-9 gap-3">
          {stateData.map((state) => (
            <div
              key={state.state}
              className="p-3 rounded-lg bg-white/[0.03] border border-white/[0.04] text-center hover:border-kurios-primary/30 transition-colors"
            >
              <p className="text-lg font-bold text-white">{state.state}</p>
              <p className="text-xs font-medium text-kurios-secondary mt-0.5">
                {state.conversion}%
              </p>
              <p className="text-[10px] text-gray-600">
                {state.clients} client{state.clients !== 1 ? 's' : ''}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
