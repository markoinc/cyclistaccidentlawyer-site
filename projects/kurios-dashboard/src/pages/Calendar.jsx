import { useState } from 'react';
import { ChevronLeft, ChevronRight, Plus } from 'lucide-react';
import { useDashboard } from '../context/DashboardContext';
import { Button, Card, CardHeader, CardBody } from '../components/UI';

const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
const DAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

const eventColors = {
  meeting: 'bg-[#3366FF]',
  call: 'bg-[#00E676]',
  deadline: 'bg-[#ff6b6b]',
};

export function Calendar() {
  const { state, dispatch, showToast } = useDashboard();
  const [currentDate, setCurrentDate] = useState(new Date(2026, 1, 1)); // Feb 2026
  const [selectedDate, setSelectedDate] = useState(null);

  const navigate = (direction) => {
    setCurrentDate(prev => {
      const newDate = new Date(prev);
      newDate.setMonth(newDate.getMonth() + direction);
      return newDate;
    });
  };

  const goToToday = () => {
    setCurrentDate(new Date(2026, 1, 1));
    setSelectedDate(new Date(2026, 1, 2));
  };

  const getDaysInMonth = (date) => {
    const year = date.getFullYear();
    const month = date.getMonth();
    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const daysInPrevMonth = new Date(year, month, 0).getDate();

    const days = [];

    // Previous month days
    for (let i = firstDay - 1; i >= 0; i--) {
      days.push({ day: daysInPrevMonth - i, isCurrentMonth: false });
    }

    // Current month days
    for (let i = 1; i <= daysInMonth; i++) {
      const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`;
      const events = state.events.filter(e => e.date === dateStr);
      days.push({ 
        day: i, 
        isCurrentMonth: true, 
        isToday: i === 2 && month === 1 && year === 2026,
        events 
      });
    }

    // Next month days
    const remaining = 42 - days.length;
    for (let i = 1; i <= remaining; i++) {
      days.push({ day: i, isCurrentMonth: false });
    }

    return days;
  };

  const handleToggleTask = (taskId) => {
    dispatch({ type: 'TOGGLE_TASK', payload: taskId });
    const task = state.tasks.find(t => t.id === taskId);
    if (task && !task.completed) {
      showToast('Task completed! 🎉', 'success');
    }
  };

  const days = getDaysInMonth(currentDate);

  return (
    <div className="p-6 animate-fadeIn">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Calendar */}
        <div className="lg:col-span-2">
          <Card>
            <CardHeader>
              <div className="flex items-center gap-4">
                <button
                  onClick={() => navigate(-1)}
                  className="w-8 h-8 rounded-lg border border-[#444d56] flex items-center justify-center hover:bg-[#3366FF] hover:border-[#3366FF] hover:text-white transition-all"
                >
                  <ChevronLeft size={16} />
                </button>
                <span className="text-lg font-semibold min-w-[160px] text-center">
                  {MONTHS[currentDate.getMonth()]} {currentDate.getFullYear()}
                </span>
                <button
                  onClick={() => navigate(1)}
                  className="w-8 h-8 rounded-lg border border-[#444d56] flex items-center justify-center hover:bg-[#3366FF] hover:border-[#3366FF] hover:text-white transition-all"
                >
                  <ChevronRight size={16} />
                </button>
              </div>
              <div className="flex gap-2">
                <Button size="sm" variant="ghost" onClick={goToToday}>Today</Button>
                <Button size="sm" onClick={() => dispatch({ type: 'OPEN_MODAL', payload: { type: 'addEvent' } })}>
                  <Plus size={14} /> Add Event
                </Button>
              </div>
            </CardHeader>
            <CardBody>
              <div className="grid grid-cols-7 gap-1">
                {/* Day headers */}
                {DAYS.map(day => (
                  <div key={day} className="text-center py-2 text-xs font-semibold text-[#6e7681] uppercase">
                    {day}
                  </div>
                ))}

                {/* Days */}
                {days.map((day, i) => (
                  <button
                    key={i}
                    onClick={() => day.isCurrentMonth && setSelectedDate(new Date(currentDate.getFullYear(), currentDate.getMonth(), day.day))}
                    className={`
                      aspect-square p-2 rounded-lg flex flex-col items-center justify-start
                      transition-all hover:bg-[#353d47]
                      ${!day.isCurrentMonth ? 'opacity-30' : ''}
                      ${day.isToday ? 'bg-[#3366FF]' : ''}
                      ${selectedDate?.getDate() === day.day && day.isCurrentMonth && !day.isToday ? 'bg-[#00E676] text-[#14171A]' : ''}
                    `}
                  >
                    <span className="text-sm font-medium">{day.day}</span>
                    {day.events && day.events.length > 0 && (
                      <div className="flex gap-1 mt-1">
                        {day.events.slice(0, 3).map((event, j) => (
                          <div key={j} className={`w-1.5 h-1.5 rounded-full ${eventColors[event.type]}`} />
                        ))}
                      </div>
                    )}
                  </button>
                ))}
              </div>
            </CardBody>
          </Card>
        </div>

        {/* Tasks */}
        <div>
          <Card>
            <CardHeader actions={
              <Button size="sm" variant="ghost" onClick={() => dispatch({ type: 'OPEN_MODAL', payload: { type: 'addTask' } })}>
                <Plus size={14} />
              </Button>
            }>
              📋 Tasks
            </CardHeader>
            <CardBody noPadding>
              <div className="divide-y divide-[#2d333b]">
                {state.tasks.map(task => (
                  <div key={task.id} className={`flex items-start gap-3 p-4 hover:bg-[#353d47] transition-colors ${task.completed ? 'opacity-50' : ''}`}>
                    <button
                      onClick={() => handleToggleTask(task.id)}
                      className={`
                        w-5 h-5 rounded-full border-2 flex-shrink-0 mt-0.5 flex items-center justify-center transition-all
                        ${task.completed 
                          ? 'bg-[#00E676] border-[#00E676] text-[#14171A]' 
                          : 'border-[#444d56] hover:border-[#00E676]'}
                      `}
                    >
                      {task.completed && '✓'}
                    </button>
                    <div className="flex-1 min-w-0">
                      <div className={`text-sm font-medium mb-1 ${task.completed ? 'line-through text-[#6e7681]' : ''}`}>
                        {task.title}
                      </div>
                      <div className="flex items-center gap-3 text-xs text-[#6e7681]">
                        <span className={`px-1.5 py-0.5 rounded text-[10px] font-semibold ${
                          task.priority === 'p0' ? 'bg-[#ff6b6b]/15 text-[#ff6b6b]' : 'bg-[#ffb347]/15 text-[#ffb347]'
                        }`}>
                          {task.label}
                        </span>
                        <span>{task.value}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardBody>
          </Card>
        </div>
      </div>
    </div>
  );
}
