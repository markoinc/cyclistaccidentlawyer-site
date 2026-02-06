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
  Zap,
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
  const { sidebarCollapsed, toggleSidebar, mobileSidebarOpen, closeMobileSidebar } = useStore();

  return (
    <aside
      className={`fixed left-0 top-0 h-screen z-50 flex flex-col transition-all duration-300 ease-out
        bg-kurios-darker border-r border-kurios-border
        ${sidebarCollapsed ? 'lg:w-20' : 'lg:w-64'}
        ${mobileSidebarOpen ? 'w-64 translate-x-0' : '-translate-x-full lg:translate-x-0'}
      `}
    >
      {/* Logo */}
      <div
        className={`h-16 flex items-center ${
          sidebarCollapsed ? 'lg:justify-center px-6 lg:px-0' : 'px-6'
        } border-b border-kurios-border`}
      >
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-kurios-primary to-kurios-accent flex items-center justify-center shadow-lg shadow-kurios-primary/20">
            <Zap className="w-5 h-5 text-white" />
          </div>
          {(!sidebarCollapsed || mobileSidebarOpen) && (
            <span className="font-bold text-lg text-white tracking-tight lg:hidden xl:inline">
              Kurios
            </span>
          )}
          {!sidebarCollapsed && (
            <span className="font-bold text-lg text-white tracking-tight hidden lg:inline">
              Kurios
            </span>
          )}
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 py-4 overflow-y-auto">
        <ul className="space-y-0.5 px-3">
          {navItems.map((item) => (
            <li key={item.path}>
              <NavLink
                to={item.path}
                end={item.path === '/'}
                onClick={() => closeMobileSidebar()}
                className={({ isActive }) =>
                  `group flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-200 ${
                    sidebarCollapsed ? 'lg:justify-center' : ''
                  } ${
                    isActive
                      ? 'bg-kurios-primary/15 text-kurios-primary border border-kurios-primary/20'
                      : 'text-gray-400 hover:text-white hover:bg-white/[0.04] border border-transparent'
                  }`
                }
                title={sidebarCollapsed ? item.label : undefined}
              >
                <item.icon className="w-[18px] h-[18px] shrink-0" />
                {(!sidebarCollapsed || mobileSidebarOpen) && (
                  <span className="text-sm font-medium lg:hidden xl:inline">{item.label}</span>
                )}
                {!sidebarCollapsed && (
                  <span className="text-sm font-medium hidden lg:inline">{item.label}</span>
                )}
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>

      {/* Collapse button - desktop only */}
      <div className="p-3 border-t border-kurios-border hidden lg:block">
        <button
          onClick={toggleSidebar}
          className="w-full flex items-center justify-center gap-2 px-3 py-2 rounded-lg text-gray-500 hover:text-gray-300 hover:bg-white/[0.04] transition-colors"
        >
          {sidebarCollapsed ? (
            <ChevronRight className="w-4 h-4" />
          ) : (
            <>
              <ChevronLeft className="w-4 h-4" />
              <span className="text-sm">Collapse</span>
            </>
          )}
        </button>
      </div>
    </aside>
  );
}
