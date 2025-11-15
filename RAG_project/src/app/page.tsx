import Link from 'next/link';

export default function HomePage() {
  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-12">
        <h1 className="text-5xl font-bold mb-4">🧠 RAG Application</h1>
        <p className="text-xl text-gray-600">
          Retrieval-Augmented Generation with Google Gemini 1.5 Flash
        </p>
      </div>

      <div className="grid md:grid-cols-2 gap-6 mb-12">
        <Link
          href="/upload"
          className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition"
        >
          <div className="text-4xl mb-3">📄</div>
          <h2 className="text-2xl font-bold mb-2">Upload Documents</h2>
          <p className="text-gray-600">
            Support for PDF, TXT, and DOCX files. Automatically chunked and indexed.
          </p>
        </Link>

        <Link
          href="/chat"
          className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition"
        >
          <div className="text-4xl mb-3">💬</div>
          <h2 className="text-2xl font-bold mb-2">Chat</h2>
          <p className="text-gray-600">
            Ask questions about your documents and get AI-powered answers with sources.
          </p>
        </Link>

        <Link
          href="/summary"
          className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition"
        >
          <div className="text-4xl mb-3">📝</div>
          <h2 className="text-2xl font-bold mb-2">Summary</h2>
          <p className="text-gray-600">
            Generate short, medium, or long summaries of your documents.
          </p>
        </Link>

        <Link
          href="/study-guide"
          className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition"
        >
          <div className="text-4xl mb-3">📚</div>
          <h2 className="text-2xl font-bold mb-2">Study Guide</h2>
          <p className="text-gray-600">
            Create comprehensive study guides with key concepts and learning objectives.
          </p>
        </Link>

        <Link
          href="/quiz"
          className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition"
        >
          <div className="text-4xl mb-3">❓</div>
          <h2 className="text-2xl font-bold mb-2">Quiz</h2>
          <p className="text-gray-600">
            Generate 3 multiple-choice questions to test your understanding.
          </p>
        </Link>

        <Link
          href="/flashcards"
          className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition"
        >
          <div className="text-4xl mb-3">🎴</div>
          <h2 className="text-2xl font-bold mb-2">Flashcards</h2>
          <p className="text-gray-600">
            Create interactive flashcards for memorization and review.
          </p>
        </Link>

        <Link
          href="/mindmap"
          className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition"
        >
          <div className="text-4xl mb-3">🧠</div>
          <h2 className="text-2xl font-bold mb-2">Mind Map</h2>
          <p className="text-gray-600">
            Visualize document structure and relationships with mind maps.
          </p>
        </Link>
      </div>

      <div className="bg-blue-50 border border-blue-200 rounded-lg p-8">
        <h2 className="text-2xl font-bold mb-4">🚀 Getting Started</h2>
        <ol className="space-y-3 text-gray-700">
          <li>
            <span className="font-semibold">1. Upload a document</span> - Go to the
            Upload page and select a PDF, TXT, or DOCX file
          </li>
          <li>
            <span className="font-semibold">2. Ask questions</span> - Use the Chat page
            to ask questions about your documents
          </li>
          <li>
            <span className="font-semibold">3. Generate content</span> - Create
            summaries, study guides, quizzes, flashcards, and mind maps
          </li>
        </ol>
      </div>

      <div className="mt-8 bg-gray-50 border border-gray-200 rounded-lg p-8">
        <h2 className="text-2xl font-bold mb-4">ℹ️ Features</h2>
        <ul className="grid md:grid-cols-2 gap-4 text-sm text-gray-700">
          <li>✅ Upload PDF, TXT, DOCX files</li>
          <li>✅ Automatic document chunking</li>
          <li>✅ In-memory vector search</li>
          <li>✅ Google Gemini 1.5 Flash AI</li>
          <li>✅ Chat with citations</li>
          <li>✅ Summary generation</li>
          <li>✅ Study guide creation</li>
          <li>✅ Quiz generation</li>
          <li>✅ Interactive flashcards</li>
          <li>✅ Mind map visualization</li>
          <li>✅ Mobile responsive</li>
          <li>✅ Vercel ready</li>
        </ul>
      </div>
    </div>
  );
}
