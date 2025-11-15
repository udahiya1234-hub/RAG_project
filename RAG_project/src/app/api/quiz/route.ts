import { NextRequest, NextResponse } from 'next/server';
import { generateQuiz } from '@/lib/services/assessmentService';

export async function POST(request: NextRequest) {
  try {
    const quiz = await generateQuiz();

    return NextResponse.json(quiz);
  } catch (error) {
    console.error('Quiz error:', error);
    return NextResponse.json(
      { error: 'Failed to generate quiz', questions: [] },
      { status: 500 }
    );
  }
}
