# 📚 NotebookLM-Style RAG System

A powerful, feature-rich Retrieval-Augmented Generation (RAG) application inspired by NotebookLM. Built with **Streamlit**, **Python**, **GROQ API**, and **LLaMA 3.1**.

## ✨ Features

### Core RAG Features
✅ **Multi-document Support** - Upload PDF, DOCX, or TXT files
✅ **Smart Chunking** - Automatic text chunking with configurable overlap
✅ **Hybrid Retrieval** - Combined Jaccard similarity + TF-IDF search
✅ **Document Grounding** - Answers reference specific source chunks
✅ **Session Persistence** - RAG object stored in Streamlit session state

### Analysis & Learning Tools
🎯 **Tabs System:**
- **📖 Overview** - Document summary, key insights, table of contents
- **💬 Chat** - Document-grounded Q&A with source citations
- **🛠️ Tools** - Mind maps, flashcards, quiz, audio scripts

### Specific Tools
- **🧠 Mind Map Generator** - Hierarchical document structure
- **❓ Quiz Generator** - MCQs with explanations (3-10 questions)
- **📇 Flashcard Generator** - Q&A pairs for spaced repetition (5-20 cards)
- **🎤 Audio Summary Script** - Conversational 2-3 minute summary
- **💡 Key Insights** - Extracted key points from documents
- **📑 Table of Contents** - Auto-generated sections

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get GROQ API Key

