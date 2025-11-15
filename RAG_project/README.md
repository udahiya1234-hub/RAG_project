# 🧠 RAG Application - Retrieval-Augmented Generation with Gemini

A full-stack web application for document-based AI Q&A, built with **Next.js 14**, **TypeScript**, and **Google Gemini 1.5 Flash API**.

## 🚀 Features

- ✅ **Upload Documents** - Support PDF, TXT, DOCX formats
- ✅ **Smart Chunking** - Automatic document chunking (800 chars, 120-char overlap)
- ✅ **RAG Chat** - Ask questions with AI-powered answers and source citations
- ✅ **Summaries** - Generate short, medium, or long summaries
- ✅ **Study Guides** - Create structured study materials
- ✅ **Quizzes** - Auto-generate 3 MCQ questions
- ✅ **Flashcards** - Create 5-7 interactive flashcards
- ✅ **Mind Maps** - Generate Markdown-formatted mind maps
- ✅ **In-Memory Storage** - No database needed (everything in RAM)
- ✅ **Mobile Responsive** - Works on desktop and mobile
- ✅ **Vercel Ready** - Deploy in one click

## 📋 Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: TailwindCSS
- **AI Model**: Google Gemini 1.5 Flash
- **PDF Parsing**: pdf.js
- **Word Parsing**: mammoth
- **HTTP Client**: Axios
- **Icons**: Lucide React
- **Deployment**: Vercel

## 🛠️ Installation

### Prerequisites
- Node.js 18+
- npm or yarn
- Google Gemini API Key

### Local Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd RAG_project
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Create environment file**
   ```bash
   echo "GEMINI_API_KEY=your_api_key_here" > .env.local
   ```

   Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

4. **Run development server**
   ```bash
   npm run dev
   ```

5. **Open in browser**
   ```
   http://localhost:3000
   ```

## 🚀 Deployment to Vercel

### Quick Deploy

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Connect to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Select your repository
   - Click "Import"

3. **Add Environment Variables**
   - In Vercel dashboard, go to Settings → Environment Variables
   - Add: `GEMINI_API_KEY=your_api_key_here`
   - Click "Save"

4. **Deploy**
   - Click "Deploy"
   - Wait for build to complete
   - Your app is live! 🎉

### Alternative: Deploy with Vercel CLI

```bash
npm i -g vercel
vercel
```

Then add environment variables in the dashboard.

## 📁 Project Structure

```
RAG_project/
├── src/
│   ├── app/
│   │   ├── api/
│   │   │   ├── chat/route.ts
│   │   │   ├── upload/route.ts
│   │   │   ├── summary/route.ts
│   │   │   ├── quiz/route.ts
│   │   │   ├── flashcards/route.ts
│   │   │   └── mindmap/route.ts
│   │   ├── chat/page.tsx
│   │   ├── upload/page.tsx
│   │   ├── summary/page.tsx
│   │   ├── study-guide/page.tsx
│   │   ├── quiz/page.tsx
│   │   ├── flashcards/page.tsx
│   │   ├── mindmap/page.tsx
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── globals.css
│   │   └── Navigation.tsx
│   ├── components/
│   │   ├── ChatPanel.tsx
│   │   ├── DocumentUpload.tsx
│   │   ├── Summary.tsx
│   │   ├── StudyGuide.tsx
│   │   ├── Quiz.tsx
│   │   ├── Flashcards.tsx
│   │   └── MindMap.tsx
│   ├── lib/
│   │   ├── services/
│   │   │   ├── chunkingService.ts
│   │   │   ├── parsingService.ts
│   │   │   ├── ragService.ts
│   │   │   ├── assessmentService.ts
│   │   │   └── apiClient.ts
│   │   └── types/
│   │       └── index.ts
│   └── public/
├── package.json
├── tsconfig.json
├── tailwind.config.js
├── postcss.config.js
├── next.config.js
└── README.md
```

## 📖 Usage Guide

### 1. Upload Documents

1. Go to **Upload** page
2. Click the upload area or drag & drop
3. Select PDF, TXT, or DOCX file
4. Wait for processing (chunking happens automatically)
5. See confirmation with chunk count

### 2. Chat with Documents

1. Go to **Chat** page
2. Type a question about your documents
3. Press Enter or click Send
4. AI generates answer with sources
5. Sources show filename and chunk number

### 3. Generate Summaries

1. Go to **Summary** page
2. Choose length: Short (100-150), Medium (200-300), Long (500-700)
3. Click "Generate Summary"
4. View formatted summary

