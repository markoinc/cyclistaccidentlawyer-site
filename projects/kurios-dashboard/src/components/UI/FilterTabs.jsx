import useStore from '../../stores/useStore';

export default function FilterTabs({ tabs, activeTab, onChange }) {
  const { settings } = useStore();
  const darkMode = settings.appearance.darkMode;

  return (
    <div className={`inline-flex p-1 rounded-lg ${
      darkMode ? 'bg-gray-800' : 'bg-gray-100'
    }`}>
      {tabs.map((tab) => (
        <button
          key={tab.value}
          onClick={() => onChange(tab.value)}
          className={`px-4 py-2 rounded-md text-sm font-medium transition-all ${
            activeTab === tab.value
              ? 'bg-kurios-primary text-white shadow'
              : darkMode
              ? 'text-gray-400 hover:text-white'
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          {tab.label}
          {tab.count !== undefined && (
            <span className={`ml-2 px-1.5 py-0.5 text-xs rounded-full ${
              activeTab === tab.value
                ? 'bg-white/20'
                : darkMode
                ? 'bg-gray-700'
                : 'bg-gray-200'
            }`}>
              {tab.count}
            </span>
          )}
        </button>
      ))}
    </div>
  );
}
