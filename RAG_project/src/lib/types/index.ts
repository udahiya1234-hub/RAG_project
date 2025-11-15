export interface Chunk {
  id: string;
  content: string;
  filename: string;
  chunkIndex: number;
  startIndex: number;
  endIndex: number;
  embedding?: number[];
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: SourceReference[];
  timestamp: Date;
}

export interface SourceReference {
  filename: string;
  chunkIndex: number;
  content: string;
}

export interface UploadResponse {
  success: boolean;
  message: string;
  chunksCreated?: number;
  filename?: string;
}

export interface ChatRequest {
  query: string;
  conversationHistory?: ChatMessage[];
}

export interface ChatResponse {
  answer: string;
  explanation: string[];
  sources: SourceReference[];
  raw: string;
}

export interface Quiz {
  questions: QuizQuestion[];
}

export interface QuizQuestion {
  id: string;
  question: string;
  options: string[];
  correctAnswer: string;
  explanation: string;
}

export interface Flashcard {
  id: string;
  front: string;
  back: string;
  category?: string;
}

export interface FlashcardSet {
  cards: Flashcard[];
}

export interface MindMap {
  title: string;
  content: string;
}

export interface SummaryRequest {
  length?: 'short' | 'medium' | 'long';
}

export interface SummaryResponse {
  summary: string;
  keyPoints: string[];
}

export interface StudyGuideResponse {
  guide: string;
  sections: string[];
}
