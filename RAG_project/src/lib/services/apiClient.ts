import axios from 'axios';
import { ChatRequest, ChatResponse, UploadResponse } from '../types/index';

const API_BASE = typeof window !== 'undefined' ? '' : process.env.API_BASE || '';

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

export async function uploadDocument(file: File): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await axios.post('/api/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
}

export async function chatQuery(request: ChatRequest): Promise<ChatResponse> {
  const response = await api.post('/api/chat', request);
  return response.data;
}

export async function getSummary(length?: string): Promise<{ summary: string }> {
  const response = await api.post('/api/summary', { length });
  return response.data;
}

export async function getStudyGuide(): Promise<{ guide: string }> {
  const response = await api.post('/api/study-guide', {});
  return response.data;
}

export async function getMindMap(): Promise<{ mindmap: string }> {
  const response = await api.post('/api/mindmap', {});
  return response.data;
}

export async function getQuiz() {
  const response = await api.post('/api/quiz', {});
  return response.data;
}

export async function getFlashcards() {
  const response = await api.post('/api/flashcards', {});
  return response.data;
}
