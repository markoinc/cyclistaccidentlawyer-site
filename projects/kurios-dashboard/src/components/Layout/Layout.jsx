import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import TopBar from './TopBar';
import Toast from '../UI/Toast';
import ModalManager from '../UI/ModalManager';
import useStore from '../../stores/useStore';

export default function Layout() {
  const { sidebarCollapsed, settings } = useStore();
  const darkMode = settings.appearance.darkMode;

  return (
    <div className={`min-h-screen ${darkMode ? 'dark bg-kurios-dark' : 'bg-gray-50'}`}>
      <Sidebar />
      <TopBar />
      
      <main 
        className={`pt-16 min-h-screen transition-all duration-300 ${
          sidebarCollapsed ? 'pl-20' : 'pl-64'
        }`}
      >
        <div className="p-6">
          <Outlet />
        </div>
      </main>

      <Toast />
      <ModalManager />
    </div>
  );
}
