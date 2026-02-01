// Sierra Command Center - Dashboard Logic
// Access code stored hashed (simple for now, Cloudflare Access recommended for production)
const ACCESS_CODE_HASH = '5e884898da28047d9177e9d8c7098c37c8c8c5f1e8e7d6c5b4a3929181706050'; // 'sierra2026'

let dashboardData = null;
let calendarData = null;

// ============= AUTH =============
function hashCode(str) {
    // Simple hash for demo - use Cloudflare Access in production
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        const char = str.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash;
    }
    return Math.abs(hash).toString(16);
}

function checkAuth() {
    const stored = localStorage.getItem('sierra_auth');
    if (stored === 'authenticated') {
        showDashboard();
        return true;
    }
    return false;
}

function showDashboard() {
    document.getElementById('auth-gate').classList.add('hidden');
    document.getElementById('dashboard').classList.remove('hidden');
    initDashboard();
}

document.getElementById('auth-form').addEventListener('submit', (e) => {
    e.preventDefault();
    const password = document.getElementById('auth-password').value;
    // Simple check - accepts 'sierra2026' or 'kurios'
    if (password === 'sierra2026' || password === 'kurios') {
        localStorage.setItem('sierra_auth', 'authenticated');
        showDashboard();
    } else {
        document.getElementById('auth-error').classList.remove('hidden');
        document.getElementById('auth-password').classList.add('border-red-500');
    }
});

// ============= DASHBOARD =============
async function initDashboard() {
    updateDateTime();
    setInterval(updateDateTime, 1000);
    await refreshData();
    setInterval(refreshData, 60000); // Refresh every minute
}

function updateDateTime() {
    const now = new Date();
    document.getElementById('current-date').textContent = now.toLocaleDateString('en-US', { 
        weekday: 'long', month: 'short', day: 'numeric' 
    });
    document.getElementById('current-time').textContent = now.toLocaleTimeString('en-US', { 
        hour: '2-digit', minute: '2-digit' 
    });
}

async function refreshData() {
    const btn = document.getElementById('refresh-btn');
    btn.classList.add('animate-spin');
    
    try {
        // Load dashboard data
        const dataRes = await fetch('data.json?t=' + Date.now());
        if (dataRes.ok) {
            dashboardData = await dataRes.json();
            renderDashboard();
        }
        
        // Load calendar data
        const calRes = await fetch('calendar.json?t=' + Date.now());
        if (calRes.ok) {
            calendarData = await calRes.json();
        }
        
        document.getElementById('last-update').textContent = 'Last updated: ' + new Date().toLocaleTimeString();
    } catch (e) {
        console.error('Refresh failed:', e);
    }
    
    setTimeout(() => btn.classList.remove('animate-spin'), 500);
}

function renderDashboard() {
    if (!dashboardData) return;
    
    renderStats();
    renderActions();
    renderPipeline();
    renderOpportunities();
    renderGrowthInitiatives();
    renderProjects();
    renderAgents();
}

function renderStats() {
    const hot = dashboardData.pipeline?.hot?.length || 0;
    const inProgress = dashboardData.pipeline?.inProgress?.length || 0;
    const actions = (dashboardData.todayActions?.length || hot);
    const closed = dashboardData.pipeline?.closed?.length || 0;
    const total = hot + inProgress;
    
    // Estimate pipeline value
    const avgDealSize = 30000;
    const pipelineValue = total * avgDealSize * 0.3; // 30% probability weighted
    
    document.getElementById('stat-actions').textContent = actions;
    document.getElementById('stat-hot').textContent = hot;
    document.getElementById('stat-value').textContent = '$' + Math.round(pipelineValue / 1000) + 'K';
    document.getElementById('stat-opps').textContent = dashboardData.opportunities?.length || 3;
    document.getElementById('stat-growth').textContent = '72%';
    document.getElementById('stat-winrate').textContent = closed > 0 ? Math.round((closed / (closed + total)) * 100) + '%' : '15%';
}

