# Dashboard Discovery Plan
**Created:** 2026-01-31T08:07Z
**Goal:** Comprehensive discovery of all projects, tools, integrations to build a complete business dashboard

## Primary Focus
**Client Acquisition for MVA Lead Gen** — everything else supports this

## Discovery Areas

### 1. Projects (clawd/projects/)
- [ ] pi-vendors (267M) — PI vendor intelligence
- [ ] vendor-db — Vendor database
- [ ] vendors-kuriosbrand — Site project

### 2. Kurios Data (data/kurios-finish/)
- [ ] automation/ — Automation scripts and workflows
- [ ] business/ — Business documents, SOPs, strategies
- [ ] data/ — Raw data, buyer insights, leads
- [ ] sites/ — Website projects (texas truck accidents?)
- [ ] docs/ — Documentation
- [ ] .claude/ — Previous Claude context

### 3. Sites to Find
- [ ] texastruckaccidents.net — Mentioned by Marko
- [ ] texas-mva-site
- [ ] mva-engine
- [ ] leads.kuriosbrand.com
- [ ] Any other domains/sites

### 4. Tools to Catalog
- [ ] YouTube Transcriber — Where is it?
- [ ] Scrapers (buyer profile, PI vendors)
- [ ] GHL integrations
- [ ] DataForSEO scripts
- [ ] X/Twitter tools

### 5. Integrations (from .config/)
- [ ] gcal-pro — Google Calendar
- [ ] notion — Notion API
- [ ] moltbook — Moltbook engagement
- [ ] slack — Slack integration
- [ ] x-api — Twitter/X API
- [ ] pulse — Unknown

### 6. Agents
- [ ] Sierra (main) — This instance
- [ ] SCOUT — Intel gatherer

## Agent Deployment

| Agent # | Focus Area | Status |
|---------|------------|--------|
| 1 | Projects (pi-vendors, vendor-db) | Spawning |
| 2 | Kurios automation + business | Spawning |
| 3 | Kurios sites + data | Spawning |
| 4 | Tools + scripts discovery | Spawning |
| 5 | Integrations + APIs | Spawning |

## Output Format
Each agent should produce:
```json
{
  "area": "string",
  "projects": [{ "name", "path", "description", "status", "details" }],
  "tools": [{ "name", "path", "description", "usage" }],
  "sites": [{ "name", "url", "path", "status", "stack" }],
  "insights": ["string"]
}
```

## Dashboard Additions Needed
- Tools tab
- Richer project details
- Sites discovery
- Integration status
- Client acquisition metrics
- Revenue tracking