1. Visit [https://console.groq.com/keys](https://console.groq.com/keys)
2. Sign up or log in
3. Create a new API key
4. Copy your key

### 3. Set Up Environment

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your API key:

```
GROQ_API_KEY=your_actual_groq_api_key_here
```

### 4. Run the Application

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📂 Project Structure

```
RAG_notebook/
├── app.py              # Main Streamlit application
├── rag.py              # RAG engine with all analysis features
├── utils.py            # Document loaders, cleaners, chunkers
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── .env                # Your actual API key (create this)
└── README.md          # This file
```

## 🔧 How to Use

### 1. Upload Documents
- Click the file uploader in the sidebar
- Select one or more PDF, DOCX, or TXT files
- Click "📥 Process" to process them

### 2. Explore Overview Tab
- See document statistics (chunks, character count)
- Auto-generated summary of all content
- Key insights extracted from documents
- Table of contents for navigation

### 3. Chat Tab
- Ask any question about your documents
- Get document-grounded answers with sources
- View which chunks were used for context
- Expand to see full chunk text

### 4. Tools Tab
- **Mind Map** - Visualize document structure
- **Quiz** - Test knowledge with MCQs (adjust slider for # questions)
- **Flashcards** - Study with generated Q&A pairs (adjust slider for # cards)
- **Audio Script** - Read summary aloud or generate audio

## 🏗️ System Architecture

### Document Processing Pipeline

```
Upload Files
    ↓
Extract Text (PDF/DOCX/TXT)
    ↓
Clean & Normalize
    ↓
Chunk Text (1000 chars, 200 overlap)
    ↓
Store in Session State
    ↓
Ready for Queries
```

### Retrieval System

```
User Query
    ↓
Extract Query Words
    ↓
Score All Chunks (Jaccard + TF-IDF)
    ↓
Select Top-3 Chunks
    ↓
Send to LLM with Context
```

### Analysis Features

```
Input Chunks → GROQ API → JSON Parsing → Formatted Output

Examples:
- Summary: Parse 5 chunks → Generate narrative
- Quiz: Parse 10 chunks → Generate MCQs with explanations
- Flashcards: Parse 8 chunks → Q&A pairs
- Mind Map: Parse 8 chunks → Hierarchical structure
```

## 📊 Key Components

### RAGSystem (rag.py)

```python
rag = RAGSystem(chunk_size=1000, overlap=200)

# Add documents
rag.add_document("file.pdf", "My Document")

# Query with retrieval
result = rag.query("What is the main topic?")

# Generate insights
summary = rag.generate_summary()
insights = rag.generate_key_insights()
quiz = rag.generate_quiz(num_questions=5)
flashcards = rag.generate_flashcards(num_cards=10)
```

### Utility Functions (utils.py)

**DocumentLoader:**
- `extract_text()` - Supports PDF, DOCX, TXT
- Returns text + metadata (page count, char count, etc.)

**TextCleaner:**
- `clean_text()` - Remove extra whitespace
- `extract_sentences()` - Split into sentences
- `extract_key_terms()` - Find top terms by frequency

**TextChunker:**
- `chunk_text()` - Fixed-size chunks with overlap
- `chunk_by_sentences()` - Sentence-based chunks

### Streamlit UI (app.py)

**Sidebar:**
- File uploader with Process/Clear buttons
- Document list with stats
- Easy document management

**Main Tabs:**
- Overview: Summary + Insights + TOC
- Chat: Document Q&A with citations
- Tools: Mind Map, Quiz, Flashcards, Audio

## 🔑 Configuration

### Chunk Settings

Edit in `rag.py`:

```python
chunk_size = 1000      # Characters per chunk
overlap = 200          # Overlap between chunks
top_k = 3              # Chunks to retrieve
```

### Model Settings

Currently using **LLaMA 3.1 70B** via GROQ:

```python
self.model = "llama-3.1-70b-versatile"
```

Change in `rag.py` if needed. Available models:
- `llama-3.1-70b-versatile` (Recommended)
- `llama-3.1-8b-instant`
- `mixtral-8x7b-32768`

### Retrieval Algorithm

Combined scoring in `retrieve()`:

```python
combined_score = 0.6 * jaccard_score + 0.4 * tfidf_score
```

Adjust weights based on your use case.

## ⚙️ Environment Variables

Required in `.env`:

```
GROQ_API_KEY=your_key_here
```

Optional additions:

```
CHUNK_SIZE=1000
OVERLAP=200
TOP_K=3
```

Load with:

```python
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
```

## 📈 Performance Tips

1. **For Large Documents**: Increase `chunk_size` and `overlap`
2. **For Faster Retrieval**: Reduce `chunk_size` or `top_k`
3. **For Better Quality**: Use smaller `overlap` values
4. **For Multiple Uploads**: Process separately then upload

## 🐛 Troubleshooting

### "GROQ_API_KEY not found"
- Verify `.env` file exists in project root
- Check key is set correctly
- Restart Streamlit after creating `.env`

### "ModuleNotFoundError"
- Run `pip install -r requirements.txt`
- Ensure virtual environment is activated

### "No chunks retrieved"
- Query words might not match document content
- Try simpler queries with common terms
- Check document was processed successfully

### "Rate limit exceeded"
- GROQ free tier: 30 requests/min
- Wait before next request or upgrade plan
- Check usage at https://console.groq.com/usage

### Quiz/Flashcards Not Generating
- Document might be too short
- Try uploading longer documents
- Check GROQ API status

## 📋 API Response Formats

### Query Result

```python
{
    "answer": "Clear answer text...",
    "sources": ["Document1.pdf", "Document2.pdf"],
    "citations": [0, 1, 2],  # Chunk indices
    "relevant_chunks": [
        (0, "chunk text", "doc_name"),
        (1, "chunk text", "doc_name"),
        (2, "chunk text", "doc_name")
    ]
}
```

### Quiz Format

```python
[
    {
        "question": "What is...?",
        "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
        "correct_answer": 0,
        "explanation": "The answer is A because..."
    }
]
```

### Flashcard Format

```python
[
    {
        "question": "Define term...",
        "answer": "A term is..."
    }
]
```

## 🚀 Advanced Usage

### Custom Chunking Strategy

```python
# Use sentence-based chunking instead
chunks = TextChunker.chunk_by_sentences(
    text,
    sentences_per_chunk=10,
    overlap_sentences=2
)
```

### Extract Key Terms

```python
from utils import TextCleaner

terms = TextCleaner.extract_key_terms(text, top_n=20)
print(terms)
```

### Batch Processing

```python
rag = RAGSystem()

for doc_path in documents:
    rag.add_document(doc_path, Path(doc_path).name)

# Now use normally
result = rag.query("Your question")
```

## 🔮 Future Enhancements

- [ ] Semantic embeddings (Sentence-Transformers)
- [ ] Vector database integration (Chroma, Pinecone)
- [ ] Web search integration
- [ ] Multi-language support
- [ ] Document comparison
- [ ] Citation bibtex export
- [ ] Custom prompts interface
- [ ] Persistent storage
- [ ] Export to PDF/Markdown
- [ ] Dark mode UI

## 📚 References

- [GROQ API Docs](https://console.groq.com/docs)
- [Streamlit Documentation](https://docs.streamlit.io)
- [LLaMA Models](https://www.llama.com/)
- [RAG Concepts](https://arxiv.org/abs/2005.11401)

## 📄 License

This project is open source for educational purposes.

## 🤝 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review code comments
3. Check GROQ API status
4. Verify environment setup

## 👤 Author

Created as a NotebookLM-inspired RAG system using modern AI APIs.

---

**Made with ❤️ using Streamlit + GROQ API + LLaMA 3.1**
