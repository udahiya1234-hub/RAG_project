import { NextRequest, NextResponse } from 'next/server';
import { generateRAGAnswer } from '@/lib/services/ragService';
import { ChatRequest, ChatResponse } from '@/lib/types/index';

export async function POST(request: NextRequest) {
  try {
    const body = (await request.json()) as ChatRequest;
    const { query } = body;

    if (!query || query.trim().length === 0) {
      return NextResponse.json(
        { error: 'Query is required' },
        { status: 400 }
      );
    }

    const response = await generateRAGAnswer(query);
    return NextResponse.json(response);
  } catch (error) {
    console.error('Chat error:', error);
    return NextResponse.json(
      { error: 'Failed to generate answer' },
      { status: 500 }
    );
  }
}
