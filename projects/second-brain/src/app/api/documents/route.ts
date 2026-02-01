import { NextRequest, NextResponse } from 'next/server';
import { getAllDocuments, createDocument, searchDocuments } from '@/lib/documents';
import { format } from 'date-fns';

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const query = searchParams.get('q');

  if (query) {
    const results = searchDocuments(query);
    return NextResponse.json(results);
  }

  const documents = getAllDocuments();
  return NextResponse.json(documents);
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { title, content, tags, type } = body;

    if (!title || !content || !type) {
      return NextResponse.json(
        { error: 'Missing required fields' },
        { status: 400 }
      );
    }

    // Determine folder based on type
    const folderMap: Record<string, string> = {
      journal: 'journal',
      concept: 'concepts',
      note: 'notes',
    };
    const folder = folderMap[type] || 'notes';

    // Generate filename
    let filename: string;
    if (type === 'journal') {
      filename = format(new Date(), 'yyyy-MM-dd');
    } else {
      filename = title
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, '-')
        .replace(/^-|-$/g, '');
    }

    const slug = createDocument(folder, filename, title, content, tags, type);

    return NextResponse.json({ slug, success: true });
  } catch (error) {
    console.error('Error creating document:', error);
    return NextResponse.json(
      { error: 'Failed to create document' },
      { status: 500 }
    );
  }
}
