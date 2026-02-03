import { useState } from 'react';
import { Plus, Download, Search, Phone, Eye } from 'lucide-react';
import { useDashboard } from '../context/DashboardContext';
import { Button, Badge } from '../components/UI';

const typeConfig = {
  partners: { label: 'Partner', color: 'bg-[#3366FF]/15 text-[#3366FF]' },
  vendors: { label: 'Key Vendor', color: 'bg-[#00E676]/15 text-[#00E676]' },
  clients: { label: 'Client', color: 'bg-[#a855f7]/15 text-[#a855f7]' },
};

export function Contacts() {
  const { state, dispatch, showToast } = useDashboard();
  const [filter, setFilter] = useState('all');
  const [search, setSearch] = useState('');
  const [selectedIds, setSelectedIds] = useState([]);

  const filteredContacts = state.contacts.filter(contact => {
    const matchesFilter = filter === 'all' || contact.type === filter;
    const matchesSearch = search === '' || 
      contact.name.toLowerCase().includes(search.toLowerCase()) ||
      contact.company.toLowerCase().includes(search.toLowerCase()) ||
      contact.email.toLowerCase().includes(search.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  const toggleSelect = (id) => {
    setSelectedIds(prev => 
      prev.includes(id) ? prev.filter(i => i !== id) : [...prev, id]
    );
  };

  const handleExport = () => {
    const data = filteredContacts.map(c => ({
      name: c.name,
      email: c.email,
      company: c.company,
      type: c.type,
      tags: c.tags.join(', '),
    }));
    const headers = ['Name', 'Email', 'Company', 'Type', 'Tags'];
    const rows = data.map(c => [c.name, c.email, c.company, c.type, c.tags]);
    const content = [headers, ...rows].map(r => r.join(',')).join('\n');
    const blob = new Blob([content], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'contacts-export.csv';
    a.click();
    URL.revokeObjectURL(url);
    showToast(`Exported ${filteredContacts.length} contacts`, 'success');
  };

  return (
    <div className="p-6 animate-fadeIn">
      {/* Actions */}
      <div className="flex flex-wrap gap-3 mb-6">
        <Button onClick={() => dispatch({ type: 'OPEN_MODAL', payload: { type: 'addContact' } })}>
          <Plus size={16} /> Add Contact
        </Button>
        <Button variant="secondary" onClick={handleExport}>
          <Download size={16} /> Export
        </Button>
      </div>

      {/* Table */}
      <div className="bg-[#242930] border border-[#2d333b] rounded-xl overflow-hidden">
        {/* Toolbar */}
        <div className="p-4 border-b border-[#2d333b] flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-2 bg-[#21262c] border border-[#444d56] rounded-lg px-4 py-2 min-w-[300px] focus-within:border-[#3366FF]">
            <Search size={16} className="text-[#6e7681]" />
            <input
              type="text"
              placeholder="Search contacts..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="flex-1 bg-transparent text-sm text-[#f0f6fc] placeholder-[#6e7681] outline-none"
            />
          </div>
          <div className="flex gap-2">
            {['all', 'partners', 'vendors', 'clients'].map(f => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className={`
                  px-3 py-1.5 rounded-full text-xs font-medium border transition-all
                  ${filter === f 
                    ? 'bg-[#3366FF] border-[#3366FF] text-white' 
                    : 'bg-transparent border-[#444d56] text-[#8b949e] hover:text-white hover:border-[#3366FF]'}
                `}
              >
                {f === 'all' ? 'All' : f.charAt(0).toUpperCase() + f.slice(1)}
              </button>
            ))}
          </div>
        </div>

        {/* Table */}
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="bg-[#21262c] text-[11px] font-semibold text-[#6e7681] uppercase tracking-wider">
                <th className="w-12 px-4 py-3"></th>
                <th className="text-left px-5 py-3">Contact</th>
                <th className="text-left px-5 py-3">Company</th>
                <th className="text-left px-5 py-3">Type</th>
                <th className="text-left px-5 py-3">Tags</th>
                <th className="text-left px-5 py-3">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#2d333b]">
              {filteredContacts.map(contact => (
                <tr key={contact.id} className="hover:bg-[#353d47] transition-colors">
                  <td className="px-4 py-3">
                    <button
                      onClick={() => toggleSelect(contact.id)}
                      className={`
                        w-5 h-5 rounded border-2 flex items-center justify-center transition-all
                        ${selectedIds.includes(contact.id) 
                          ? 'bg-[#3366FF] border-[#3366FF] text-white' 
                          : 'border-[#444d56] hover:border-[#3366FF]'}
                      `}
                    >
                      {selectedIds.includes(contact.id) && '✓'}
                    </button>
                  </td>
                  <td className="px-5 py-3">
                    <div className="flex items-center gap-3">
                      <div className="w-9 h-9 rounded-full gradient-brand flex items-center justify-center text-sm font-semibold text-white">
                        {contact.avatar}
                      </div>
                      <div>
                        <div className="font-semibold">{contact.name}</div>
                        <div className="text-xs text-[#6e7681]">{contact.email}</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-5 py-3 text-sm">{contact.company}</td>
                  <td className="px-5 py-3">
                    <span className={`px-2.5 py-1 rounded text-xs font-medium ${typeConfig[contact.type]?.color}`}>
                      {typeConfig[contact.type]?.label}
                    </span>
                  </td>
                  <td className="px-5 py-3">
                    <div className="flex gap-1">
                      {contact.tags.map(tag => (
                        <span key={tag} className="px-2 py-0.5 bg-[#353d47] rounded text-xs text-[#8b949e]">
                          {tag}
                        </span>
                      ))}
                    </div>
                  </td>
                  <td className="px-5 py-3">
                    <div className="flex gap-2">
                      <Button
                        size="sm"
                        variant="ghost"
                        onClick={() => dispatch({ type: 'OPEN_MODAL', payload: { type: 'viewContact', data: contact } })}
                      >
                        <Eye size={14} />
                      </Button>
                      <Button
                        size="sm"
                        variant={contact.type === 'vendors' ? 'primary' : 'ghost'}
                        onClick={() => showToast(`Calling ${contact.name}...`, 'info')}
                      >
                        <Phone size={14} />
                      </Button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {filteredContacts.length === 0 && (
          <div className="text-center py-12 text-[#6e7681]">
            No contacts found matching your criteria
          </div>
        )}
      </div>
    </div>
  );
}

export default Contacts;
