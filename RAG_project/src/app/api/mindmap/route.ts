import { NextRequest, NextResponse } from 'next/server';
import { generateMindMap } from '@/lib/services/ragService';

export async function POST(request: NextRequest) {
  try {
    const mindmap = await generateMindMap();

    return NextResponse.json({ mindmap });
  } catch (error) {
    console.error('MindMap error:', error);
    return NextResponse.json(
      { error: 'Failed to generate mind map' },
      { status: 500 }
    );
  }
}
