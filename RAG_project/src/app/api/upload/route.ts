import { NextRequest, NextResponse } from 'next/server';
import { parseDocument } from '@/lib/services/parsingService';
import {
  chunkText,
  createChunkObjects,
  addChunks,
} from '@/lib/services/chunkingService';

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    const file = formData.get('file') as File;

    if (!file) {
      return NextResponse.json(
        { success: false, message: 'No file provided' },
        { status: 400 }
      );
    }

    // Parse document
    const text = await parseDocument(file);

    // Chunk text
    const chunks = chunkText(text, 800, 120);

    // Create chunk objects
    const chunkObjects = createChunkObjects(chunks, file.name);

    // Add to global store
    addChunks(chunkObjects);

    return NextResponse.json({
      success: true,
      message: `Successfully uploaded and chunked ${file.name}`,
      chunksCreated: chunkObjects.length,
      filename: file.name,
    });
  } catch (error) {
    console.error('Upload error:', error);
    return NextResponse.json(
      {
        success: false,
        message: `Failed to upload document: ${error}`,
      },
      { status: 500 }
    );
  }
}
