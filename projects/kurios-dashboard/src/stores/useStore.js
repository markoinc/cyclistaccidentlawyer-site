import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { 
  initialDeals, 
  initialClients, 
  initialContacts, 
  initialProjects, 
  initialIdeas,
  settings as initialSettings,
  callData as initialCallData
} from '../data/sampleData';

const useStore = create(
  persist(
    (set, get) => ({
      // Deals / Pipeline
      deals: initialDeals,
      addDeal: (deal) => set((state) => ({ 
        deals: [...state.deals, { 
          ...deal, 
          id: `d${Date.now()}`, 
          createdAt: new Date().toISOString().split('T')[0],
          kuriosMargin: Math.round(deal.value * 0.3),
          probability: deal.probability || 30,
          priority: deal.priority || 'medium',
        }] 
      })),
      updateDeal: (id, updates) => set((state) => ({
        deals: state.deals.map(d => d.id === id ? { 
          ...d, 
          ...updates,
          kuriosMargin: updates.value ? Math.round(updates.value * 0.3) : d.kuriosMargin
        } : d)
      })),
      deleteDeal: (id) => set((state) => ({
        deals: state.deals.filter(d => d.id !== id)
      })),
      moveDeal: (dealId, newStage) => set((state) => ({
        deals: state.deals.map(d => {
          if (d.id !== dealId) return d;
          // Update probability based on stage
          const probabilities = { lead: 25, qualified: 50, proposal: 65, negotiation: 85, closed: 100 };
          return { 
            ...d, 
            stage: newStage,
            probability: probabilities[newStage] || d.probability
          };
        })
      })),

      // Call tracking
      callData: initialCallData,
      logCall: () => set((state) => ({
        callData: {
          ...state.callData,
          today: state.callData.today + 1,
          thisWeek: state.callData.thisWeek + 1,
        }
      })),
      updateCallData: (updates) => set((state) => ({
        callData: { ...state.callData, ...updates }
      })),

      // Clients
      clients: initialClients,
      addClient: (client) => set((state) => ({
        clients: [...state.clients, { ...client, id: `c${Date.now()}` }]
      })),
      updateClient: (id, updates) => set((state) => ({
        clients: state.clients.map(c => c.id === id ? { ...c, ...updates } : c)
      })),
      deleteClient: (id) => set((state) => ({
        clients: state.clients.filter(c => c.id !== id)
      })),

      // Contacts
      contacts: initialContacts,
      addContact: (contact) => set((state) => ({
        contacts: [...state.contacts, { ...contact, id: `ct${Date.now()}` }]
      })),
      updateContact: (id, updates) => set((state) => ({
        contacts: state.contacts.map(c => c.id === id ? { ...c, ...updates } : c)
      })),
      deleteContact: (id) => set((state) => ({
        contacts: state.contacts.filter(c => c.id !== id)
      })),

      // Projects
      projects: initialProjects,
      addProject: (project) => set((state) => ({
        projects: [...state.projects, { ...project, id: `p${Date.now()}`, tasks: [], progress: 0 }]
      })),
      updateProject: (id, updates) => set((state) => ({
        projects: state.projects.map(p => p.id === id ? { ...p, ...updates } : p)
      })),
      deleteProject: (id) => set((state) => ({
        projects: state.projects.filter(p => p.id !== id)
      })),
      toggleTask: (projectId, taskId) => set((state) => ({
        projects: state.projects.map(p => {
          if (p.id !== projectId) return p;
          const tasks = p.tasks.map(t => t.id === taskId ? { ...t, completed: !t.completed } : t);
          const progress = Math.round((tasks.filter(t => t.completed).length / tasks.length) * 100);
          return { ...p, tasks, progress };
        })
      })),
      addTask: (projectId, taskName) => set((state) => ({
        projects: state.projects.map(p => {
          if (p.id !== projectId) return p;
          const newTask = { id: `t${Date.now()}`, name: taskName, completed: false };
          const tasks = [...p.tasks, newTask];
          const progress = Math.round((tasks.filter(t => t.completed).length / tasks.length) * 100);
          return { ...p, tasks, progress };
        })
      })),

      // Ideas
      ideas: initialIdeas,
      addIdea: (idea) => set((state) => ({
        ideas: [...state.ideas, { ...idea, id: `i${Date.now()}`, votes: 0, createdAt: new Date().toISOString().split('T')[0] }]
      })),
      updateIdea: (id, updates) => set((state) => ({
        ideas: state.ideas.map(i => i.id === id ? { ...i, ...updates } : i)
      })),
      deleteIdea: (id) => set((state) => ({
        ideas: state.ideas.filter(i => i.id !== id)
      })),
      voteIdea: (id) => set((state) => ({
        ideas: state.ideas.map(i => i.id === id ? { ...i, votes: i.votes + 1 } : i)
      })),

      // Settings - Dark mode default
      settings: initialSettings,
      updateSettings: (category, updates) => set((state) => ({
        settings: {
          ...state.settings,
          [category]: { ...state.settings[category], ...updates }
        }
      })),
      toggleDarkMode: () => set((state) => ({
        settings: {
          ...state.settings,
          appearance: { ...state.settings.appearance, darkMode: !state.settings.appearance.darkMode }
        }
      })),

      // UI State
      sidebarCollapsed: false,
      toggleSidebar: () => set((state) => ({ sidebarCollapsed: !state.sidebarCollapsed })),
      
      // Toast notifications
      toasts: [],
      addToast: (toast) => set((state) => ({
        toasts: [...state.toasts, { ...toast, id: Date.now() }]
      })),
      removeToast: (id) => set((state) => ({
        toasts: state.toasts.filter(t => t.id !== id)
      })),

      // Search
      searchQuery: '',
      setSearchQuery: (query) => set({ searchQuery: query }),

      // Modals
      activeModal: null,
      modalData: null,
      openModal: (modalType, data = null) => set({ activeModal: modalType, modalData: data }),
      closeModal: () => set({ activeModal: null, modalData: null }),

      // Reset to initial data
      resetData: () => set({
        deals: initialDeals,
        clients: initialClients,
        contacts: initialContacts,
        projects: initialProjects,
        ideas: initialIdeas,
        settings: initialSettings,
        callData: initialCallData,
      }),
    }),
    {
      name: 'kurios-dashboard-storage',
      partialize: (state) => ({
        deals: state.deals,
        clients: state.clients,
        contacts: state.contacts,
        projects: state.projects,
        ideas: state.ideas,
        settings: state.settings,
        callData: state.callData,
      }),
    }
  )
);

export default useStore;
