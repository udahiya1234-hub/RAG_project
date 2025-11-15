import { Quiz, QuizQuestion, FlashcardSet, Flashcard } from '../types/index';
import { getGlobalChunks } from './chunkingService';
import { GoogleGenerativeAI } from '@google/generative-ai';

const client = new GoogleGenerativeAI(process.env.GEMINI_API_KEY || '');

export async function generateQuiz(): Promise<Quiz> {
  const chunks = getGlobalChunks();

  if (chunks.length === 0) {
    return { questions: [] };
  }

  const content = chunks.map((c) => c.content).join('\n\n');

  const prompt = `Create 3 multiple choice questions based on the following content. Return ONLY valid JSON in this exact format:
{
  "questions": [
    {
      "id": "q1",
      "question": "Question text?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correctAnswer": "Option A",
      "explanation": "Why this is correct"
    }
  ]
}

Content:
${content}`;

  try {
    const model = client.getGenerativeModel({ model: 'gemini-1.5-flash' });
    const result = await model.generateContent(prompt);
    const text = result.response.text();

    // Extract JSON from response
    const jsonMatch = text.match(/\{[\s\S]*\}/);
    if (jsonMatch) {
      const parsed = JSON.parse(jsonMatch[0]);
      return parsed;
    }
    return { questions: [] };
  } catch (error) {
    console.error('Failed to generate quiz:', error);
    return { questions: [] };
  }
}

export async function generateFlashcards(): Promise<FlashcardSet> {
  const chunks = getGlobalChunks();

  if (chunks.length === 0) {
    return { cards: [] };
  }

  const content = chunks.map((c) => c.content).join('\n\n');

  const prompt = `Create 5-7 flashcards based on the following content. Return ONLY valid JSON in this exact format:
{
  "cards": [
    {
      "id": "fc1",
      "front": "Question or term",
      "back": "Answer or definition",
      "category": "Category name"
    }
  ]
}

Content:
${content}`;

  try {
    const model = client.getGenerativeModel({ model: 'gemini-1.5-flash' });
    const result = await model.generateContent(prompt);
    const text = result.response.text();

    // Extract JSON from response
    const jsonMatch = text.match(/\{[\s\S]*\}/);
    if (jsonMatch) {
      const parsed = JSON.parse(jsonMatch[0]);
      return parsed;
    }
    return { cards: [] };
  } catch (error) {
    console.error('Failed to generate flashcards:', error);
    return { cards: [] };
  }
}
