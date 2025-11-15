import { ChatResponse, SourceReference } from '../types/index';
import { retrieveRelevantChunks, getGlobalChunks } from './chunkingService';
import { GoogleGenerativeAI } from '@google/generative-ai';

const client = new GoogleGenerativeAI(process.env.GEMINI_API_KEY || '');

export async function generateRAGAnswer(query: string): Promise<ChatResponse> {
  const retrievedChunks = retrieveRelevantChunks(query);

  if (retrievedChunks.length === 0) {
    return {
      answer: 'No relevant documents found. Please upload documents first.',
      explanation: ['No context available'],
      sources: [],
      raw: 'No documents in memory',
    };
  }

  const context = retrievedChunks
    .map(
      (chunk, i) => `[Source ${i + 1} - ${chunk.filename} | Chunk ${chunk.chunkIndex}]\n${chunk.content}`
    )
    .join('\n\n');

  const prompt = `You are a helpful assistant. Answer the following query ONLY using the provided context. If the answer is not in the context, say "I don't have information about this in the provided documents."

Query: ${query}

Context:
${context}

Please provide your answer in this exact format:

### ✅ Answer
[Your short and clear answer here]

### 📌 Explanation
- [Bullet point 1]
- [Bullet point 2]
- [Bullet point 3]

### 📚 Sources Used
[List sources in format: source: FILENAME | chunk: NUMBER]`;

  try {
    const model = client.getGenerativeModel({ model: 'gemini-1.5-flash' });
    const result = await model.generateContent(prompt);
    const raw = result.response.text();

    const sources: SourceReference[] = retrievedChunks.map((chunk) => ({
      filename: chunk.filename,
      chunkIndex: chunk.chunkIndex,
      content: chunk.content,
    }));

    return {
      answer: extractSection(raw, 'Answer'),
      explanation: extractBullets(extractSection(raw, 'Explanation')),
      sources,
      raw,
    };
  } catch (error) {
    throw new Error(`Failed to generate answer: ${error}`);
  }
}

export async function generateSummary(length: 'short' | 'medium' | 'long' = 'medium'): Promise<string> {
  const chunks = getGlobalChunks();

  if (chunks.length === 0) {
    return 'No documents available to summarize.';
  }

  const content = chunks.map((c) => c.content).join('\n\n');

  const lengthGuide = {
    short: '100-150 words',
    medium: '200-300 words',
    long: '500-700 words',
  };

  const prompt = `Create a ${length} summary of the following text in ${lengthGuide[length]}:

${content}`;

  try {
    const model = client.getGenerativeModel({ model: 'gemini-1.5-flash' });
    const result = await model.generateContent(prompt);
    return result.response.text();
  } catch (error) {
    throw new Error(`Failed to generate summary: ${error}`);
  }
}

export async function generateStudyGuide(): Promise<string> {
  const chunks = getGlobalChunks();

  if (chunks.length === 0) {
    return 'No documents available for study guide.';
  }

  const content = chunks.map((c) => c.content).join('\n\n');

  const prompt = `Create a comprehensive study guide from the following material. Include key concepts, important points, and learning objectives:

${content}`;

  try {
    const model = client.getGenerativeModel({ model: 'gemini-1.5-flash' });
    const result = await model.generateContent(prompt);
    return result.response.text();
  } catch (error) {
    throw new Error(`Failed to generate study guide: ${error}`);
  }
}

export async function generateMindMap(): Promise<string> {
  const chunks = getGlobalChunks();

  if (chunks.length === 0) {
    return 'No documents available for mind map.';
  }

  const content = chunks.map((c) => c.content).join('\n\n');

  const prompt = `Create a structured mind map in Markdown format for the following content. Use headers, bullet points, and nesting to show relationships:

${content}

Format as Markdown with clear hierarchy:
# Main Topic
## Sub Topic 1
- Point 1
- Point 2
## Sub Topic 2
- Point 1`;

  try {
    const model = client.getGenerativeModel({ model: 'gemini-1.5-flash' });
    const result = await model.generateContent(prompt);
    return result.response.text();
  } catch (error) {
    throw new Error(`Failed to generate mind map: ${error}`);
  }
}

function extractSection(text: string, sectionName: string): string {
  const regex = new RegExp(
    `###\\s*(?:✅|📌|📚)?\\s*${sectionName}[^]*?(?=###|$)`,
    'i'
  );
  const match = text.match(regex);
  if (match) {
    return match[0].replace(new RegExp(`###\\s*(?:✅|📌|📚)?\\s*${sectionName}`, 'i'), '').trim();
  }
  return '';
}

function extractBullets(text: string): string[] {
  return text
    .split('\n')
    .filter((line) => line.trim().startsWith('-'))
    .map((line) => line.replace(/^-\s*/, '').trim())
    .filter((line) => line.length > 0);
}
