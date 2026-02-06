import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import TopBar from './TopBar';
import Toast from '../UI/Toast';
import ModalManager from '../UI/ModalManager';
import useStore from '../../stores/useStore';

export default function Layout() {
  const { sidebarCollapsed, mobileSidebarOpen, closeMobileSidebar } = useStore();

  return (
    <div className="min-h-screen bg-kurios-dark noise-bg">
      <Sidebar />
      <TopBar />

      {/* Mobile sidebar overlay */}
      {mobileSidebarOpen && (
        <div
          className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40 lg:hidden"
          onClick={closeMobileSidebar}
        />
      )}

      <main
        className={`pt-16 min-h-screen transition-all duration-300 ease-out ${
          sidebarCollapsed ? 'lg:pl-20' : 'lg:pl-64'
        } pl-0`}
      >
        <div className="p-4 md:p-6 lg:p-8 max-w-[1600px] mx-auto relative z-1">
          <Outlet />
        </div>
      </main>

      <Toast />
      <ModalManager />
    </div>
  );
}
