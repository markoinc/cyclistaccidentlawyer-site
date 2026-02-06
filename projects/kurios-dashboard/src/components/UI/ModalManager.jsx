import { useState } from 'react';
import Modal from './Modal';
import useStore from '../../stores/useStore';
import { formatCurrency, formatDate } from '../../utils/helpers';

export default function ModalManager() {
  const { activeModal, modalData, closeModal } = useStore();

  if (!activeModal) return null;

  const modalConfig = {
    addDeal: { title: 'Add New Deal', content: <AddDealForm onClose={closeModal} /> },
    addContact: { title: 'Add Contact', content: <AddContactForm onClose={closeModal} /> },
    addProject: { title: 'Add Project', content: <AddProjectForm onClose={closeModal} /> },
    addIdea: { title: 'Submit Idea', content: <AddIdeaForm onClose={closeModal} /> },
    addClient: { title: 'Add Client', content: <AddClientForm onClose={closeModal} /> },
    addCall: { title: 'Log Call', content: <LogCallForm onClose={closeModal} /> },
    viewDetails: { title: modalData?.name || modalData?.title || 'Details', content: <DetailsView data={modalData} /> },
  };

  const config = modalConfig[activeModal] || {
    title: 'Modal',
    content: <p className="text-gray-400 text-sm">Modal type: {activeModal}</p>,
  };

  return (
    <Modal title={config.title} onClose={closeModal} size="lg">
      {config.content}
    </Modal>
  );
}

// ── Form input helper ──────────────────────────────────────────
const inputClass =
  'w-full px-4 py-2.5 rounded-lg bg-white/[0.04] border border-kurios-border text-sm text-white placeholder-gray-500 focus:outline-none focus:border-kurios-primary/50 focus:ring-1 focus:ring-kurios-primary/20 transition-all';
const labelClass = 'block text-xs font-medium text-gray-400 mb-1.5';
const btnPrimary =
  'px-5 py-2.5 bg-kurios-primary text-white text-sm font-medium rounded-lg hover:bg-kurios-primary/90 transition-all';
const btnSecondary =
  'px-5 py-2.5 bg-white/[0.06] text-gray-300 text-sm rounded-lg hover:bg-white/[0.1] border border-kurios-border transition-colors';

// ── Add Deal ────────────────────────────────────────────────────
function AddDealForm({ onClose }) {
  const { addDeal, addToast } = useStore();
  const [form, setForm] = useState({ name: '', company: '', value: '', state: '', priority: 'medium', notes: '' });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!form.name || !form.value) return addToast('Name and value required', 'error');
    addDeal({ ...form, value: Number(form.value), stage: 'lead', nextAction: 'Discovery call' });
    addToast(`Deal "${form.name}" added!`, 'success');
    onClose();
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div><label className={labelClass}>Name *</label><input className={inputClass} value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} placeholder="Contact name" /></div>
        <div><label className={labelClass}>Company</label><input className={inputClass} value={form.company} onChange={(e) => setForm({ ...form, company: e.target.value })} placeholder="Firm name" /></div>
        <div><label className={labelClass}>Deal Value ($) *</label><input className={inputClass} type="number" value={form.value} onChange={(e) => setForm({ ...form, value: e.target.value })} placeholder="50000" /></div>
        <div><label className={labelClass}>State</label><input className={inputClass} value={form.state} onChange={(e) => setForm({ ...form, state: e.target.value })} placeholder="TX" maxLength={2} /></div>
        <div className="col-span-2">
          <label className={labelClass}>Priority</label>
          <div className="flex gap-2">
            {['low', 'medium', 'high'].map((p) => (
              <button key={p} type="button" onClick={() => setForm({ ...form, priority: p })}
                className={`flex-1 py-2 rounded-lg text-xs font-medium border transition-all ${form.priority === p ? 'bg-kurios-primary/15 border-kurios-primary/30 text-kurios-primary' : 'bg-white/[0.02] border-kurios-border text-gray-500 hover:text-gray-300'}`}>
                {p.charAt(0).toUpperCase() + p.slice(1)}
              </button>
            ))}
          </div>
        </div>
        <div className="col-span-2"><label className={labelClass}>Notes</label><textarea className={`${inputClass} min-h-[60px]`} value={form.notes} onChange={(e) => setForm({ ...form, notes: e.target.value })} placeholder="Add notes…" /></div>
      </div>
      <div className="flex gap-3 pt-2">
        <button type="submit" className={btnPrimary}>Add Deal</button>
        <button type="button" onClick={onClose} className={btnSecondary}>Cancel</button>
      </div>
    </form>
  );
}

