import { useState } from 'react';
import { useLocation } from 'react-router-dom';
import { 
  Search, 
  Bell, 
  Sun, 
  Moon, 
  Plus,
  ChevronDown
} from 'lucide-react';
import useStore from '../../stores/useStore';
import { getInitials, getAvatarColor } from '../../utils/helpers';

const pageTitles = {
  '/': 'Dashboard',
  '/pipeline': 'Sales Pipeline',
  '/projects': 'Projects',
  '/contacts': 'Contacts',
  '/clients': 'Clients',
  '/analytics': 'Analytics',
  '/ideas': 'Ideas Backlog',
  '/settings': 'Settings',
};

export default function TopBar() {
  const location = useLocation();
  const { 
    settings, 
    toggleDarkMode, 
    searchQuery, 
    setSearchQuery,
    openModal,
    sidebarCollapsed 
  } = useStore();
  
  const darkMode = settings.appearance.darkMode;
  const [showNotifications, setShowNotifications] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [showQuickAdd, setShowQuickAdd] = useState(false);

  const pageTitle = pageTitles[location.pathname] || 'Dashboard';

  return (
    <header 
      className={`fixed top-0 right-0 h-16 ${
        sidebarCollapsed ? 'left-20' : 'left-64'
      } ${
        darkMode ? 'bg-kurios-darker/95 border-gray-800' : 'bg-white/95 border-gray-200'
      } border-b backdrop-blur-sm z-40 transition-all duration-300`}
    >
      <div className="h-full px-6 flex items-center justify-between">
        {/* Page title */}
        <div className="flex items-center gap-4">
          <h1 className={`text-2xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
            {pageTitle}
          </h1>
        </div>

        {/* Actions */}
        <div className="flex items-center gap-4">
          {/* Search */}
          <div className={`relative ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4" />
            <input
              type="text"
              placeholder="Search..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className={`pl-10 pr-4 py-2 w-64 rounded-lg border ${
                darkMode 
                  ? 'bg-gray-800 border-gray-700 text-white placeholder-gray-500 focus:border-kurios-primary' 
                  : 'bg-gray-50 border-gray-200 text-gray-900 placeholder-gray-400 focus:border-kurios-primary'
              } focus:outline-none focus:ring-2 focus:ring-kurios-primary/20 transition-all`}
            />
          </div>

          {/* Quick Add */}
          <div className="relative">
            <button
              onClick={() => setShowQuickAdd(!showQuickAdd)}
              className="flex items-center gap-2 px-4 py-2 bg-kurios-primary text-white rounded-lg hover:bg-kurios-primary/90 transition-colors shadow-lg shadow-kurios-primary/30"
            >
              <Plus className="w-4 h-4" />
              <span className="font-medium">Add</span>
              <ChevronDown className="w-4 h-4" />
            </button>
            
            {showQuickAdd && (
              <>
                <div className="fixed inset-0 z-10" onClick={() => setShowQuickAdd(false)} />
                <div className={`absolute right-0 mt-2 w-48 rounded-lg shadow-lg ${
                  darkMode ? 'bg-gray-800 border border-gray-700' : 'bg-white border border-gray-200'
                } z-20 py-1`}>
                  {[
                    { label: 'New Deal', modal: 'addDeal' },
                    { label: 'New Contact', modal: 'addContact' },
                    { label: 'New Project', modal: 'addProject' },
                    { label: 'New Idea', modal: 'addIdea' },
                  ].map((item) => (
                    <button
                      key={item.modal}
                      onClick={() => {
                        openModal(item.modal);
                        setShowQuickAdd(false);
                      }}
                      className={`w-full px-4 py-2 text-left ${
                        darkMode 
                          ? 'text-gray-300 hover:bg-gray-700' 
                          : 'text-gray-700 hover:bg-gray-100'
                      } transition-colors`}
                    >
                      {item.label}
                    </button>
                  ))}
                </div>
              </>
            )}
          </div>

          {/* Dark mode toggle */}
          <button
            onClick={toggleDarkMode}
            className={`p-2 rounded-lg ${
              darkMode 
                ? 'text-gray-400 hover:text-white hover:bg-gray-800' 
                : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100'
            } transition-colors`}
          >
            {darkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
          </button>

          {/* Notifications */}
          <div className="relative">
            <button
              onClick={() => setShowNotifications(!showNotifications)}
              className={`p-2 rounded-lg relative ${
                darkMode 
                  ? 'text-gray-400 hover:text-white hover:bg-gray-800' 
                  : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100'
              } transition-colors`}
            >
              <Bell className="w-5 h-5" />
              <span className="absolute top-1 right-1 w-2 h-2 bg-kurios-secondary rounded-full" />
            </button>
            
            {showNotifications && (
              <>
                <div className="fixed inset-0 z-10" onClick={() => setShowNotifications(false)} />
                <div className={`absolute right-0 mt-2 w-80 rounded-lg shadow-lg ${
                  darkMode ? 'bg-gray-800 border border-gray-700' : 'bg-white border border-gray-200'
                } z-20`}>
                  <div className={`px-4 py-3 border-b ${darkMode ? 'border-gray-700' : 'border-gray-200'}`}>
                    <h3 className={`font-semibold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                      Notifications
                    </h3>
                  </div>
                  <div className="max-h-80 overflow-y-auto">
                    {[
                      { title: 'Hot lead!', desc: 'Joan Suh call scheduled', time: '5m ago' },
                      { title: 'Verbal commit', desc: 'Jalal Abdallah - $50k', time: '2h ago' },
                      { title: 'First closed deal! 🎉', desc: 'Jason E. - $31,750', time: '1d ago' },
                    ].map((notif, i) => (
                      <div 
                        key={i}
                        className={`px-4 py-3 ${
                          darkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-50'
                        } cursor-pointer transition-colors`}
                      >
                        <p className={`font-medium ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                          {notif.title}
                        </p>
                        <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                          {notif.desc}
                        </p>
                        <p className={`text-xs mt-1 ${darkMode ? 'text-gray-500' : 'text-gray-400'}`}>
                          {notif.time}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              </>
            )}
          </div>

          {/* User menu */}
          <div className="relative">
            <button
              onClick={() => setShowUserMenu(!showUserMenu)}
              className="flex items-center gap-2"
            >
              <div 
                className="w-9 h-9 rounded-full flex items-center justify-center text-white font-medium text-sm"
                style={{ backgroundColor: getAvatarColor(settings.profile.name) }}
              >
                {getInitials(settings.profile.name)}
              </div>
            </button>
            
            {showUserMenu && (
              <>
                <div className="fixed inset-0 z-10" onClick={() => setShowUserMenu(false)} />
                <div className={`absolute right-0 mt-2 w-56 rounded-lg shadow-lg ${
                  darkMode ? 'bg-gray-800 border border-gray-700' : 'bg-white border border-gray-200'
                } z-20`}>
                  <div className={`px-4 py-3 border-b ${darkMode ? 'border-gray-700' : 'border-gray-200'}`}>
                    <p className={`font-medium ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                      {settings.profile.name}
                    </p>
                    <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                      {settings.profile.email}
                    </p>
                  </div>
                  <div className="py-1">
                    <a 
                      href="/settings"
                      className={`block px-4 py-2 ${
                        darkMode ? 'text-gray-300 hover:bg-gray-700' : 'text-gray-700 hover:bg-gray-100'
                      } transition-colors`}
                    >
                      Settings
                    </a>
                  </div>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}
