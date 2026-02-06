import { useState } from 'react';
import {
  User,
  Bell,
  Palette,
  Link as LinkIcon,
  Shield,
  Download,
  RotateCcw,
  Sun,
  Moon,
  Music,
} from 'lucide-react';
import useStore from '../stores/useStore';
import { GOAL } from '../data/sampleData';
import { formatCurrency, exportToCSV } from '../utils/helpers';

export default function Settings() {
  const { settings, updateSettings, resetData, addToast, deals, clients, contacts } = useStore();
  const darkMode = settings.appearance.darkMode;
  const [activeTab, setActiveTab] = useState('profile');

  const tabs = [
    { id: 'profile', label: 'Profile', icon: User },
    { id: 'notifications', label: 'Notifications', icon: Bell },
    { id: 'appearance', label: 'Appearance', icon: Palette },
    { id: 'integrations', label: 'Integrations', icon: LinkIcon },
    { id: 'data', label: 'Data', icon: Shield },
  ];

  const handleProfileChange = (key, value) => updateSettings('profile', { [key]: value });
  const handleNotificationChange = (key, value) => updateSettings('notifications', { [key]: value });
  const handleAppearanceChange = (key, value) => updateSettings('appearance', { [key]: value });

  const handleIntegrationToggle = (key) => {
    updateSettings('integrations', { [key]: !settings.integrations[key] });
    addToast({ type: 'success', message: `${key} ${settings.integrations[key] ? 'disabled' : 'enabled'}` });
  };

  const handleExportData = (type) => {
    const data = type === 'deals' ? deals : type === 'clients' ? clients : contacts;
    exportToCSV(data, type);
    addToast({ type: 'success', message: `${type} exported successfully` });
  };

  const handleReset = () => {
    if (confirm('Are you sure? This will reset all data to defaults.')) {
      resetData();
      addToast({ type: 'success', message: 'Data reset to defaults' });
    }
  };

  const inputClass =
    'w-full px-4 py-2.5 rounded-lg bg-white/[0.04] border border-kurios-border text-sm text-white placeholder-gray-500 focus:outline-none focus:border-kurios-primary/50 focus:ring-1 focus:ring-kurios-primary/20 transition-all';

  const Toggle = ({ checked, onChange }) => (
    <button
      onClick={onChange}
      className={`relative w-11 h-6 rounded-full transition-colors ${
        checked ? 'bg-kurios-primary' : 'bg-white/[0.08]'
      }`}
    >
      <span
        className={`absolute top-1 w-4 h-4 rounded-full bg-white transition-transform ${
          checked ? 'translate-x-6' : 'translate-x-1'
        }`}
      />
    </button>
  );

  return (
    <div className="animate-fadeIn">
      <div className="flex flex-col md:flex-row gap-6">
        {/* Sidebar */}
        <div className="md:w-56 shrink-0">
          <nav className="p-2 rounded-xl border border-kurios-border bg-kurios-card space-y-0.5">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-lg transition-all text-sm ${
                  activeTab === tab.id
                    ? 'bg-kurios-primary/15 text-kurios-primary font-medium'
                    : 'text-gray-400 hover:text-white hover:bg-white/[0.04]'
                }`}
              >
                <tab.icon className="w-[18px] h-[18px]" />
                {tab.label}
              </button>
            ))}
          </nav>
        </div>

        {/* Content */}
        <div className="flex-1 p-6 rounded-xl border border-kurios-border bg-kurios-card">
          {/* Profile */}
          {activeTab === 'profile' && (
            <div className="space-y-6">
              <h2 className="text-lg font-semibold text-white">Profile Settings</h2>

              {/* Goal reminder */}
              <div className="p-4 rounded-lg bg-kurios-primary/[0.06] border border-kurios-primary/20">
                <div className="flex items-center gap-3">
                  <Music className="w-5 h-5 text-kurios-primary" />
                  <div>
                    <p className="font-medium text-sm text-white">
                      Goal: {formatCurrency(GOAL.total)} → Retire to Music 🎵
                    </p>
                    <p className="text-xs text-gray-500">Deadline: December 2026</p>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {[
                  { key: 'name', label: 'Name' },
                  { key: 'stageName', label: 'Stage Name' },
                  { key: 'email', label: 'Email', type: 'email' },
                  { key: 'role', label: 'Role' },
                ].map((field) => (
                  <div key={field.key}>
                    <label className="block text-xs font-medium text-gray-400 mb-1.5">
                      {field.label}
                    </label>
                    <input
                      type={field.type || 'text'}
                      value={settings.profile[field.key] || ''}
                      onChange={(e) => handleProfileChange(field.key, e.target.value)}
                      className={inputClass}
                    />
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Notifications */}
          {activeTab === 'notifications' && (
            <div className="space-y-6">
              <h2 className="text-lg font-semibold text-white">Notification Preferences</h2>
              <div className="space-y-3">
                {Object.entries(settings.notifications).map(([key, value]) => {
                  const descriptions = {
                    email: 'Receive email notifications',
                    push: 'Receive push notifications',
                    dealUpdates: 'Get notified when deals move',
                    callReminders: 'Remind me about scheduled calls',
                  };
                  return (
                    <div key={key} className="flex items-center justify-between p-4 rounded-lg bg-white/[0.02] border border-kurios-border">
                      <div>
                        <p className="text-sm font-medium text-white">
                          {key.replace(/([A-Z])/g, ' $1').replace(/^./, (s) => s.toUpperCase())}
                        </p>
                        <p className="text-xs text-gray-500">{descriptions[key]}</p>
                      </div>
                      <Toggle checked={value} onChange={() => handleNotificationChange(key, !value)} />
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* Appearance */}
          {activeTab === 'appearance' && (
            <div className="space-y-6">
              <h2 className="text-lg font-semibold text-white">Appearance</h2>
              <div className="space-y-3">
                <div className="flex items-center justify-between p-4 rounded-lg bg-white/[0.02] border border-kurios-border">
                  <div className="flex items-center gap-3">
                    {darkMode ? (
                      <Moon className="w-5 h-5 text-kurios-primary" />
                    ) : (
                      <Sun className="w-5 h-5 text-amber-400" />
                    )}
                    <div>
                      <p className="text-sm font-medium text-white">Dark Mode</p>
                      <p className="text-xs text-gray-500">Perfect for late night sessions 🌙</p>
                    </div>
                  </div>
                  <Toggle
                    checked={darkMode}
                    onChange={() => handleAppearanceChange('darkMode', !darkMode)}
                  />
                </div>
                <div className="flex items-center justify-between p-4 rounded-lg bg-white/[0.02] border border-kurios-border">
                  <div>
                    <p className="text-sm font-medium text-white">Compact Mode</p>
                    <p className="text-xs text-gray-500">Denser layout, more data on screen</p>
                  </div>
                  <Toggle
                    checked={settings.appearance.compactMode}
                    onChange={() =>
                      handleAppearanceChange('compactMode', !settings.appearance.compactMode)
                    }
                  />
                </div>
              </div>
            </div>
          )}

          {/* Integrations */}
          {activeTab === 'integrations' && (
            <div className="space-y-6">
              <h2 className="text-lg font-semibold text-white">Integrations</h2>
              <div className="space-y-3">
                {Object.entries(settings.integrations).map(([key, value]) => {
                  const descriptions = {
                    googleCalendar: 'Sync with Google Calendar',
                    slack: 'Send notifications to Slack',
                    patrick: 'Route deals through Patrick intake',
                  };
                  return (
                    <div
                      key={key}
                      className={`p-4 rounded-lg border transition-colors ${
                        value
                          ? 'border-kurios-secondary/30 bg-kurios-secondary/[0.04]'
                          : 'border-kurios-border bg-white/[0.02]'
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-sm font-medium text-white">
                            {key === 'patrick'
                              ? 'Patrick Pipeline'
                              : key.replace(/([A-Z])/g, ' $1').replace(/^./, (s) => s.toUpperCase())}
                          </p>
                          <p className="text-xs text-gray-500">{descriptions[key]}</p>
                        </div>
                        <button
                          onClick={() => handleIntegrationToggle(key)}
                          className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                            value
                              ? 'bg-kurios-secondary text-white'
                              : 'bg-white/[0.06] text-gray-400 hover:bg-white/[0.1]'
                          }`}
                        >
                          {value ? 'Connected' : 'Connect'}
                        </button>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* Data */}
          {activeTab === 'data' && (
            <div className="space-y-6">
              <h2 className="text-lg font-semibold text-white">Data Management</h2>

              {/* Export */}
              <div>
                <h3 className="text-sm font-medium text-gray-400 mb-3">Export Data</h3>
                <div className="flex flex-wrap gap-3">
                  {['deals', 'clients', 'contacts'].map((type) => (
                    <button
                      key={type}
                      onClick={() => handleExportData(type)}
                      className="flex items-center gap-2 px-4 py-2.5 rounded-lg border border-kurios-border text-sm text-gray-300 hover:bg-white/[0.04] transition-colors"
                    >
                      <Download className="w-4 h-4" />
                      Export {type.charAt(0).toUpperCase() + type.slice(1)}
                    </button>
                  ))}
                </div>
              </div>

              {/* Reset */}
              <div className="p-4 rounded-lg border border-red-500/20 bg-red-500/[0.04]">
                <h3 className="text-sm font-medium text-red-400 mb-1">Danger Zone</h3>
                <p className="text-xs text-gray-500 mb-3">
                  Reset all data to defaults. This cannot be undone.
                </p>
                <button
                  onClick={handleReset}
                  className="flex items-center gap-2 px-4 py-2 bg-red-500/20 text-red-400 border border-red-500/30 rounded-lg text-sm hover:bg-red-500/30 transition-colors"
                >
                  <RotateCcw className="w-4 h-4" />
                  Reset All Data
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
