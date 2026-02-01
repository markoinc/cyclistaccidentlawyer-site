# Second Brain 🧠

Never lose an idea again. A document viewer for capturing insights, ideas, and important concepts.

Built based on Alex Finn's recommendation - Obsidian meets Linear aesthetic.

## Features

- **📝 Journal Entries**: Daily logs of discussions and events
- **💡 Concept Documents**: Deep dives on important ideas  
- **📋 Quick Notes**: Rapid capture of fleeting thoughts
- **🏷️ Auto-Tagging**: Categories for revenue ideas, client work, automation, content, strategy, learning, action items
- **🔍 Command Palette Search**: Press `⌘K` for quick search
- **📅 Journal Calendar**: Visual calendar showing entries
- **📁 Folder Navigation**: Organize by journal/concepts/notes

## Tech Stack

- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- File-based storage (Markdown with frontmatter)
- gray-matter for parsing
- react-markdown for rendering

## Getting Started

```bash
# Development
npm run dev

# Production build
npm run build
npm start
```

Default port: 3000

## Document Structure

Documents are stored in `/documents` folder:

```
documents/
├── journal/
│   └── 2025-01-31.md
├── concepts/
│   └── proactive-ai-workflows.md
└── notes/
    └── quick-note.md
```

## Frontmatter Format

```yaml
---
title: "Document Title"
date: "2025-01-31"
tags: ["automation", "strategy"]
type: "journal" | "concept" | "note"
---
```

## Tag Categories

| Tag | Color | Use For |
|-----|-------|---------|
| revenue-idea | 🟢 Green | Money-making opportunities |
| client-work | 🔵 Blue | Client-related notes |
| automation | 🟣 Purple | Automation/workflow ideas |
| content | 🟠 Orange | Content ideas for social/marketing |
| strategy | 🔴 Rose | Business strategy |
| learning | 🔷 Cyan | New concepts learned |
| action-item | 🟡 Yellow | Things to do |

## API Endpoints

- `GET /api/documents` - List all documents
- `GET /api/documents?q=query` - Search documents
- `POST /api/documents` - Create new document
- `GET /api/documents/[slug]` - Get single document
- `PUT /api/documents/[slug]` - Update document
- `DELETE /api/documents/[slug]` - Delete document

## Integration with Clawdbot

Clawdbot can automatically:
1. Create journal entries from daily discussions
2. Generate concept documents for important topics
3. Auto-tag based on content analysis
4. Search and retrieve past insights

---

*Part of the $9.6M exit journey - capturing every insight permanently.*
