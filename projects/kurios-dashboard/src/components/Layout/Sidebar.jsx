import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Kanban, 
  FolderKanban, 
  Users, 
  Building2, 
  BarChart3, 
  Lightbulb, 
  Settings,
  ChevronLeft,
  ChevronRight,
  Zap
} from 'lucide-react';
import useStore from '../../stores/useStore';

const navItems = [
  { path: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { path: '/pipeline', icon: Kanban, label: 'Pipeline' },
  { path: '/projects', icon: FolderKanban, label: 'Projects' },
  { path: '/contacts', icon: Users, label: 'Contacts' },
  { path: '/clients', icon: Building2, label: 'Clients' },
  { path: '/analytics', icon: BarChart3, label: 'Analytics' },
  { path: '/ideas', icon: Lightbulb, label: 'Ideas' },
  { path: '/settings', icon: Settings, label: 'Settings' },
];

export default function Sidebar() {
  const { sidebarCollapsed, toggleSidebar, settings } = useStore();
  const darkMode = settings.appearance.darkMode;

  return (
    <aside 
      className={`fixed left-0 top-0 h-screen ${
        sidebarCollapsed ? 'w-20' : 'w-64'
      } ${
        darkMode ? 'bg-kurios-darker border-gray-800' : 'bg-white border-gray-200'
      } border-r transition-all duration-300 z-50 flex flex-col`}
    >
      {/* Logo */}
      <div className={`h-16 flex items-center ${sidebarCollapsed ? 'justify-center' : 'px-6'} border-b ${
        darkMode ? 'border-gray-800' : 'border-gray-200'
      }`}>
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-kurios-primary to-kurios-secondary flex items-center justify-center">
            <Zap className="w-6 h-6 text-white" />
          </div>
          {!sidebarCollapsed && (
            <span className={`font-bold text-xl ${darkMode ? 'text-white' : 'text-gray-900'}`}>
              Kurios
            </span>
          )}
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 py-4 overflow-y-auto">
        <ul className="space-y-1 px-3">
          {navItems.map((item) => (
            <li key={item.path}>
              <NavLink
                to={item.path}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-200 ${
                    sidebarCollapsed ? 'justify-center' : ''
                  } ${
                    isActive
                      ? 'bg-kurios-primary text-white shadow-lg shadow-kurios-primary/30'
                      : darkMode
                      ? 'text-gray-400 hover:text-white hover:bg-gray-800'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                  }`
                }
                title={sidebarCollapsed ? item.label : undefined}
              >
                <item.icon className="w-5 h-5 shrink-0" />
                {!sidebarCollapsed && (
                  <span className="font-medium">{item.label}</span>
                )}
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>

      {/* Collapse button */}
      <div className={`p-3 border-t ${darkMode ? 'border-gray-800' : 'border-gray-200'}`}>
        <button
          onClick={toggleSidebar}
          className={`w-full flex items-center justify-center gap-2 px-3 py-2 rounded-lg transition-colors ${
            darkMode 
              ? 'text-gray-400 hover:text-white hover:bg-gray-800' 
              : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
          }`}
        >
          {sidebarCollapsed ? (
            <ChevronRight className="w-5 h-5" />
          ) : (
            <>
              <ChevronLeft className="w-5 h-5" />
              <span className="font-medium">Collapse</span>
            </>
          )}
        </button>
      </div>
    </aside>
  );
}
