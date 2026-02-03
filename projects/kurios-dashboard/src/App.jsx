import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useEffect } from 'react';
import Layout from './components/Layout/Layout';
import Dashboard from './pages/Dashboard';
import Pipeline from './pages/Pipeline';
import Projects from './pages/Projects';
import Contacts from './pages/Contacts';
import Clients from './pages/Clients';
import Analytics from './pages/Analytics';
import Ideas from './pages/Ideas';
import Settings from './pages/Settings';
import useStore from './stores/useStore';

const queryClient = new QueryClient();

function AppContent() {
  const { settings } = useStore();
  
  // Apply dark mode class to html element
  useEffect(() => {
    if (settings.appearance.darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [settings.appearance.darkMode]);

  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Dashboard />} />
        <Route path="pipeline" element={<Pipeline />} />
        <Route path="projects" element={<Projects />} />
        <Route path="contacts" element={<Contacts />} />
        <Route path="clients" element={<Clients />} />
        <Route path="analytics" element={<Analytics />} />
        <Route path="ideas" element={<Ideas />} />
        <Route path="settings" element={<Settings />} />
      </Route>
    </Routes>
  );
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AppContent />
      </BrowserRouter>
    </QueryClientProvider>
  );
}
