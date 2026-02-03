import { TrendingUp, TrendingDown } from 'lucide-react';
import useStore from '../../stores/useStore';

export default function KPICard({ title, value, change, changeLabel, icon: Icon, color = 'primary' }) {
  const { settings } = useStore();
  const darkMode = settings.appearance.darkMode;

  const isPositive = change >= 0;

  const colorStyles = {
    primary: 'from-kurios-primary/10 to-kurios-primary/5 border-kurios-primary/20',
    secondary: 'from-kurios-secondary/10 to-kurios-secondary/5 border-kurios-secondary/20',
    purple: 'from-purple-500/10 to-purple-500/5 border-purple-500/20',
    orange: 'from-orange-500/10 to-orange-500/5 border-orange-500/20',
  };

  const iconBgColors = {
    primary: 'bg-kurios-primary',
    secondary: 'bg-kurios-secondary',
    purple: 'bg-purple-500',
    orange: 'bg-orange-500',
  };

  return (
    <div 
      className={`p-6 rounded-xl border bg-gradient-to-br ${colorStyles[color]} ${
        darkMode ? 'border-opacity-50' : ''
      }`}
    >
      <div className="flex items-start justify-between">
        <div>
          <p className={`text-sm font-medium ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
            {title}
          </p>
          <p className={`text-3xl font-bold mt-2 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
            {value}
          </p>
          {change !== undefined && (
            <div className="flex items-center gap-1 mt-2">
              {isPositive ? (
                <TrendingUp className="w-4 h-4 text-kurios-secondary" />
              ) : (
                <TrendingDown className="w-4 h-4 text-red-500" />
              )}
              <span className={`text-sm font-medium ${isPositive ? 'text-kurios-secondary' : 'text-red-500'}`}>
                {isPositive ? '+' : ''}{change}%
              </span>
              {changeLabel && (
                <span className={`text-sm ${darkMode ? 'text-gray-500' : 'text-gray-400'}`}>
                  {changeLabel}
                </span>
              )}
            </div>
          )}
        </div>
        {Icon && (
          <div className={`p-3 rounded-xl ${iconBgColors[color]}`}>
            <Icon className="w-6 h-6 text-white" />
          </div>
        )}
      </div>
    </div>
  );
}
