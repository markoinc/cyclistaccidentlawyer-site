import { Search, X } from 'lucide-react';
import useStore from '../../stores/useStore';

export default function SearchInput({ value, onChange, placeholder = 'Search...' }) {
  const { settings } = useStore();
  const darkMode = settings.appearance.darkMode;

  return (
    <div className="relative">
      <Search className={`absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 ${
        darkMode ? 'text-gray-500' : 'text-gray-400'
      }`} />
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className={`w-full pl-10 pr-10 py-2 rounded-lg border ${
          darkMode 
            ? 'bg-gray-800 border-gray-700 text-white placeholder-gray-500' 
            : 'bg-white border-gray-200 text-gray-900 placeholder-gray-400'
        } focus:outline-none focus:ring-2 focus:ring-kurios-primary/20 focus:border-kurios-primary transition-all`}
      />
      {value && (
        <button
          onClick={() => onChange('')}
          className={`absolute right-3 top-1/2 -translate-y-1/2 ${
            darkMode ? 'text-gray-500 hover:text-gray-300' : 'text-gray-400 hover:text-gray-600'
          }`}
        >
          <X className="w-4 h-4" />
        </button>
      )}
    </div>
  );
}
