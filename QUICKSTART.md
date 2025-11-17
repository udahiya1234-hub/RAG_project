# 🚀 Quick Reference Guide

## Installation & Setup (5 minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env from template
cp .env.example .env

# 3. Edit .env - add your GROQ API key
# Get key from: https://console.groq.com/keys

# 4. Run the app
streamlit run app.py

# 5. Open browser to http://localhost:8501
```

## File Structure

```
RAG_notebook/
├── app.py              ← Main UI (run this)
├── rag.py              ← RAG engine (all logic)
├── utils.py            ← Helpers (text processing)
├── requirements.txt    ← Install dependencies
├── .env.example        ← Copy to .env and add key
├── .env                ← Your actual API key (create)
├── README.md           ← Full documentation
├── FEATURES.md         ← Feature list
└── setup.py            ← Setup checker
```

## Usage Workflow

### 1️⃣ Upload Documents
```
Sidebar → File Uploader → Select 1+ files (PDF/DOCX/TXT) → Process
```

### 2️⃣ Explore Overview Tab
```
📖 Overview Tab → Summary + Insights + Table of Contents
```

### 3️⃣ Ask Questions (Chat Tab)
```
💬 Chat Tab → Type question → Get answer with sources → View chunks
```

### 4️⃣ Use Tools (Tools Tab)
```
🛠️ Tools Tab → Choose: Mind Map / Quiz / Flashcards / Audio Script
```

## Common Commands

```bash
# Start app
streamlit run app.py

# Install packages
pip install -r requirements.txt

# Check setup
python setup.py

# Clear Streamlit cache
streamlit cache clear

# Run with specific port
streamlit run app.py --server.port 8502

# Run in headless mode
streamlit run app.py --headless
```

## Configuration Tips

### Adjust Chunk Size
Edit in `rag.py`:
```python
RAGSystem(chunk_size=1000, overlap=200)
```
- Larger = more context per chunk, fewer chunks
- Smaller = less context, more chunks

### Change Model
Edit in `rag.py`:
```python
self.model = "llama-3.1-70b-versatile"  # Default (fast)
self.model = "llama-3.1-8b-instant"     # Smaller/faster
self.model = "mixtral-8x7b-32768"       # Alternative
```

### Adjust Retrieval
Edit in `rag.py`:
```python
# Retrieval weighting
combined_score = 0.6 * jaccard_score + 0.4 * tfidf_score
# More keyword-based: 0.8 * jaccard + 0.2 * tfidf
# More semantic: 0.3 * jaccard + 0.7 * tfidf
```

## Features at a Glance

| Feature | Location | Input | Output |
|---------|----------|-------|--------|
| 📖 Summary | Overview | All chunks | Text summary |
| 💡 Insights | Overview | All chunks | 5 key points |
| 📑 TOC | Overview | All chunks | Section list |
| 💬 Q&A | Chat | Question | Answer + sources |
| 🧠 Mind Map | Tools | All chunks | Hierarchical text |
| ❓ Quiz | Tools | Slider (3-10) | MCQs with answers |
| 📇 Flashcards | Tools | Slider (5-20) | Q&A pairs |
| 🎤 Audio Script | Tools | All chunks | 2-3 min script |

## Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| "API Key not found" | Verify .env exists and has GROQ_API_KEY |
| "ModuleNotFoundError" | Run: `pip install -r requirements.txt` |
| "Page not loading" | Check server is running, try localhost:8501 |
| "Rate limit exceeded" | Wait 2 mins or upgrade GROQ plan |
| "No chunks retrieved" | Try simpler query or upload larger docs |
| "Quiz won't generate" | Document might be too short |

## Code Snippets

### Use RAG Programmatically
```python
from rag import RAGSystem

# Initialize
rag = RAGSystem()

# Add documents
rag.add_document("document.pdf", "My Doc")

# Query
result = rag.query("Your question")
print(result["answer"])
print(result["sources"])

# Generate tools
summary = rag.generate_summary()
quiz = rag.generate_quiz(5)
flashcards = rag.generate_flashcards(10)
```

### Extract from Utilities
```python
from utils import DocumentLoader, TextCleaner, TextChunker

# Extract text
text, metadata = DocumentLoader.extract_text("file.pdf")

# Clean text
clean = TextCleaner.clean_text(text)