// ── Add Contact ────────────────────────────────────────────────
function AddContactForm({ onClose }) {
  const { addContact, addToast } = useStore();
  const [form, setForm] = useState({ name: '', email: '', company: '', role: '', type: 'prospect', notes: '' });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!form.name) return addToast('Name is required', 'error');
    addContact(form);
    addToast(`Contact "${form.name}" added!`, 'success');
    onClose();
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div><label className={labelClass}>Name *</label><input className={inputClass} value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} /></div>
        <div><label className={labelClass}>Email</label><input className={inputClass} type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} /></div>
        <div><label className={labelClass}>Company</label><input className={inputClass} value={form.company} onChange={(e) => setForm({ ...form, company: e.target.value })} /></div>
        <div><label className={labelClass}>Role</label><input className={inputClass} value={form.role} onChange={(e) => setForm({ ...form, role: e.target.value })} /></div>
        <div className="col-span-2">
          <label className={labelClass}>Type</label>
          <div className="flex gap-2">
            {['partner', 'prospect', 'client'].map((t) => (
              <button key={t} type="button" onClick={() => setForm({ ...form, type: t })}
                className={`flex-1 py-2 rounded-lg text-xs font-medium border transition-all ${form.type === t ? 'bg-kurios-primary/15 border-kurios-primary/30 text-kurios-primary' : 'bg-white/[0.02] border-kurios-border text-gray-500'}`}>
                {t.charAt(0).toUpperCase() + t.slice(1)}
              </button>
            ))}
          </div>
        </div>
        <div className="col-span-2"><label className={labelClass}>Notes</label><textarea className={`${inputClass} min-h-[60px]`} value={form.notes} onChange={(e) => setForm({ ...form, notes: e.target.value })} /></div>
      </div>
      <div className="flex gap-3 pt-2">
        <button type="submit" className={btnPrimary}>Add Contact</button>
        <button type="button" onClick={onClose} className={btnSecondary}>Cancel</button>
      </div>
    </form>
  );
}

// ── Add Project ────────────────────────────────────────────────
function AddProjectForm({ onClose }) {
  const { addProject, addToast } = useStore();
  const [form, setForm] = useState({ name: '', description: '', client: '', status: 'in_progress', dueDate: '' });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!form.name) return addToast('Name is required', 'error');
    addProject(form);
    addToast(`Project "${form.name}" created!`, 'success');
    onClose();
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div className="col-span-2"><label className={labelClass}>Name *</label><input className={inputClass} value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} /></div>
        <div className="col-span-2"><label className={labelClass}>Description</label><textarea className={`${inputClass} min-h-[60px]`} value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} /></div>
        <div><label className={labelClass}>Client</label><input className={inputClass} value={form.client} onChange={(e) => setForm({ ...form, client: e.target.value })} /></div>
        <div><label className={labelClass}>Due Date</label><input className={inputClass} type="date" value={form.dueDate} onChange={(e) => setForm({ ...form, dueDate: e.target.value })} /></div>
      </div>
      <div className="flex gap-3 pt-2">
        <button type="submit" className={btnPrimary}>Create Project</button>
        <button type="button" onClick={onClose} className={btnSecondary}>Cancel</button>
      </div>
    </form>
  );
}

