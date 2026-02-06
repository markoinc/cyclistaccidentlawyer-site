import { useEffect } from 'react';
import { CheckCircle, XCircle, AlertCircle, Info, X } from 'lucide-react';
import useStore from '../../stores/useStore';

const icons = {
  success: CheckCircle,
  error: XCircle,
  warning: AlertCircle,
  info: Info,
};

const iconColors = {
  success: 'text-kurios-secondary',
  error: 'text-red-400',
  warning: 'text-amber-400',
  info: 'text-kurios-primary',
};

const bgColors = {
  success: 'bg-kurios-secondary/10',
  error: 'bg-red-400/10',
  warning: 'bg-amber-400/10',
  info: 'bg-kurios-primary/10',
};

export default function Toast() {
  const { toasts, removeToast } = useStore();

  return (
    <div className="fixed bottom-4 right-4 z-50 flex flex-col gap-2 max-w-sm">
      {toasts.map((toast) => (
        <ToastItem
          key={toast.id}
          toast={toast}
          onRemove={() => removeToast(toast.id)}
        />
      ))}
    </div>
  );
}

function ToastItem({ toast, onRemove }) {
  const Icon = icons[toast.type] || Info;

  useEffect(() => {
    const timer = setTimeout(onRemove, toast.duration || 4000);
    return () => clearTimeout(timer);
  }, [onRemove, toast.duration]);

  return (
    <div className="flex items-center gap-3 px-4 py-3 rounded-xl shadow-2xl shadow-black/30 animate-slideIn bg-kurios-card border border-kurios-border backdrop-blur-xl min-w-[280px]">
      <div className={`p-1.5 rounded-lg ${bgColors[toast.type]}`}>
        <Icon className={`w-4 h-4 ${iconColors[toast.type]}`} />
      </div>
      <div className="flex-1 min-w-0">
        {toast.title && (
          <p className="font-medium text-sm text-white">{toast.title}</p>
        )}
        <p className="text-sm text-gray-300">{toast.message}</p>
      </div>
      <button
        onClick={onRemove}
        className="p-1 rounded-md text-gray-600 hover:text-gray-300 transition-colors shrink-0"
      >
        <X className="w-4 h-4" />
      </button>
    </div>
  );
}
