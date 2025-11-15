import { NextRequest, NextResponse } from 'next/server';
import { generateSummary } from '@/lib/services/ragService';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { length = 'medium' } = body;

    const summary = await generateSummary(length);

    return NextResponse.json({
      summary,
      keyPoints: extractKeyPoints(summary),
    });
  } catch (error) {
    console.error('Summary error:', error);
    return NextResponse.json(
      { error: 'Failed to generate summary' },
      { status: 500 }
    );
  }
}

function extractKeyPoints(summary: string): string[] {
  // Extract first few sentences as key points
  const sentences = summary.match(/[^.!?]+[.!?]+/g) || [];
  return sentences
    .slice(0, 5)
    .map((s) => s.trim())
    .filter((s) => s.length > 0);
}