// ── Add Idea ─────────────────────────────────────────────────────
function AddIdeaForm({ onClose }) {
  const { addIdea, addToast } = useStore();
  const [form, setForm] = useState({ title: '', description: '', priority: 'medium', status: 'backlog' });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!form.title) return addToast('Title is required', 'error');
    addIdea(form);
    addToast(`Idea "${form.title}" submitted!`, 'success');
    onClose();
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div><label className={labelClass}>Title *</label><input className={inputClass} value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} /></div>
      <div><label className={labelClass}>Description</label><textarea className={`${inputClass} min-h-[80px]`} value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} /></div>
      <div>
        <label className={labelClass}>Priority</label>
        <div className="flex gap-2">
          {['low', 'medium', 'high'].map((p) => (
            <button key={p} type="button" onClick={() => setForm({ ...form, priority: p })}
              className={`flex-1 py-2 rounded-lg text-xs font-medium border transition-all ${form.priority === p ? 'bg-kurios-primary/15 border-kurios-primary/30 text-kurios-primary' : 'bg-white/[0.02] border-kurios-border text-gray-500'}`}>
              {p.charAt(0).toUpperCase() + p.slice(1)}
            </button>
          ))}
        </div>
      </div>
      <div className="flex gap-3 pt-2">
        <button type="submit" className={btnPrimary}>Submit Idea</button>
        <button type="button" onClick={onClose} className={btnSecondary}>Cancel</button>
      </div>
    </form>
  );
}

// ── Add Client ─────────────────────────────────────────────────
function AddClientForm({ onClose }) {
  const { addClient, addToast } = useStore();
  const [form, setForm] = useState({ name: '', state: '', revenue: '', conversion: '', casesPerMonth: '', industry: 'MVA', status: 'active' });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!form.name || !form.state) return addToast('Name and state required', 'error');
    addClient({ ...form, revenue: Number(form.revenue), conversion: Number(form.conversion), casesPerMonth: Number(form.casesPerMonth) });
    addToast(`Client "${form.name}" added!`, 'success');
    onClose();
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div><label className={labelClass}>Name *</label><input className={inputClass} value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} /></div>
        <div><label className={labelClass}>State *</label><input className={inputClass} value={form.state} onChange={(e) => setForm({ ...form, state: e.target.value })} placeholder="TX" maxLength={2} /></div>
        <div><label className={labelClass}>Case Value ($)</label><input className={inputClass} type="number" value={form.revenue} onChange={(e) => setForm({ ...form, revenue: e.target.value })} /></div>
        <div><label className={labelClass}>Conversion %</label><input className={inputClass} type="number" value={form.conversion} onChange={(e) => setForm({ ...form, conversion: e.target.value })} /></div>
        <div><label className={labelClass}>Cases/Month</label><input className={inputClass} type="number" value={form.casesPerMonth} onChange={(e) => setForm({ ...form, casesPerMonth: e.target.value })} /></div>
      </div>
      <div className="flex gap-3 pt-2">
        <button type="submit" className={btnPrimary}>Add Client</button>
        <button type="button" onClick={onClose} className={btnSecondary}>Cancel</button>
      </div>
    </form>
  );
}

// ── Log Call ─────────────────────────────────────────────────────
function LogCallForm({ onClose }) {
  const { logCall, addToast } = useStore();

  const handleLog = () => {
    logCall();
    addToast('Call logged! 📞', 'success');
    onClose();
  };

  return (
    <div className="space-y-4">
      <p className="text-sm text-gray-400">Log a completed sales call. This increments your daily and weekly call counts.</p>
      <div className="flex gap-3 pt-2">
        <button onClick={handleLog} className={btnPrimary}>Log Call</button>
        <button onClick={onClose} className={btnSecondary}>Cancel</button>
      </div>
    </div>
  );
}

// ── Details View ────────────────────────────────────────────────
function DetailsView({ data }) {
  if (!data) return <p className="text-gray-500 text-sm">No data</p>;

  const fields = Object.entries(data).filter(
    ([key]) => !['id', 'tasks'].includes(key) && typeof data[key] !== 'object'
  );

  return (
    <div className="space-y-3">
      {fields.map(([key, value]) => (
        <div key={key} className="flex items-start gap-4">
          <span className="text-xs font-medium text-gray-500 w-28 shrink-0 pt-0.5">
            {key.replace(/([A-Z])/g, ' $1').replace(/^./, (s) => s.toUpperCase())}
          </span>
          <span className="text-sm text-white">
            {typeof value === 'number' && key.toLowerCase().includes('value')
              ? formatCurrency(value)
              : typeof value === 'number' && key.toLowerCase().includes('margin')
              ? formatCurrency(value)
              : String(value || '—')}
          </span>
        </div>
      ))}
    </div>
  );
}
