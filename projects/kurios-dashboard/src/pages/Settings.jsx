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
  Target
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

  const handleProfileChange = (key, value) => {
    updateSettings('profile', { [key]: value });
  };

  const handleNotificationChange = (key, value) => {
    updateSettings('notifications', { [key]: value });
  };

  const handleAppearanceChange = (key, value) => {
    updateSettings('appearance', { [key]: value });
  };

  const handleIntegrationToggle = (key) => {
    updateSettings('integrations', { [key]: !settings.integrations[key] });
    addToast({ 
      type: 'success', 
      message: `${key} ${settings.integrations[key] ? 'disabled' : 'enabled'}` 
    });
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

  return (
    <div className="animate-fadeIn">
      <div className="flex flex-col md:flex-row gap-6">
        {/* Sidebar */}
        <div className={`md:w-64 p-4 rounded-xl border ${
          darkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'
        }`}>
          <nav className="space-y-1">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                  activeTab === tab.id
                    ? 'bg-kurios-primary text-white'
                    : darkMode
                    ? 'text-gray-400 hover:text-white hover:bg-gray-700'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                }`}
              >
                <tab.icon className="w-5 h-5" />
                <span className="font-medium">{tab.label}</span>
              </button>
            ))}
          </nav>
        </div>

        {/* Content */}
        <div className={`flex-1 p-6 rounded-xl border ${
          darkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'
        }`}>
          {/* Profile */}
          {activeTab === 'profile' && (
            <div className="space-y-6">
              <div>
                <h2 className={`text-xl font-semibold mb-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                  Profile Settings
                </h2>
                
                {/* Goal reminder */}
                <div className={`p-4 rounded-lg mb-6 ${
                  darkMode ? 'bg-kurios-primary/10 border border-kurios-primary/30' : 'bg-kurios-primary/5 border border-kurios-primary/20'
                }`}>
                  <div className="flex items-center gap-3">
                    <Music className="w-6 h-6 text-kurios-primary" />
                    <div>
                      <p className={`font-medium ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                        Goal: {formatCurrency(GOAL.total)} → Retire to Music 🎵
                      </p>
                      <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                        Deadline: December 2026
                      </p>
                    </div>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className={`block text-sm font-medium mb-2 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                      Name
                    </label>
                    <input
                      type="text"
                      value={settings.profile.name}
                      onChange={(e) => handleProfileChange('name', e.target.value)}
                      className={`w-full px-4 py-2 rounded-lg border ${
                        darkMode
                          ? 'bg-gray-700 border-gray-600 text-white'
                          : 'bg-white border-gray-300 text-gray-900'
                      } focus:outline-none focus:ring-2 focus:ring-kurios-primary/20 focus:border-kurios-primary`}
                    />
                  </div>
                  <div>
                    <label className={`block text-sm font-medium mb-2 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                      Stage Name
                    </label>
                    <input
                      type="text"
                      value={settings.profile.stageName || ''}
                      onChange={(e) => handleProfileChange('stageName', e.target.value)}
                      className={`w-full px-4 py-2 rounded-lg border ${
                        darkMode
                          ? 'bg-gray-700 border-gray-600 text-white'
                          : 'bg-white border-gray-300 text-gray-900'
                      } focus:outline-none focus:ring-2 focus:ring-kurios-primary/20 focus:border-kurios-primary`}
                    />
                  </div>
                  <div>
                    <label className={`block text-sm font-medium mb-2 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                      Email
                    </label>
                    <input
                      type="email"
                      value={settings.profile.email}
                      onChange={(e) => handleProfileChange('email', e.target.value)}
                      className={`w-full px-4 py-2 rounded-lg border ${
                        darkMode
                          ? 'bg-gray-700 border-gray-600 text-white'
                          : 'bg-white border-gray-300 text-gray-900'
                      } focus:outline-none focus:ring-2 focus:ring-kurios-primary/20 focus:border-kurios-primary`}
                    />
                  </div>
                  <div>
                    <label className={`block text-sm font-medium mb-2 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                      Role
                    </label>
                    <input
                      type="text"
                      value={settings.profile.role}
                      onChange={(e) => handleProfileChange('role', e.target.value)}
                      className={`w-full px-4 py-2 rounded-lg border ${
                        darkMode
                          ? 'bg-gray-700 border-gray-600 text-white'
                          : 'bg-white border-gray-300 text-gray-900'
                      } focus:outline-none focus:ring-2 focus:ring-kurios-primary/20 focus:border-kurios-primary`}
                    />
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Notifications */}
          {activeTab === 'notifications' && (
            <div className="space-y-6">
              <h2 className={`text-xl font-semibold mb-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                Notification Preferences
              </h2>
              
              <div className="space-y-4">
                {Object.entries(settings.notifications).map(([key, value]) => (
                  <div 
                    key={key}
                    className={`flex items-center justify-between p-4 rounded-lg ${
                      darkMode ? 'bg-gray-700' : 'bg-gray-50'
                    }`}
                  >
                    <div>
                      <p className={`font-medium ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                        {key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}
                      </p>
                      <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                        {key === 'email' && 'Receive email notifications'}
                        {key === 'push' && 'Receive push notifications'}
                        {key === 'dealUpdates' && 'Get notified when deals move'}
                        {key === 'callReminders' && 'Remind me about scheduled calls'}
                      </p>
                    </div>
                    <button
                      onClick={() => handleNotificationChange(key, !value)}
                      className={`relative w-12 h-6 rounded-full transition-colors ${
                        value ? 'bg-kurios-primary' : darkMode ? 'bg-gray-600' : 'bg-gray-300'
                      }`}
                    >
                      <span 
                        className={`absolute top-1 w-4 h-4 rounded-full bg-white transition-transform ${
                          value ? 'translate-x-7' : 'translate-x-1'
                        }`}
                      />
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Appearance */}
          {activeTab === 'appearance' && (
            <div className="space-y-6">
              <h2 className={`text-xl font-semibold mb-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                Appearance
              </h2>
              
              <div className="space-y-4">
                {/* Dark mode toggle */}
                <div className={`p-4 rounded-lg ${darkMode ? 'bg-gray-700' : 'bg-gray-50'}`}>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      {darkMode ? <Moon className="w-5 h-5 text-kurios-primary" /> : <Sun className="w-5 h-5 text-orange-500" />}
                      <div>
                        <p className={`font-medium ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                          Dark Mode
                        </p>
                        <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                          Perfect for late night work sessions 🌙
                        </p>
                      </div>
                    </div>
                    <button
                      onClick={() => handleAppearanceChange('darkMode', !darkMode)}
                      className={`relative w-12 h-6 rounded-full transition-colors ${
                        darkMode ? 'bg-kurios-primary' : 'bg-gray-300'
                      }`}
                    >
                      <span 
                        className={`absolute top-1 w-4 h-4 rounded-full bg-white transition-transform ${
                          darkMode ? 'translate-x-7' : 'translate-x-1'
                        }`}
                      />
                    </button>
                  </div>
                </div>

                {/* Compact mode */}
                <div className={`p-4 rounded-lg ${darkMode ? 'bg-gray-700' : 'bg-gray-50'}`}>
                  <div className="flex items-center justify-between">
                    <div>
                      <p className={`font-medium ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                        Compact Mode
                      </p>
                      <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                        Denser layout, more data on screen
                      </p>
                    </div>
                    <button
                      onClick={() => handleAppearanceChange('compactMode', !settings.appearance.compactMode)}
                      className={`relative w-12 h-6 rounded-full transition-colors ${
                        settings.appearance.compactMode ? 'bg-kurios-primary' : darkMode ? 'bg-gray-600' : 'bg-gray-300'
                      }`}
                    >
                      <span 
                        className={`absolute top-1 w-4 h-4 rounded-full bg-white transition-transform ${
                          settings.appearance.compactMode ? 'translate-x-7' : 'translate-x-1'
                        }`}
                      />
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Integrations */}
          {activeTab === 'integrations' && (
            <div className="space-y-6">
              <h2 className={`text-xl font-semibold mb-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                Integrations
              </h2>
              
              <div className="space-y-4">
                {Object.entries(settings.integrations).map(([key, value]) => (
                  <div 
                    key={key}
                    className={`p-4 rounded-lg border ${
                      value 
                        ? 'border-kurios-secondary/50 bg-kurios-secondary/5' 
                        : darkMode ? 'bg-gray-700 border-gray-600' : 'bg-gray-50 border-gray-200'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <p className={`font-medium ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                          {key === 'patrick' ? 'Patrick Pipeline' : 
                           key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}
                        </p>
                        <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                          {key === 'googleCalendar' && 'Sync with Google Calendar'}
                          {key === 'slack' && 'Send notifications to Slack'}
                          {key === 'patrick' && 'Route deals through Patrick intake'}
                        </p>
                      </div>
                      <button
                        onClick={() => handleIntegrationToggle(key)}
                        className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                          value
                            ? 'bg-kurios-secondary text-white'
                            : darkMode
                            ? 'bg-gray-600 text-gray-300 hover:bg-gray-500'
                            : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                        }`}
                      >
                        {value ? 'Connected' : 'Connect'}
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Data */}
          {activeTab === 'data' && (
            <div className="space-y-6">
              <h2 className={`text-xl font-semibold mb-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                Data Management
              </h2>
              
              {/* Export */}
              <div>
                <h3 className={`font-medium mb-3 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                  Export Data
                </h3>
                <div className="flex flex-wrap gap-3">
                  <button
                    onClick={() => handleExportData('deals')}
                    className={`flex items-center gap-2 px-4 py-2 rounded-lg border ${
                      darkMode
                        ? 'border-gray-600 text-gray-300 hover:bg-gray-700'
                        : 'border-gray-200 text-gray-700 hover:bg-gray-50'
                    } transition-colors`}
                  >
                    <Download className="w-4 h-4" />
                    Export Deals
                  </button>
                  <button
                    onClick={() => handleExportData('clients')}
                    className={`flex items-center gap-2 px-4 py-2 rounded-lg border ${
                      darkMode
                        ? 'border-gray-600 text-gray-300 hover:bg-gray-700'
                        : 'border-gray-200 text-gray-700 hover:bg-gray-50'
                    } transition-colors`}
                  >
                    <Download className="w-4 h-4" />
                    Export Clients
                  </button>
                  <button
                    onClick={() => handleExportData('contacts')}
                    className={`flex items-center gap-2 px-4 py-2 rounded-lg border ${
                      darkMode
                        ? 'border-gray-600 text-gray-300 hover:bg-gray-700'
                        : 'border-gray-200 text-gray-700 hover:bg-gray-50'
                    } transition-colors`}
                  >
                    <Download className="w-4 h-4" />
                    Export Contacts
                  </button>
                </div>
              </div>

              {/* Reset */}
              <div className={`p-4 rounded-lg border border-red-500/30 ${
                darkMode ? 'bg-red-900/10' : 'bg-red-50'
              }`}>
                <h3 className="font-medium text-red-500 mb-2">Danger Zone</h3>
                <p className={`text-sm mb-3 ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                  Reset all data to defaults. This cannot be undone.
                </p>
                <button
                  onClick={handleReset}
                  className="flex items-center gap-2 px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
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
