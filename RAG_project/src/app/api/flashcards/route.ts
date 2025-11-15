import { NextRequest, NextResponse } from 'next/server';
import { generateFlashcards } from '@/lib/services/assessmentService';

export async function POST(request: NextRequest) {
  try {
    const flashcards = await generateFlashcards();

    return NextResponse.json(flashcards);
  } catch (error) {
    console.error('Flashcards error:', error);
    return NextResponse.json(
      { error: 'Failed to generate flashcards', cards: [] },
      { status: 500 }
    );
  }
}
