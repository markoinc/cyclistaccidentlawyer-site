import { useState } from 'react';
import { Plus, Download, Search, Phone, Eye, Mail, UserCircle } from 'lucide-react';
import useStore from '../stores/useStore';
import { filterBySearch } from '../utils/helpers';

const typeConfig = {
  partner: { label: 'Partner', color: 'bg-kurios-primary/12 text-kurios-primary' },
  prospect: { label: 'Prospect', color: 'bg-amber-500/12 text-amber-400' },
  client: { label: 'Client', color: 'bg-kurios-secondary/12 text-kurios-secondary' },
};

export default function Contacts() {
  const { contacts, addToast, openModal } = useStore();
  const [filter, setFilter] = useState('all');
  const [search, setSearch] = useState('');

  const types = ['all', 'partner', 'prospect', 'client'];

  const filteredContacts = filterBySearch(
    filter === 'all' ? contacts : contacts.filter((c) => c.type === filter),
    search,
    ['name', 'company', 'email']
  );

  const handleExport = () => {
    const data = filteredContacts.map((c) => ({
      name: c.name,
      email: c.email,
      company: c.company,
      type: c.type,
      role: c.role,
    }));
    const headers = ['Name', 'Email', 'Company', 'Type', 'Role'];
    const rows = data.map((c) => Object.values(c));
    const content = [headers, ...rows].map((r) => r.join(',')).join('\n');
    const blob = new Blob([content], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'contacts-export.csv';
    a.click();
    URL.revokeObjectURL(url);
    addToast(`Exported ${filteredContacts.length} contacts`, 'success');
  };

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* Actions */}
      <div className="flex flex-wrap items-center gap-3">
        <button
          onClick={() => openModal('addContact')}
          className="flex items-center gap-2 px-4 py-2.5 bg-kurios-primary text-white text-sm font-medium rounded-lg hover:bg-kurios-primary/90 transition-all shadow-lg shadow-kurios-primary/20"
        >
          <Plus className="w-4 h-4" />
          Add Contact
        </button>
        <button
          onClick={handleExport}
          className="flex items-center gap-2 px-4 py-2.5 bg-white/[0.06] text-gray-300 text-sm font-medium rounded-lg hover:bg-white/[0.1] border border-kurios-border transition-colors"
        >
          <Download className="w-4 h-4" />
          Export
        </button>
      </div>

      {/* Toolbar */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        {/* Search */}
        <div className="relative w-full sm:w-72">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
          <input
            type="text"
            placeholder="Search contacts…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-9 pr-4 py-2.5 rounded-lg bg-white/[0.04] border border-kurios-border text-sm text-white placeholder-gray-500 focus:outline-none focus:border-kurios-primary/50 transition-all"
          />
        </div>
        {/* Filter tabs */}
        <div className="flex gap-1.5 p-1 rounded-lg bg-white/[0.04]">
          {types.map((t) => (
            <button
              key={t}
              onClick={() => setFilter(t)}
              className={`px-3 py-1.5 rounded-md text-xs font-medium transition-all ${
                filter === t
                  ? 'bg-kurios-primary text-white shadow-sm'
                  : 'text-gray-400 hover:text-white'
              }`}
            >
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {/* Contact Cards */}
      {filteredContacts.length === 0 ? (
        <div className="text-center py-16 text-gray-500">
          <UserCircle className="w-12 h-12 mx-auto mb-3 opacity-40" />
          <p className="text-sm">No contacts found</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-3 stagger-children">
          {filteredContacts.map((contact) => {
            const cfg = typeConfig[contact.type] || typeConfig.prospect;
            return (
              <div
                key={contact.id}
                className="group p-4 rounded-xl border border-kurios-border bg-kurios-card hover:border-kurios-border-hover hover:bg-kurios-card-hover transition-all duration-200 card-glow"
              >
                <div className="flex items-start gap-3">
                  {/* Avatar */}
                  <div className="w-10 h-10 rounded-full bg-gradient-to-br from-kurios-primary/30 to-kurios-accent/20 flex items-center justify-center text-sm font-semibold text-white shrink-0">
                    {contact.name?.charAt(0) || '?'}
                  </div>

                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-0.5">
                      <h3 className="font-semibold text-sm text-white truncate">
                        {contact.name}
                      </h3>
                      <span className={`shrink-0 text-[10px] font-medium px-2 py-0.5 rounded-full ${cfg.color}`}>
                        {cfg.label}
                      </span>
                    </div>
                    <p className="text-xs text-gray-500 truncate">{contact.company} {contact.role ? `• ${contact.role}` : ''}</p>
                    {contact.notes && (
                      <p className="text-[11px] text-gray-600 mt-1.5 line-clamp-2">{contact.notes}</p>
                    )}
                  </div>
                </div>

                {/* Actions */}
                <div className="flex items-center gap-2 mt-3 pt-3 border-t border-kurios-border">
                  {contact.email && (
                    <a
                      href={`mailto:${contact.email}`}
                      className="flex items-center gap-1.5 text-[11px] text-gray-500 hover:text-kurios-primary transition-colors"
                    >
                      <Mail className="w-3.5 h-3.5" />
                      {contact.email}
                    </a>
                  )}
                  <div className="ml-auto flex gap-1">
                    <button
                      onClick={() => openModal('viewDetails', contact)}
                      className="p-1.5 rounded-md text-gray-500 hover:text-white hover:bg-white/[0.06] transition-colors"
                    >
                      <Eye className="w-3.5 h-3.5" />
                    </button>
                    <button
                      onClick={() => addToast(`Calling ${contact.name}...`, 'info')}
                      className="p-1.5 rounded-md text-gray-500 hover:text-kurios-primary hover:bg-kurios-primary/10 transition-colors"
                    >
                      <Phone className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
