import { Chunk } from '../types/index';

// Global in-memory chunk store
let globalChunks: Chunk[] = [];

export const getGlobalChunks = (): Chunk[] => globalChunks;

export const setGlobalChunks = (chunks: Chunk[]): void => {
  globalChunks = chunks;
};

export const addChunks = (chunks: Chunk[]): void => {
  globalChunks = [...globalChunks, ...chunks];
};

export const clearChunks = (): void => {
  globalChunks = [];
};

export function cleanText(text: string): string {
  return text
    .replace(/\s+/g, ' ')
    .replace(/[\r\n]+/g, ' ')
    .trim();
}

export function chunkText(
  text: string,
  chunkSize: number = 800,
  overlap: number = 120
): string[] {
  const cleanedText = cleanText(text);
  const chunks: string[] = [];

  for (let i = 0; i < cleanedText.length; i += chunkSize - overlap) {
    const chunk = cleanedText.substring(i, i + chunkSize);
    if (chunk.length > 0) {
      chunks.push(chunk);
    }
  }

  return chunks;
}

export function cosineSimilarity(a: number[], b: number[]): number {
  const dotProduct = a.reduce((sum, val, i) => sum + val * b[i], 0);
  const magnitudeA = Math.sqrt(a.reduce((sum, val) => sum + val * val, 0));
  const magnitudeB = Math.sqrt(b.reduce((sum, val) => sum + val * val, 0));

  if (magnitudeA === 0 || magnitudeB === 0) return 0;
  return dotProduct / (magnitudeA * magnitudeB);
}

export function keywordSimilarity(query: string, text: string): number {
  const queryWords = query.toLowerCase().split(/\s+/);
  const textWords = text.toLowerCase().split(/\s+/);

  const matchCount = queryWords.filter((word) =>
    textWords.some((tWord) => tWord.includes(word) || word.includes(tWord))
  ).length;

  return matchCount / Math.max(queryWords.length, 1);
}

export function retrieveRelevantChunks(
  query: string,
  chunks: Chunk[] = globalChunks,
  topK: number = 5
): Chunk[] {
  const scored = chunks.map((chunk) => ({
    chunk,
    score: keywordSimilarity(query, chunk.content),
  }));

  scored.sort((a, b) => b.score - a.score);

  return scored
    .filter((item) => item.score > 0)
    .slice(0, topK)
    .map((item) => item.chunk);
}

export function createChunkObjects(
  textChunks: string[],
  filename: string
): Chunk[] {
  return textChunks.map((content, index) => ({
    id: `${filename}-chunk-${index}`,
    content,
    filename,
    chunkIndex: index,
    startIndex: 0,
    endIndex: content.length,
  }));
}
