import { useState } from 'react';
import { useLocation } from 'react-router-dom';
import {
  Search,
  Bell,
  Sun,
  Moon,
  Plus,
  ChevronDown,
  Menu,
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
    sidebarCollapsed,
    openMobileSidebar,
  } = useStore();

  const darkMode = settings.appearance.darkMode;
  const [showNotifications, setShowNotifications] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [showQuickAdd, setShowQuickAdd] = useState(false);

  const pageTitle = pageTitles[location.pathname] || 'Dashboard';

  return (
    <header
      className={`fixed top-0 right-0 h-16 ${
        sidebarCollapsed ? 'lg:left-20' : 'lg:left-64'
      } left-0 bg-kurios-darker/80 border-b border-kurios-border backdrop-blur-xl z-40 transition-all duration-300`}
    >
      <div className="h-full px-4 md:px-6 flex items-center justify-between">
        {/* Left: hamburger + page title */}
        <div className="flex items-center gap-3">
          <button
            onClick={openMobileSidebar}
            className="lg:hidden p-2 -ml-2 rounded-lg text-gray-400 hover:text-white hover:bg-white/[0.06] transition-colors"
          >
            <Menu className="w-5 h-5" />
          </button>
          <h1 className="text-lg md:text-xl font-semibold text-white tracking-tight">
            {pageTitle}
          </h1>
        </div>

        {/* Right: actions */}
        <div className="flex items-center gap-2 md:gap-3">
          {/* Search - hidden on small screens */}
          <div className="relative hidden md:block">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
            <input
              type="text"
              placeholder="Search…"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-9 pr-4 py-2 w-56 lg:w-64 rounded-lg bg-white/[0.04] border border-kurios-border text-sm text-white placeholder-gray-500 focus:outline-none focus:border-kurios-primary/50 focus:bg-white/[0.06] transition-all"
            />
          </div>

          {/* Quick Add */}
          <div className="relative">
            <button
              onClick={() => setShowQuickAdd(!showQuickAdd)}
              className="flex items-center gap-1.5 px-3 py-2 bg-kurios-primary text-white text-sm font-medium rounded-lg hover:bg-kurios-primary/90 transition-all shadow-lg shadow-kurios-primary/20"
            >
              <Plus className="w-4 h-4" />
              <span className="hidden sm:inline">Add</span>
              <ChevronDown className="w-3 h-3 opacity-60" />
            </button>

            {showQuickAdd && (
              <>
                <div className="fixed inset-0 z-10" onClick={() => setShowQuickAdd(false)} />
                <div className="absolute right-0 mt-2 w-48 rounded-xl shadow-2xl bg-kurios-card border border-kurios-border z-20 py-1.5 animate-fadeIn">
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
                      className="w-full px-4 py-2.5 text-left text-sm text-gray-300 hover:text-white hover:bg-white/[0.06] transition-colors"
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
            className="p-2 rounded-lg text-gray-400 hover:text-white hover:bg-white/[0.06] transition-colors"
          >
            {darkMode ? <Sun className="w-[18px] h-[18px]" /> : <Moon className="w-[18px] h-[18px]" />}
          </button>

          {/* Notifications */}
          <div className="relative">
            <button
              onClick={() => setShowNotifications(!showNotifications)}
              className="p-2 rounded-lg relative text-gray-400 hover:text-white hover:bg-white/[0.06] transition-colors"
            >
              <Bell className="w-[18px] h-[18px]" />
              <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-kurios-secondary rounded-full ring-2 ring-kurios-darker" />
            </button>

            {showNotifications && (
              <>
                <div className="fixed inset-0 z-10" onClick={() => setShowNotifications(false)} />
                <div className="absolute right-0 mt-2 w-80 rounded-xl shadow-2xl bg-kurios-card border border-kurios-border z-20 animate-fadeIn">
                  <div className="px-4 py-3 border-b border-kurios-border">
                    <h3 className="font-semibold text-sm text-white">Notifications</h3>
                  </div>
                  <div className="max-h-80 overflow-y-auto">
                    {[
                      { title: 'Hot lead!', desc: 'Joan Suh call scheduled', time: '5m ago' },
                      { title: 'Verbal commit', desc: 'Jalal Abdallah — $50k', time: '2h ago' },
                      { title: 'First closed deal! 🎉', desc: 'Jason E. — $31,750', time: '1d ago' },
                    ].map((notif, i) => (
                      <div
                        key={i}
                        className="px-4 py-3 hover:bg-white/[0.04] cursor-pointer transition-colors"
                      >
                        <p className="font-medium text-sm text-white">{notif.title}</p>
                        <p className="text-xs text-gray-400 mt-0.5">{notif.desc}</p>
                        <p className="text-[11px] mt-1 text-gray-600">{notif.time}</p>
                      </div>
                    ))}
                  </div>
                </div>
              </>
            )}
          </div>

          {/* User avatar */}
          <div className="relative">
            <button
              onClick={() => setShowUserMenu(!showUserMenu)}
              className="flex items-center"
            >
              <div
                className="w-8 h-8 rounded-full flex items-center justify-center text-white font-medium text-xs ring-2 ring-white/10"
                style={{ backgroundColor: getAvatarColor(settings.profile.name) }}
              >
                {getInitials(settings.profile.name)}
              </div>
            </button>

            {showUserMenu && (
              <>
                <div className="fixed inset-0 z-10" onClick={() => setShowUserMenu(false)} />
                <div className="absolute right-0 mt-2 w-56 rounded-xl shadow-2xl bg-kurios-card border border-kurios-border z-20 animate-fadeIn">
                  <div className="px-4 py-3 border-b border-kurios-border">
                    <p className="font-medium text-sm text-white">{settings.profile.name}</p>
                    <p className="text-xs text-gray-500">{settings.profile.email}</p>
                  </div>
                  <div className="py-1.5">
                    <a
                      href="/settings"
                      className="block px-4 py-2.5 text-sm text-gray-300 hover:text-white hover:bg-white/[0.06] transition-colors"
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
