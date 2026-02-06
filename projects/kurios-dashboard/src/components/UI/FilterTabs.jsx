export default function FilterTabs({ tabs, activeTab, onChange }) {
  return (
    <div className="inline-flex p-1 rounded-lg bg-white/[0.04] border border-kurios-border">
      {tabs.map((tab) => (
        <button
          key={tab.value}
          onClick={() => onChange(tab.value)}
          className={`px-3.5 py-2 rounded-md text-sm font-medium transition-all ${
            activeTab === tab.value
              ? 'bg-kurios-primary text-white shadow-sm shadow-kurios-primary/20'
              : 'text-gray-400 hover:text-white'
          }`}
        >
          {tab.label}
          {tab.count !== undefined && (
            <span
              className={`ml-1.5 px-1.5 py-0.5 text-[10px] rounded-full ${
                activeTab === tab.value
                  ? 'bg-white/20'
                  : 'bg-white/[0.06]'
              }`}
            >
              {tab.count}
            </span>
          )}
        </button>
      ))}
    </div>
  );
}