# Get sentences
sentences = TextCleaner.extract_sentences(text)

# Get key terms
terms = TextCleaner.extract_key_terms(text, top_n=10)

# Chunk text
chunks = TextChunker.chunk_text(text, chunk_size=1000, overlap=200)
```

## API Reference

### RAGSystem Methods

```python
rag = RAGSystem(chunk_size=1000, overlap=200)

# Document management
rag.add_document(file_path, doc_name)     # → Dict
rag.clear()                                # → None

# Query & retrieval
rag.query(query, top_k=3)                 # → Dict
rag.retrieve(query, top_k=3)              # → List

# Analysis tools
rag.generate_summary()                    # → str
rag.generate_key_insights()               # → List[str]
rag.generate_mind_map()                   # → str
rag.generate_quiz(num_questions=5)        # → List[Dict]
rag.generate_flashcards(num_cards=10)     # → List[Dict]
rag.generate_audio_script()               # → str
rag.generate_table_of_contents()          # → List[str]

# Utilities
rag.get_stats()                           # → Dict
```

### Response Formats

**Query Response:**
```python
{
    "answer": "...",
    "sources": ["doc1", "doc2"],
    "citations": [0, 1, 2],
    "relevant_chunks": [(idx, text, doc), ...]
}
```

**Quiz Question:**
```python
{
    "question": "What is...?",
    "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
    "correct_answer": 0,
    "explanation": "..."
}
```

**Flashcard:**
```python
{
    "question": "Define...",
    "answer": "..."
}
```

## Performance Benchmarks

- **Query time**: 2-4 seconds
- **Summary generation**: 2-3 seconds
- **Quiz generation (5 Q)**: 3-5 seconds
- **Flashcards (10 cards)**: 3-5 seconds
- **Mind map generation**: 3-4 seconds

## Limits & Constraints

- **File types**: PDF, DOCX, TXT only
- **Max file size**: Limited by RAM
- **Max questions**: 10 (quiz slider)
- **Max flashcards**: 20 (flashcard slider)
- **API rate limit**: 30 req/min (free tier)
- **Response time**: ~30s max (API timeout)

## Environment Variables

### Required
```
GROQ_API_KEY=your_actual_key
```

### Optional
```
CHUNK_SIZE=1000
OVERLAP=200
TOP_K=3
```

Load with:
```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
```

## Useful Links

- [GROQ API](https://console.groq.com)
- [GROQ Docs](https://console.groq.com/docs)
- [Streamlit Docs](https://docs.streamlit.io)
- [LLaMA Info](https://www.llama.com)
- [RAG Paper](https://arxiv.org/abs/2005.11401)

## Support Resources

1. **Check Docs**: README.md, FEATURES.md
2. **Check Code**: Comments in rag.py, app.py, utils.py
3. **Check Status**: [GROQ Status](https://status.groq.com)
4. **Check Logs**: Streamlit terminal output

## Tips & Tricks

### ✨ For Best Results
- Use documents with clear structure
- Ask specific questions
- Keep documents under 50MB
- Use descriptive document names
- Upload related documents together

### ⚡ For Speed
- Smaller documents process faster
- Fewer chunks = faster retrieval
- Simpler queries = faster answers
- Use 8B model for speed, 70B for quality

### 🎯 For Accuracy
- Provide more context in questions
- Use longer documents for analysis
- View chunks to verify sources
- Test with different query wordings

## Keyboard Shortcuts (Streamlit)

- `C`: Clear cache
- `R`: Rerun app
- `Shift+P`: Settings menu
- `Ctrl+/`: Toggle sidebar

## File Size Recommendations

| Document Type | Recommended Size |
|---------------|-----------------|
| Textbook | 10-50 MB |
| Paper | 1-10 MB |
| Article | 0.5-5 MB |
| Notes | 0.1-1 MB |
| Multiple docs | 50-200 MB total |

## Next Steps After Setup

1. ✅ Run: `streamlit run app.py`
2. ✅ Upload a test document
3. ✅ Ask a question in Chat tab
4. ✅ Try a tool (Quiz/Flashcards)
5. ✅ Explore Overview tab
6. ✅ Customize settings (optional)

---

**Quick Start Complete!** 🎉

Need help? Check README.md for detailed documentation.
