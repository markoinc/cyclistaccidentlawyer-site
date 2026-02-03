import { useEffect } from 'react';
import { CheckCircle, XCircle, AlertCircle, Info, X } from 'lucide-react';
import useStore from '../../stores/useStore';

const icons = {
  success: CheckCircle,
  error: XCircle,
  warning: AlertCircle,
  info: Info,
};

const colors = {
  success: 'bg-green-500',
  error: 'bg-red-500',
  warning: 'bg-yellow-500',
  info: 'bg-blue-500',
};

export default function Toast() {
  const { toasts, removeToast, settings } = useStore();
  const darkMode = settings.appearance.darkMode;

  return (
    <div className="fixed bottom-4 right-4 z-50 flex flex-col gap-2">
      {toasts.map((toast) => (
        <ToastItem 
          key={toast.id} 
          toast={toast} 
          onRemove={() => removeToast(toast.id)}
          darkMode={darkMode}
        />
      ))}
    </div>
  );
}

function ToastItem({ toast, onRemove, darkMode }) {
  const Icon = icons[toast.type] || Info;

  useEffect(() => {
    const timer = setTimeout(() => {
      onRemove();
    }, toast.duration || 4000);

    return () => clearTimeout(timer);
  }, [onRemove, toast.duration]);

  return (
    <div 
      className={`flex items-center gap-3 px-4 py-3 rounded-lg shadow-lg animate-slideIn ${
        darkMode ? 'bg-gray-800 border border-gray-700' : 'bg-white border border-gray-200'
      }`}
      style={{ minWidth: '300px' }}
    >
      <div className={`p-1 rounded-full ${colors[toast.type]}`}>
        <Icon className="w-4 h-4 text-white" />
      </div>
      <div className="flex-1">
        {toast.title && (
          <p className={`font-medium ${darkMode ? 'text-white' : 'text-gray-900'}`}>
            {toast.title}
          </p>
        )}
        <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
          {toast.message}
        </p>
      </div>
      <button
        onClick={onRemove}
        className={`p-1 rounded hover:bg-gray-100 ${
          darkMode ? 'text-gray-400 hover:bg-gray-700' : 'text-gray-500'
        }`}
      >
        <X className="w-4 h-4" />
      </button>
    </div>
  );
}
