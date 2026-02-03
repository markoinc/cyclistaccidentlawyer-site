import { Plus, Upload, Bot, Mail, Clock, UserPlus, Phone, CheckCircle } from 'lucide-react';
import { useDashboard } from '../context/DashboardContext';
import { Button, Card, CardBody } from '../components/UI';

const iconMap = {
  robot: Bot,
  mail: Mail,
};

const colorMap = {
  success: { bg: 'bg-[#00E676]/15', text: 'text-[#00E676]' },
  info: { bg: 'bg-[#3366FF]/15', text: 'text-[#3366FF]' },
  warning: { bg: 'bg-[#ffb347]/15', text: 'text-[#ffb347]' },
  purple: { bg: 'bg-[#a855f7]/15', text: 'text-[#a855f7]' },
};

export function Automations() {
  const { state, dispatch, showToast } = useDashboard();

  const handleToggle = (id) => {
    dispatch({ type: 'TOGGLE_AUTOMATION', payload: id });
    const automation = state.automations.find(a => a.id === id);
    showToast(
      `${automation?.name} ${automation?.active ? 'disabled' : 'enabled'}`,
      automation?.active ? 'info' : 'success'
    );
  };

  const handleImportTemplate = () => {
    showToast('Template library coming soon!', 'info');
  };

  return (
    <div className="p-6 animate-fadeIn">
      {/* Actions */}
      <div className="flex flex-wrap gap-3 mb-6">
        <Button onClick={() => dispatch({ type: 'OPEN_MODAL', payload: { type: 'addAutomation' } })}>
          <Plus size={16} /> Create Automation
        </Button>
        <Button variant="outline" onClick={handleImportTemplate}>
          <Upload size={16} /> Import Template
        </Button>
      </div>

      {/* Automations List */}
      <div className="space-y-4">
        {state.automations.map(automation => {
          const Icon = iconMap[automation.icon] || Bot;
          const colors = colorMap[automation.color] || colorMap.info;

          return (
            <Card key={automation.id}>
              <CardBody>
                {/* Header */}
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${colors.bg} ${colors.text}`}>
                      <Icon size={20} />
                    </div>
                    <div>
                      <div className="font-semibold">{automation.name}</div>
                      <div className="text-sm text-[#6e7681]">{automation.description}</div>
                    </div>
                  </div>
                  <button
                    onClick={() => handleToggle(automation.id)}
                    className={`
                      w-12 h-6 rounded-full relative cursor-pointer transition-colors duration-200
                      ${automation.active ? 'bg-[#00E676]' : 'bg-[#353d47]'}
                    `}
                  >
                    <span className={`
                      absolute top-0.5 w-5 h-5 bg-white rounded-full shadow transition-transform duration-200
                      ${automation.active ? 'translate-x-6' : 'translate-x-0.5'}
                    `} />
                  </button>
                </div>

                {/* Flow */}
                <div className="flex items-center gap-3 p-4 bg-[#21262c] rounded-lg overflow-x-auto mb-4">
                  {automation.id === '1' ? (
                    <>
                      <FlowStep icon={UserPlus} label="New Lead" />
                      <FlowArrow />
                      <FlowStep icon={Bot} label="AI Qualification" />
                      <FlowArrow />
                      <FlowStep icon={Phone} label="Live Transfer" />
                      <FlowArrow />
                      <FlowStep icon={CheckCircle} label="Case Signed" />
                    </>
                  ) : (
                    <>
                      <FlowStep icon={Clock} label="Day 1" />
                      <FlowArrow />
                      <FlowStep icon={Mail} label="Email 1" />
                      <FlowArrow />
                      <FlowStep icon={Clock} label="Day 3" />
                      <FlowArrow />
                      <FlowStep icon={Mail} label="Email 2" />
                    </>
                  )}
                </div>

                {/* Stats */}
                <div className="grid grid-cols-3 gap-4 pt-4 border-t border-[#2d333b]">
                  {automation.savings && (
                    <>
                      <div className="text-center">
                        <div className="text-lg font-bold text-[#00E676]">{automation.savings}</div>
                        <div className="text-xs text-[#6e7681]">Annual Savings</div>
                      </div>
                      <div className="text-center">
                        <div className="text-lg font-bold">{automation.completion}%</div>
                        <div className="text-xs text-[#6e7681]">Complete</div>
                      </div>
                      <div className="text-center">
                        <div className="text-lg font-bold text-[#ffb347]">{automation.needs}</div>
                        <div className="text-xs text-[#6e7681]">Needs</div>
                      </div>
                    </>
                  )}
                  {automation.runs && (
                    <>
                      <div className="text-center">
                        <div className="text-lg font-bold">{automation.runs}</div>
                        <div className="text-xs text-[#6e7681]">Total Runs</div>
                      </div>
                      <div className="text-center">
                        <div className="text-lg font-bold text-[#00E676]">{automation.opens}</div>
                        <div className="text-xs text-[#6e7681]">Open Rate</div>
                      </div>
                      <div className="text-center">
                        <div className="text-lg font-bold text-[#3366FF]">Active</div>
                        <div className="text-xs text-[#6e7681]">Status</div>
                      </div>
                    </>
                  )}
                </div>
              </CardBody>
            </Card>
          );
        })}
      </div>
    </div>
  );
}

function FlowStep({ icon: Icon, label }) {
  return (
    <div className="flex items-center gap-2 px-3 py-2 bg-[#242930] border border-[#444d56] rounded-lg text-sm whitespace-nowrap">
      <Icon size={14} />
      <span>{label}</span>
    </div>
  );
}

function FlowArrow() {
  return <span className="text-[#3366FF] font-bold">→</span>;
}
