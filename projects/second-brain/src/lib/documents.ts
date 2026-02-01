import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';

export interface Document {
  slug: string;
  title: string;
  date: string;
  tags: string[];
  type: 'journal' | 'concept' | 'note';
  content: string;
  excerpt: string;
  folder: string;
}

export interface DocumentMeta {
  slug: string;
  title: string;
  date: string;
  tags: string[];
  type: 'journal' | 'concept' | 'note';
  excerpt: string;
  folder: string;
}

const DOCUMENTS_DIR = path.join(process.cwd(), 'documents');

// Ensure documents directory exists
function ensureDocumentsDir() {
  if (!fs.existsSync(DOCUMENTS_DIR)) {
    fs.mkdirSync(DOCUMENTS_DIR, { recursive: true });
  }
  const folders = ['journal', 'concepts', 'notes'];
  folders.forEach(folder => {
    const folderPath = path.join(DOCUMENTS_DIR, folder);
    if (!fs.existsSync(folderPath)) {
      fs.mkdirSync(folderPath, { recursive: true });
    }
  });
}

function getFilesRecursively(dir: string, baseDir: string = dir): string[] {
  ensureDocumentsDir();
  
  if (!fs.existsSync(dir)) {
    return [];
  }

  const files: string[] = [];
  const entries = fs.readdirSync(dir, { withFileTypes: true });

  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...getFilesRecursively(fullPath, baseDir));
    } else if (entry.name.endsWith('.md')) {
      files.push(fullPath);
    }
  }

  return files;
}

export function getAllDocuments(): DocumentMeta[] {
  ensureDocumentsDir();
  const files = getFilesRecursively(DOCUMENTS_DIR);

  const documents = files.map(filePath => {
    const fileContent = fs.readFileSync(filePath, 'utf-8');
    const { data, content } = matter(fileContent);
    
    const relativePath = path.relative(DOCUMENTS_DIR, filePath);
    const slug = relativePath.replace(/\.md$/, '');
    const folder = path.dirname(relativePath);

    return {
      slug,
      title: data.title || path.basename(filePath, '.md'),
      date: data.date || fs.statSync(filePath).mtime.toISOString().split('T')[0],
      tags: data.tags || [],
      type: data.type || (folder === 'journal' ? 'journal' : folder === 'concepts' ? 'concept' : 'note'),
      excerpt: content.slice(0, 200).replace(/\n/g, ' ').trim() + '...',
      folder: folder === '.' ? '' : folder,
    };
  });

  return documents.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
}

export function getDocument(slug: string): Document | null {
  ensureDocumentsDir();
  const filePath = path.join(DOCUMENTS_DIR, `${slug}.md`);

  if (!fs.existsSync(filePath)) {
    return null;
  }

  const fileContent = fs.readFileSync(filePath, 'utf-8');
  const { data, content } = matter(fileContent);
  
  const folder = path.dirname(slug);

  return {
    slug,
    title: data.title || path.basename(slug),
    date: data.date || fs.statSync(filePath).mtime.toISOString().split('T')[0],
    tags: data.tags || [],
    type: data.type || (folder === 'journal' ? 'journal' : folder === 'concepts' ? 'concept' : 'note'),
    content,
    excerpt: content.slice(0, 200).replace(/\n/g, ' ').trim() + '...',
    folder: folder === '.' ? '' : folder,
  };
}

export function createDocument(
  folder: string,
  filename: string,
  title: string,
  content: string,
  tags: string[],
  type: 'journal' | 'concept' | 'note'
): string {
  ensureDocumentsDir();
  
  const folderPath = path.join(DOCUMENTS_DIR, folder);
  if (!fs.existsSync(folderPath)) {
    fs.mkdirSync(folderPath, { recursive: true });
  }

  const safeName = filename.replace(/[^a-z0-9-]/gi, '-').toLowerCase();
  const filePath = path.join(folderPath, `${safeName}.md`);

  const frontmatter = {
    title,
    date: new Date().toISOString().split('T')[0],
    tags,
    type,
  };

  const fileContent = matter.stringify(content, frontmatter);
  fs.writeFileSync(filePath, fileContent);

  return `${folder}/${safeName}`;
}

export function updateDocument(
  slug: string,
  title: string,
  content: string,
  tags: string[]
): boolean {
  ensureDocumentsDir();
  const filePath = path.join(DOCUMENTS_DIR, `${slug}.md`);

  if (!fs.existsSync(filePath)) {
    return false;
  }

  const existing = fs.readFileSync(filePath, 'utf-8');
  const { data } = matter(existing);

  const frontmatter = {
    ...data,
    title,
    tags,
  };

  const fileContent = matter.stringify(content, frontmatter);
  fs.writeFileSync(filePath, fileContent);

  return true;
}

export function deleteDocument(slug: string): boolean {
  ensureDocumentsDir();
  const filePath = path.join(DOCUMENTS_DIR, `${slug}.md`);

  if (!fs.existsSync(filePath)) {
    return false;
  }

  fs.unlinkSync(filePath);
  return true;
}

export function searchDocuments(query: string): DocumentMeta[] {
  const documents = getAllDocuments();
  const lowerQuery = query.toLowerCase();

  return documents.filter(doc => 
    doc.title.toLowerCase().includes(lowerQuery) ||
    doc.excerpt.toLowerCase().includes(lowerQuery) ||
    doc.tags.some(tag => tag.toLowerCase().includes(lowerQuery))
  );
}

export function getDocumentsByTag(tag: string): DocumentMeta[] {
  const documents = getAllDocuments();
  return documents.filter(doc => doc.tags.includes(tag));
}

export function getDocumentsByFolder(folder: string): DocumentMeta[] {
  const documents = getAllDocuments();
  return documents.filter(doc => doc.folder === folder);
}

export function getAllTags(): { tag: string; count: number }[] {
  const documents = getAllDocuments();
  const tagCounts: Record<string, number> = {};

  documents.forEach(doc => {
    doc.tags.forEach(tag => {
      tagCounts[tag] = (tagCounts[tag] || 0) + 1;
    });
  });

  return Object.entries(tagCounts)
    .map(([tag, count]) => ({ tag, count }))
    .sort((a, b) => b.count - a.count);
}

export function getFolderStructure(): { name: string; count: number }[] {
  const documents = getAllDocuments();
  const folderCounts: Record<string, number> = {};

  documents.forEach(doc => {
    const folder = doc.folder || 'root';
    folderCounts[folder] = (folderCounts[folder] || 0) + 1;
  });

  return Object.entries(folderCounts)
    .map(([name, count]) => ({ name, count }))
    .sort((a, b) => a.name.localeCompare(b.name));
}
