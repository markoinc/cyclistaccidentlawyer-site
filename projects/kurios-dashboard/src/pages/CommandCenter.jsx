import { 
  DollarSign, Filter, Building2, FolderKanban, Flame, HeartPulse,
  TrendingUp, Zap, FunnelIcon, Target, Activity, Handshake, Phone, Mail, Bot
} from 'lucide-react';
import { useDashboard, useStats } from '../context/DashboardContext';
import { Card, CardHeader, CardBody, StatCard, Button, StatusPill, PriorityBadge } from '../components/UI';
import { RevenueChart, PipelineChart } from '../components/charts';

export function CommandCenter() {
  const { state, dispatch, showToast } = useDashboard();
  const { closedRevenue, pipelineValue, activeProspects, activeProjects, goalPercent } = useStats();

  const handleToggleTask = (taskId) => {
    dispatch({ type: 'TOGGLE_TASK', payload: taskId });
    const task = state.tasks.find(t => t.id === taskId);
    if (task && !task.completed) {
      showToast('Task completed! 🎉', 'success');
    }
  };

  const pipelineByStage = {
    hot: state.prospects.filter(p => ['proposal', 'negotiation'].includes(p.stage)),
    progress: state.prospects.filter(p => ['lead', 'qualified'].includes(p.stage)),
    closed: state.prospects.filter(p => p.stage === 'closed'),
  };

  const activities = [
    { icon: Handshake, color: 'success', title: 'Jason E closed - $9,525', time: 'Jan 2026' },
    { icon: Phone, color: 'info', title: 'Patrick call with Scott Barney', time: '2 days ago' },
    { icon: Mail, color: 'warning', title: 'Proposal sent to Lucas', time: 'Today' },
    { icon: Bot, color: 'purple', title: 'AI Intake Agent 90% complete', time: 'Needs API key' },
  ];

  const activityColors = {
    success: 'bg-[#00E676]/15 text-[#00E676]',
    info: 'bg-[#3366FF]/15 text-[#3366FF]',
    warning: 'bg-[#ffb347]/15 text-[#ffb347]',
    purple: 'bg-[#a855f7]/15 text-[#a855f7]',
  };

  return (
    <div className="p-6 animate-fadeIn">
      {/* Hero Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4 mb-6">
        <StatCard
          label="Revenue (Closed)"
          value={`$${closedRevenue.toLocaleString()}`}
          trend="First close of 2026"
          trendUp={true}
          icon={DollarSign}
          color="success"
          onClick={() => dispatch({ type: 'SET_PAGE', payload: 'financial' })}
        />
        <StatCard
          label="Pipeline Value (10%)"
          value={`$${Math.round(pipelineValue).toLocaleString()}`}
          trend={`${activeProspects} active prospects`}
          trendUp={true}
          icon={Filter}
          color="primary"
          onClick={() => dispatch({ type: 'SET_PAGE', payload: 'pipeline' })}
        />
        <StatCard
          label="Active Clients"
          value="24"
          trend="15+ states covered"
          trendUp={true}
          icon={Building2}
          color="gradient"
          onClick={() => dispatch({ type: 'SET_PAGE', payload: 'clients' })}
        />
        <StatCard
          label="Active Projects"
          value={activeProjects.toString()}
          trend="2 stalled"
          trendUp={null}
          icon={FolderKanban}
          color="warning"
          onClick={() => dispatch({ type: 'SET_PAGE', payload: 'projects' })}
        />
        <StatCard
          label="Monthly Burn"
          value="$900"
          trend="Review Feb 3"
          trendUp={false}
          icon={Flame}
          color="danger"
          onClick={() => dispatch({ type: 'OPEN_MODAL', payload: { type: 'expense' } })}
        />
        <StatCard
          label="Business Health"
          value="78%"
          trend="Improving"
          trendUp={true}
          icon={HeartPulse}
          color="success"
          onClick={() => dispatch({ type: 'OPEN_MODAL', payload: { type: 'health' } })}
        />
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-12 gap-5">
        {/* Revenue Chart */}
        <Card className="col-span-12 lg:col-span-8">
          <CardHeader 
            actions={
              <div className="flex gap-2">
                <Button size="sm" variant="ghost">Weekly</Button>
                <Button size="sm" variant="primary">Monthly</Button>
                <Button size="sm" variant="ghost">Quarterly</Button>
              </div>
            }
          >
            <TrendingUp size={16} className="text-[#3366FF]" />
            Revenue & Pipeline Tracking
          </CardHeader>
          <CardBody>
            <RevenueChart />
          </CardBody>
        </Card>

        {/* Priority Actions */}
        <Card className="col-span-12 lg:col-span-4">
          <CardHeader 
            actions={
              <Button 
                size="sm" 
                variant="ghost" 
                onClick={() => dispatch({ type: 'OPEN_MODAL', payload: { type: 'addTask' } })}
              >
                + Add
              </Button>
            }
          >
            <Zap size={16} className="text-[#3366FF]" />
            Priority Actions
          </CardHeader>
          <CardBody noPadding>
            <div className="divide-y divide-[#2d333b]">
              {state.tasks.slice(0, 4).map(task => (
                <div key={task.id} className={`flex items-start gap-3 p-4 hover:bg-[#353d47] transition-colors ${task.completed ? 'opacity-50' : ''}`}>
                  <button
                    onClick={() => handleToggleTask(task.id)}
                    className={`
                      w-5 h-5 rounded-full border-2 flex-shrink-0 mt-0.5 flex items-center justify-center transition-all
                      ${task.completed 
                        ? 'bg-[#00E676] border-[#00E676] text-[#14171A]' 
                        : 'border-[#444d56] hover:border-[#00E676]'}
                    `}
                  >
                    {task.completed && '✓'}
                  </button>
                  <div className="flex-1 min-w-0">
                    <div className={`text-sm font-medium mb-1 ${task.completed ? 'line-through text-[#6e7681]' : ''}`}>
                      {task.title}
                    </div>
                    <div className="flex items-center gap-3 text-xs text-[#6e7681]">
                      <span className={`px-1.5 py-0.5 rounded text-[10px] font-semibold ${
                        task.priority === 'p0' ? 'bg-[#ff6b6b]/15 text-[#ff6b6b]' : 'bg-[#ffb347]/15 text-[#ffb347]'
                      }`}>
                        {task.label}
                      </span>
                      <span>{task.value}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardBody>
        </Card>

        {/* Pipeline Summary */}
        <Card className="col-span-12 lg:col-span-6">
          <CardHeader 
            actions={
              <Button size="sm" variant="ghost" onClick={() => dispatch({ type: 'SET_PAGE', payload: 'pipeline' })}>
                View All
              </Button>
            }
          >
            <FunnelIcon size={16} className="text-[#3366FF]" />
            Pipeline Summary
          </CardHeader>
          <CardBody>
            <div className="grid grid-cols-3 gap-4 mb-5">
              <div 
                className="text-center p-4 bg-[#ff6b6b]/15 rounded-lg border-l-4 border-[#ff6b6b] cursor-pointer hover:bg-[#ff6b6b]/20 transition-colors"
                onClick={() => dispatch({ type: 'SET_PAGE', payload: 'pipeline' })}
              >
                <div className="text-3xl font-extrabold text-[#ff6b6b]">{pipelineByStage.hot.length}</div>
                <div className="text-xs text-[#6e7681] uppercase mb-1">🔥 Hot</div>
                <div className="text-sm font-semibold">${pipelineByStage.hot.reduce((s, p) => s + p.amount, 0).toLocaleString()}</div>
              </div>
              <div 
                className="text-center p-4 bg-[#ffb347]/15 rounded-lg border-l-4 border-[#ffb347] cursor-pointer hover:bg-[#ffb347]/20 transition-colors"
                onClick={() => dispatch({ type: 'SET_PAGE', payload: 'pipeline' })}
              >
                <div className="text-3xl font-extrabold text-[#ffb347]">{pipelineByStage.progress.length}</div>
                <div className="text-xs text-[#6e7681] uppercase mb-1">⏳ Progress</div>
                <div className="text-sm font-semibold">${pipelineByStage.progress.reduce((s, p) => s + p.amount, 0).toLocaleString()}</div>
              </div>
              <div 
                className="text-center p-4 bg-[#00E676]/15 rounded-lg border-l-4 border-[#00E676] cursor-pointer hover:bg-[#00E676]/20 transition-colors"
                onClick={() => dispatch({ type: 'SET_PAGE', payload: 'pipeline' })}
              >
                <div className="text-3xl font-extrabold text-[#00E676]">{pipelineByStage.closed.length}</div>
                <div className="text-xs text-[#6e7681] uppercase mb-1">✅ Closed</div>
                <div className="text-sm font-semibold">${pipelineByStage.closed.reduce((s, p) => s + p.amount, 0).toLocaleString()}</div>
              </div>
            </div>
            <PipelineChart />
          </CardBody>
        </Card>

        {/* Goal Progress */}
        <Card className="col-span-12 lg:col-span-6">
          <CardHeader 
            actions={
              <Button size="sm" variant="ghost" onClick={() => dispatch({ type: 'OPEN_MODAL', payload: { type: 'goal' } })}>
                Edit
              </Button>
            }
          >
            <Target size={16} className="text-[#3366FF]" />
            Exit Goal: $9.6M
          </CardHeader>
          <CardBody>
            <div className="text-center mb-5">
              <div className="text-4xl font-extrabold gradient-text">${state.goal.current.toLocaleString()}</div>
              <div className="text-sm text-[#6e7681]">{goalPercent}% of $9.6M goal</div>
            </div>
            <div className="h-4 bg-[#353d47] rounded-full overflow-hidden mb-5">
              <div 
                className="h-full gradient-brand rounded-full transition-all duration-500"
                style={{ width: `${Math.max(2, parseFloat(goalPercent))}%` }}
              />
            </div>
            <div className="flex justify-between mb-5">
              {[
                { icon: '✓', label: 'Start', value: '$0', active: true },
                { icon: '🎯', label: 'First 100K', value: '$100K', active: false },
                { icon: '🚀', label: 'Millionaire', value: '$1M', active: false },
                { icon: '💎', label: 'Halfway', value: '$5M', active: false },
                { icon: '👑', label: 'EXIT', value: '$9.6M', active: false },
              ].map((milestone, i) => (
                <div key={i} className={`text-center ${milestone.active ? '' : 'opacity-40'}`}>
                  <div className={`w-8 h-8 mx-auto mb-2 rounded-full flex items-center justify-center text-sm ${milestone.active ? 'bg-[#00E676] text-[#14171A]' : 'bg-[#353d47]'}`}>
                    {milestone.icon}
                  </div>
                  <div className="text-xs font-semibold">{milestone.value}</div>
                  <div className="text-[10px] text-[#6e7681]">{milestone.label}</div>
                </div>
              ))}
            </div>
            <div className="grid grid-cols-3 gap-4 pt-4 border-t border-[#2d333b]">
              <div className="text-center">
                <div className="text-xl font-bold text-[#3366FF]">380</div>
                <div className="text-[10px] text-[#6e7681]">Deals @ $25K avg</div>
              </div>
              <div className="text-center">
                <div className="text-xl font-bold text-[#ffb347]">32/mo</div>
                <div className="text-[10px] text-[#6e7681]">To hit in 1 year</div>
              </div>
              <div className="text-center">
                <div className="text-xl font-bold text-[#6e7681]">~10 yrs</div>
                <div className="text-[10px] text-[#6e7681]">At current pace</div>
              </div>
            </div>
          </CardBody>
        </Card>

        {/* Activity Feed */}
        <Card className="col-span-12 lg:col-span-4">
          <CardHeader>
            <Activity size={16} className="text-[#3366FF]" />
            Recent Activity
          </CardHeader>
          <CardBody noPadding>
            <div className="max-h-[300px] overflow-y-auto">
              {activities.map((activity, i) => {
                const Icon = activity.icon;
                return (
                  <div key={i} className="flex items-start gap-3 p-4 border-b border-[#2d333b] last:border-b-0 hover:bg-[#353d47] transition-colors">
                    <div className={`w-9 h-9 rounded-full flex items-center justify-center ${activityColors[activity.color]}`}>
                      <Icon size={16} />
                    </div>
                    <div>
                      <div className="text-sm font-medium">{activity.title}</div>
                      <div className="text-xs text-[#6e7681]">{activity.time}</div>
                    </div>
                  </div>
                );
              })}
            </div>
          </CardBody>
        </Card>

        {/* Active Projects */}
        <Card className="col-span-12 lg:col-span-8">
          <CardHeader 
            actions={
              <Button size="sm" variant="ghost" onClick={() => dispatch({ type: 'SET_PAGE', payload: 'projects' })}>
                View All
              </Button>
            }
          >
            <FolderKanban size={16} className="text-[#3366FF]" />
            Active Projects
          </CardHeader>
          <CardBody noPadding>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="bg-[#21262c] text-[11px] font-semibold text-[#6e7681] uppercase tracking-wider">
                    <th className="text-left px-5 py-3">Project</th>
                    <th className="text-left px-5 py-3">Status</th>
                    <th className="text-left px-5 py-3">Priority</th>
                    <th className="text-left px-5 py-3">Progress</th>
                    <th className="text-left px-5 py-3">Due</th>
                    <th className="text-left px-5 py-3">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#2d333b]">
                  {state.projects.slice(0, 3).map(project => (
                    <tr key={project.id} className="hover:bg-[#353d47] transition-colors">
                      <td className="px-5 py-4">
                        <div className="flex items-center gap-3">
                          <div className={`w-1 h-8 rounded ${
                            project.priority === 'p0' ? 'bg-[#ff6b6b]' : 
                            project.priority === 'p1' ? 'bg-[#ffb347]' : 'bg-[#3366FF]'
                          }`} />
                          <div>
                            <div className="font-semibold">{project.name}</div>
                            <div className="text-xs text-[#6e7681]">{project.description}</div>
                          </div>
                        </div>
                      </td>
                      <td className="px-5 py-4"><StatusPill status={project.status} /></td>
                      <td className="px-5 py-4">
                        <span className={`font-semibold ${
                          project.priority === 'p0' ? 'text-[#ff6b6b]' : 
                          project.priority === 'p1' ? 'text-[#ffb347]' : 'text-[#3366FF]'
                        }`}>
                          {project.priority.toUpperCase()}
                        </span>
                      </td>
                      <td className="px-5 py-4">
                        <div className="w-full max-w-[100px]">
                          <div className="h-1.5 bg-[#353d47] rounded-full overflow-hidden">
                            <div 
                              className={`h-full rounded-full ${
                                project.progress >= 75 ? 'bg-[#00E676]' : 
                                project.progress >= 50 ? 'bg-[#3366FF]' : 'bg-[#ffb347]'
                              }`}
                              style={{ width: `${project.progress}%` }}
                            />
                          </div>
                          <div className="text-xs text-[#6e7681] mt-1">{project.progress}%</div>
                        </div>
                      </td>
                      <td className="px-5 py-4 text-sm text-[#6e7681]">{project.due}</td>
                      <td className="px-5 py-4">
                        <Button 
                          size="sm" 
                          variant={project.status === 'in-progress' ? 'primary' : 'ghost'}
                          onClick={() => dispatch({ type: 'OPEN_MODAL', payload: { type: 'editProject', data: project } })}
                        >
                          {project.status === 'in-progress' ? 'Continue' : 'Open'}
                        </Button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardBody>
        </Card>
      </div>
    </div>
  );
}