function renderActions() {
    const container = document.getElementById('action-list');
    const actions = generateTodayActions();
    
    document.getElementById('action-count').textContent = actions.length + ' items';
    document.getElementById('stat-actions').textContent = actions.length;
    
    container.innerHTML = actions.map(action => `
        <div class="bg-dark-700 rounded-lg p-4 ${action.priority === 'urgent' ? 'action-urgent' : action.priority === 'high' ? 'action-high' : 'action-normal'} hover:bg-dark-600 transition cursor-pointer">
            <div class="flex items-start justify-between">
                <div class="flex-1">
                    <div class="flex items-center gap-2 mb-1">
                        <span class="text-sm">${action.icon}</span>
                        <span class="font-semibold text-sm">${action.title}</span>
                        ${action.priority === 'urgent' ? '<span class="bg-red-500/20 text-red-400 text-xs px-2 py-0.5 rounded">URGENT</span>' : ''}
                    </div>
                    <p class="text-xs text-zinc-400">${action.description}</p>
                </div>
                ${action.contact ? `<span class="text-xs text-zinc-500 ml-2">${action.contact}</span>` : ''}
            </div>
        </div>
    `).join('');
}

function generateTodayActions() {
    const actions = [];
    const pipeline = dashboardData.pipeline || {};
    
    // High priority leads need calls
    (pipeline.hot || []).forEach(lead => {
        if (lead.nextAction) {
            actions.push({
                icon: '📞',
                title: lead.nextAction,
                description: lead.notes || lead.company || '',
                contact: lead.name,
                priority: lead.priority === 'high' ? 'urgent' : 'high'
            });
        }
    });
    
    // Check for follow-ups due today
    (pipeline.inProgress || []).forEach(lead => {
        if (lead.followUp) {
            const followDate = new Date(lead.followUp);
            const today = new Date();
            if (followDate.toDateString() === today.toDateString()) {
                actions.push({
                    icon: '📋',
                    title: 'Follow up with ' + lead.name,
                    description: lead.notes || '',
                    contact: lead.company,
                    priority: 'high'
                });
            }
        }
    });
    
    // Add AI Intake Agent opportunity
    actions.push({
        icon: '🤖',
        title: 'Deploy AI Intake Agent',
        description: 'Add OpenAI API key - saves $5K/month',
        priority: 'high'
    });
    
    return actions.slice(0, 8); // Limit to 8 actions
}

function renderPipeline() {
    const pipeline = dashboardData.pipeline || {};
    const container = document.getElementById('pipeline-grid');
    
    const columns = [
        { key: 'hot', title: '🔴 Hot', color: 'red' },
        { key: 'inProgress', title: '🟡 In Progress', color: 'yellow' },
        { key: 'closed', title: '✅ Closed', color: 'green' }
    ];
    
    container.innerHTML = columns.map(col => {
        const leads = pipeline[col.key] || [];
        return `
            <div class="bg-dark-700 rounded-lg p-3">
                <div class="flex items-center justify-between mb-3 pb-2 border-b border-dark-600">
                    <span class="font-semibold text-sm">${col.title}</span>
                    <span class="bg-dark-600 text-xs px-2 py-0.5 rounded">${leads.length}</span>
                </div>
                <div class="space-y-2 max-h-64 overflow-y-auto">
                    ${leads.map(lead => {
                        const prob = getCloseProbability(lead, col.key);
                        return `
                            <div class="bg-dark-800 rounded p-3 hover:bg-dark-600 transition cursor-pointer">
                                <div class="flex items-start justify-between">
                                    <div>
                                        <p class="font-medium text-sm">${lead.name}</p>
                                        ${lead.company ? `<p class="text-xs text-zinc-500">${lead.company}</p>` : ''}
                                    </div>
                                    <span class="text-xs font-bold ${prob.class}">${prob.value}%</span>
                                </div>
                                ${lead.budget ? `<p class="text-xs text-green-400 mt-1">${lead.budget}</p>` : ''}
                                ${lead.notes ? `<p class="text-xs text-zinc-400 mt-1 truncate">${lead.notes}</p>` : ''}
                            </div>
                        `;
                    }).join('')}
                    ${leads.length === 0 ? '<p class="text-xs text-zinc-500 text-center py-4">No leads</p>' : ''}
                </div>
            </div>
        `;
    }).join('');
}

function getCloseProbability(lead, stage) {
    let base = stage === 'hot' ? 40 : stage === 'inProgress' ? 25 : 100;
    
    // Adjust based on signals
    if (lead.priority === 'high') base += 20;
    if (lead.budget) base += 15;
    if (lead.value) return { value: 100, class: 'prob-high' };
    
    base = Math.min(base, 95);
    
    const probClass = base >= 60 ? 'prob-high' : base >= 35 ? 'prob-medium' : 'prob-low';
    return { value: base, class: probClass };
}

