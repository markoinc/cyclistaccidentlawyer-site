import { createContext, useContext, useReducer, useCallback } from 'react';
import useStore from '../stores/useStore';

// Initial state
const initialState = {
  prospects: [],
  projects: [],
  contacts: [],
  clients: [],
  ideas: [],
  automations: [],
  events: [],
  loading: false,
  error: null,
};

// Reducer
function dashboardReducer(state, action) {
  switch (action.type) {
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    case 'SET_ERROR':
      return { ...state, error: action.payload };
    case 'SET_PROSPECTS':
      return { ...state, prospects: action.payload };
    case 'ADD_PROSPECT':
      return { ...state, prospects: [...state.prospects, action.payload] };
    case 'UPDATE_PROSPECT':
      return {
        ...state,
        prospects: state.prospects.map(p =>
          p.id === action.payload.id ? { ...p, ...action.payload } : p
        ),
      };
    case 'DELETE_PROSPECT':
      return {
        ...state,
        prospects: state.prospects.filter(p => p.id !== action.payload),
      };
    case 'SET_PROJECTS':
      return { ...state, projects: action.payload };
    case 'ADD_PROJECT':
      return { ...state, projects: [...state.projects, action.payload] };
    case 'UPDATE_PROJECT':
      return {
        ...state,
        projects: state.projects.map(p =>
          p.id === action.payload.id ? { ...p, ...action.payload } : p
        ),
      };
    case 'SET_CONTACTS':
      return { ...state, contacts: action.payload };
    case 'ADD_CONTACT':
      return { ...state, contacts: [...state.contacts, action.payload] };
    case 'SET_CLIENTS':
      return { ...state, clients: action.payload };
    case 'SET_IDEAS':
      return { ...state, ideas: action.payload };
    case 'ADD_IDEA':
      return { ...state, ideas: [...state.ideas, action.payload] };
    case 'SET_AUTOMATIONS':
      return { ...state, automations: action.payload };
    case 'SET_EVENTS':
      return { ...state, events: action.payload };
    default:
      return state;
  }
}

// Context
const DashboardContext = createContext(null);

// Provider
export function DashboardProvider({ children }) {
  const [state, dispatch] = useReducer(dashboardReducer, initialState);
  const { addToast } = useStore();

  const showToast = useCallback((message, type = 'success') => {
    addToast(message, type);
  }, [addToast]);

  return (
    <DashboardContext.Provider value={{ state, dispatch, showToast }}>
      {children}
    </DashboardContext.Provider>
  );
}

// Hook
export function useDashboard() {
  const context = useContext(DashboardContext);
  if (!context) {
    throw new Error('useDashboard must be used within a DashboardProvider');
  }
  return context;
}

// Stats hook
export function useStats() {
  const { state } = useDashboard();
  
  return {
    totalProspects: state.prospects.length,
    totalProjects: state.projects.length,
    totalContacts: state.contacts.length,
    totalClients: state.clients.length,
    pipelineValue: state.prospects.reduce((sum, p) => sum + (p.value || 0), 0),
    activeProjects: state.projects.filter(p => p.status === 'active').length,
  };
}

export default DashboardContext;
