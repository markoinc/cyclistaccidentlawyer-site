# Second Brain - Document System Specification

## Overview
A Next.js app for capturing and organizing insights, ideas, and important concepts. Think Obsidian meets Linear - clean, minimal, fast.

## Core Features

### 1. Document Viewer
- Left sidebar with document list (collapsible folders)
- Main content area with markdown rendering
- Clean, minimal UI with dark/light mode
- Fast search across all documents

### 2. Document Types
- **Journal Entries**: Daily logs of discussions and events (auto-dated)
- **Concept Documents**: Deep dives on important ideas
- **Quick Notes**: Rapid capture of fleeting thoughts

### 3. Auto-Tagging System
Categories (multi-select):
- `revenue-idea` - Money-making opportunities
- `client-work` - Client-related notes
- `automation` - Automation/workflow ideas
- `content` - Content ideas for social/marketing
- `strategy` - Business strategy
- `learning` - New concepts learned
- `action-item` - Things to do

### 4. Folder Structure
```
/documents
  /journal
    /2025-01-31.md
    /2025-01-30.md
  /concepts
    /topic-name.md
  /notes
    /quick-note.md
```

## Tech Stack
- Next.js 14 (App Router)
- Tailwind CSS
- TypeScript
- File-based storage (markdown files)
- gray-matter for frontmatter parsing
- react-markdown for rendering

## UI Design (Linear-inspired)
- Monospace headers
- Subtle borders
- Muted colors with accent highlights
- Keyboard shortcuts
- Command palette (Cmd+K)
- Smooth transitions

## Document Frontmatter
```yaml
---
title: Document Title
date: 2025-01-31
tags: [revenue-idea, automation]
type: journal | concept | note
---
```

## API Routes
- GET /api/documents - List all documents
- GET /api/documents/[slug] - Get single document
- POST /api/documents - Create new document
- PUT /api/documents/[slug] - Update document
- DELETE /api/documents/[slug] - Delete document
- GET /api/search?q=query - Search documents

## Pages
- `/` - Dashboard with recent documents and stats
- `/documents` - Full document browser
- `/documents/[...slug]` - Individual document view
- `/new` - Create new document
- `/journal` - Journal-specific view (calendar)

## Key UI Components
1. Sidebar - Document navigation tree
2. DocumentCard - Preview card in lists
3. Editor - Markdown editor with preview
4. TagBadge - Colored tag pills
5. SearchCommand - Command palette
6. CalendarView - Journal calendar picker

## Styling Notes
- Background: slate-950 (dark) / white (light)
- Accent: indigo-500
- Borders: very subtle, 1px
- Fonts: Inter for body, JetBrains Mono for code
- Transitions: 150ms ease