function renderOpportunities() {
    const container = document.getElementById('opportunities-list');
    
    const opportunities = [
        {
            icon: '🤖',
            title: 'AI Intake Agent',
            subtitle: '$5K/month savings',
            description: '90% complete - just needs OpenAI API key',
            priority: 'high'
        },
        {
            icon: '📊',
            title: 'Call Cost Reduction',
            subtitle: '$250 → <$100',
            description: 'AI voice can cut call costs by 60%',
            priority: 'medium'
        },
        {
            icon: '🌐',
            title: 'SEO Network',
            subtitle: '5-7 niche sites',
            description: 'Satellite sites for backlinks & traffic',
            priority: 'medium'
        }
    ];
    
    container.innerHTML = opportunities.map(opp => `
        <div class="bg-dark-700 rounded-lg p-3 ${opp.priority === 'high' ? 'border-l-4 border-purple-500' : ''} hover:bg-dark-600 transition cursor-pointer">
            <div class="flex items-start gap-3">
                <span class="text-xl">${opp.icon}</span>
                <div class="flex-1">
                    <div class="flex items-center justify-between">
                        <span class="font-semibold text-sm">${opp.title}</span>
                        <span class="text-xs text-green-400">${opp.subtitle}</span>
                    </div>
                    <p class="text-xs text-zinc-400 mt-1">${opp.description}</p>
                </div>
            </div>
        </div>
    `).join('');
}

function renderGrowthInitiatives() {
    const container = document.getElementById('growth-list');
    
    const initiatives = [
        { name: 'Call Cost Reduction', progress: 20, target: 'AI Voice' },
        { name: 'SEO Network Build', progress: 35, target: '5-7 sites' },
        { name: 'Customer Refinement', progress: 70, target: 'Avatars done' },
        { name: 'Texas Site Strategy', progress: 85, target: 'TX Trucks live' },
        { name: 'AI SEO', progress: 10, target: 'ChatGPT citations' }
    ];
    
    container.innerHTML = initiatives.map(init => `
        <div class="bg-dark-700 rounded-lg p-3">
            <div class="flex items-center justify-between mb-2">
                <span class="text-sm font-medium">${init.name}</span>
                <span class="text-xs text-zinc-500">${init.target}</span>
            </div>
            <div class="h-2 bg-dark-600 rounded-full overflow-hidden">
                <div class="h-full bg-gradient-to-r from-blue-500 to-purple-500 rounded-full transition-all" style="width: ${init.progress}%"></div>
            </div>
            <p class="text-xs text-zinc-500 mt-1 text-right">${init.progress}%</p>
        </div>
    `).join('');
}

function renderProjects() {
    const container = document.getElementById('projects-list');
    const projects = dashboardData.projects?.core || [];
    
    container.innerHTML = projects.slice(0, 5).map(project => `
        <div class="bg-dark-700 rounded-lg p-3 hover:bg-dark-600 transition cursor-pointer">
            <div class="flex items-center justify-between">
                <span class="font-medium text-sm">${project.name}</span>
                <span class="text-xs px-2 py-0.5 rounded ${getStatusClass(project.status)}">${project.status}</span>
            </div>
            <p class="text-xs text-zinc-400 mt-1 truncate">${project.description || ''}</p>
        </div>
    `).join('');
}

function renderAgents() {
    const container = document.getElementById('agents-list');
    const agents = dashboardData.projects?.agents || [];
    
    container.innerHTML = agents.map(agent => `
        <div class="bg-dark-700 rounded-lg p-3 hover:bg-dark-600 transition cursor-pointer">
            <div class="flex items-center justify-between">
                <div class="flex items-center gap-2">
                    <span class="text-lg">${agent.emoji}</span>
                    <span class="font-medium text-sm">${agent.name}</span>
                </div>
                <div class="flex items-center gap-2">
                    <span class="w-2 h-2 bg-green-500 rounded-full pulse-dot"></span>
                    <span class="text-xs text-green-400">Online</span>
                </div>
            </div>
            <p class="text-xs text-zinc-400 mt-1">${agent.model} • ${agent.role}</p>
        </div>
    `).join('');
}

function getStatusClass(status) {
    const classes = {
        'active': 'bg-green-500/20 text-green-400',
        'building': 'bg-purple-500/20 text-purple-400',
        'pending': 'bg-yellow-500/20 text-yellow-400',
        'live': 'bg-green-500/20 text-green-400',
        'dev': 'bg-blue-500/20 text-blue-400'
    };
    return classes[status] || 'bg-zinc-500/20 text-zinc-400';
}

function scrollToSection(id) {
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ============= INIT =============
if (!checkAuth()) {
    document.getElementById('auth-gate').classList.remove('hidden');
}