### 4. Create Study Guide

1. Go to **Study Guide** page
2. Click "Generate Study Guide"
3. AI creates comprehensive material with sections

### 5. Take Quiz

1. Go to **Quiz** page
2. Click "Generate Quiz"
3. Answer 3 multiple-choice questions
4. Click "Submit Quiz"
5. See results with explanations

### 6. Use Flashcards

1. Go to **Flashcards** page
2. Click "Generate Flashcards"
3. Click card to flip between Q&A
4. Use Previous/Next to navigate
5. Generate new sets as needed

### 7. View Mind Map

1. Go to **Mind Map** page
2. Click "Generate Mind Map"
3. See Markdown-formatted structure
4. Copy for use in other tools

## 🔧 API Endpoints

### POST /api/upload
Uploads and chunks a document.

**Request:**
```javascript
FormData {
  file: File
}
```

**Response:**
```json
{
  "success": true,
  "message": "Successfully uploaded...",
  "chunksCreated": 5,
  "filename": "document.pdf"
}
```

### POST /api/chat
Retrieves relevant chunks and generates answer.

**Request:**
```json
{
  "query": "What is this document about?",
  "conversationHistory": []
}
```

**Response:**
```json
{
  "answer": "Short answer",
  "explanation": ["Point 1", "Point 2"],
  "sources": [
    {
      "filename": "doc.pdf",
      "chunkIndex": 0,
      "content": "..."
    }
  ],
  "raw": "Full formatted response"
}
```

### POST /api/summary
Generates document summary.

**Request:**
```json
{
  "length": "medium"
}
```

**Response:**
```json
{
  "summary": "Summary text...",
  "keyPoints": ["Point 1", "Point 2"]
}
```

### POST /api/quiz
Generates 3 MCQ questions.

**Response:**
```json
{
  "questions": [
    {
      "id": "q1",
      "question": "Question?",
      "options": ["A", "B", "C", "D"],
      "correctAnswer": "A",
      "explanation": "Why A is correct"
    }
  ]
}
```

### POST /api/flashcards
Generates 5-7 flashcards.

**Response:**
```json
{
  "cards": [
    {
      "id": "fc1",
      "front": "Question",
      "back": "Answer",
      "category": "Category"
    }
  ]
}
```

### POST /api/mindmap
Generates mind map.

**Response:**
```json
{
  "mindmap": "# Main Topic\n## Subtopic\n- Point 1"
}
```

## ⚙️ Configuration

### Environment Variables

```env
# Required
GEMINI_API_KEY=your_google_ai_studio_api_key

# Optional
API_BASE=http://localhost:3000  # For development
```

### Chunking Parameters

Edit in `src/lib/services/chunkingService.ts`:

```typescript
export function chunkText(
  text: string,
  chunkSize: number = 800,      // Size of each chunk
  overlap: number = 120          // Overlap between chunks
)
```

### Gemini Model

Change model in `src/lib/services/ragService.ts`:

```typescript
const model = client.getGenerativeModel({ 
  model: 'gemini-1.5-flash'  // or 'gemini-pro'
});
```

## 🧪 Testing

### Local Testing

```bash
# Dev mode with hot reload
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linter
npm run lint
```

### Test Workflow

1. Upload a sample document
2. Ask a relevant question
3. Verify answer has sources
4. Generate different content types
5. Check mobile responsive design

## 🐛 Troubleshooting

### API Key Not Working
- Verify key in [Google AI Studio](https://aistudio.google.com/app/apikey)
- Check `.env.local` file exists
- Restart dev server after adding key
- On Vercel: Check Environment Variables in Settings

### PDF Upload Fails
- Ensure file is valid PDF
- Check file size (large PDFs may timeout)
- Try TXT or DOCX format
- Check browser console for errors

### Chat Returns Empty
- Verify documents are uploaded first
- Check chunking worked (should see confirmation)
- Ensure GEMINI_API_KEY is set
- Check API quota in Google AI Studio

### Slow Response
- Reduce chunk count (fewer documents = faster)
- Try smaller documents first
- Check internet connection
- Verify Gemini API is not rate-limited

## 📚 Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [Google Generative AI](https://ai.google.dev)
- [TailwindCSS](https://tailwindcss.com)
- [TypeScript](https://www.typescriptlang.org)

## 📄 License

MIT License - feel free to use for any purpose

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📞 Support

For issues or questions:
1. Check documentation above
2. Review browser console errors
3. Check API key and environment setup
4. Open an issue with details

---

**Happy Learning! 🚀📚**
