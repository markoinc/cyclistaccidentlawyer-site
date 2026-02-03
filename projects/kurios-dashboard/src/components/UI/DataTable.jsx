import { useState } from 'react';
import { ChevronUp, ChevronDown, MoreHorizontal } from 'lucide-react';
import useStore from '../../stores/useStore';

export default function DataTable({ 
  columns, 
  data, 
  onRowClick,
  actions,
  emptyMessage = 'No data found'
}) {
  const { settings } = useStore();
  const darkMode = settings.appearance.darkMode;
  const [sortKey, setSortKey] = useState(null);
  const [sortDirection, setSortDirection] = useState('asc');
  const [activeRowMenu, setActiveRowMenu] = useState(null);

  const handleSort = (key) => {
    if (sortKey === key) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortKey(key);
      setSortDirection('asc');
    }
  };

  const sortedData = sortKey
    ? [...data].sort((a, b) => {
        const aVal = a[sortKey];
        const bVal = b[sortKey];
        if (aVal < bVal) return sortDirection === 'asc' ? -1 : 1;
        if (aVal > bVal) return sortDirection === 'asc' ? 1 : -1;
        return 0;
      })
    : data;

  if (data.length === 0) {
    return (
      <div className={`text-center py-12 ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
        {emptyMessage}
      </div>
    );
  }

  return (
    <div className={`rounded-lg border overflow-hidden ${
      darkMode ? 'border-gray-700' : 'border-gray-200'
    }`}>
      <table className="w-full">
        <thead className={darkMode ? 'bg-gray-800' : 'bg-gray-50'}>
          <tr>
            {columns.map((column) => (
              <th
                key={column.key}
                onClick={() => column.sortable && handleSort(column.key)}
                className={`px-4 py-3 text-left text-sm font-semibold ${
                  darkMode ? 'text-gray-300' : 'text-gray-700'
                } ${column.sortable ? 'cursor-pointer select-none' : ''}`}
              >
                <div className="flex items-center gap-2">
                  {column.label}
                  {column.sortable && sortKey === column.key && (
                    sortDirection === 'asc' 
                      ? <ChevronUp className="w-4 h-4" />
                      : <ChevronDown className="w-4 h-4" />
                  )}
                </div>
              </th>
            ))}
            {actions && <th className="w-10" />}
          </tr>
        </thead>
        <tbody>
          {sortedData.map((row, rowIndex) => (
            <tr 
              key={row.id || rowIndex}
              onClick={() => onRowClick && onRowClick(row)}
              className={`${
                onRowClick ? 'cursor-pointer' : ''
              } ${
                darkMode 
                  ? 'hover:bg-gray-800/50 border-b border-gray-700' 
                  : 'hover:bg-gray-50 border-b border-gray-200'
              } transition-colors`}
            >
              {columns.map((column) => (
                <td
                  key={column.key}
                  className={`px-4 py-3 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}
                >
                  {column.render ? column.render(row[column.key], row) : row[column.key]}
                </td>
              ))}
              {actions && (
                <td className="px-2 py-3 relative">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      setActiveRowMenu(activeRowMenu === row.id ? null : row.id);
                    }}
                    className={`p-1 rounded ${
                      darkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-100'
                    }`}
                  >
                    <MoreHorizontal className="w-4 h-4" />
                  </button>
                  {activeRowMenu === row.id && (
                    <>
                      <div className="fixed inset-0 z-10" onClick={() => setActiveRowMenu(null)} />
                      <div className={`absolute right-0 mt-1 w-36 rounded-lg shadow-lg z-20 py-1 ${
                        darkMode ? 'bg-gray-800 border border-gray-700' : 'bg-white border border-gray-200'
                      }`}>
                        {actions.map((action, i) => (
                          <button
                            key={i}
                            onClick={(e) => {
                              e.stopPropagation();
                              action.onClick(row);
                              setActiveRowMenu(null);
                            }}
                            className={`w-full px-3 py-2 text-left text-sm ${
                              action.danger
                                ? 'text-red-500 hover:bg-red-500/10'
                                : darkMode
                                ? 'text-gray-300 hover:bg-gray-700'
                                : 'text-gray-700 hover:bg-gray-100'
                            } transition-colors`}
                          >
                            {action.label}
                          </button>
                        ))}
                      </div>
                    </>
                  )}
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
