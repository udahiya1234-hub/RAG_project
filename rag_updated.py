"""
Advanced RAG System with NotebookLM-style features and Google TTS.
"""
from dotenv import load_dotenv
import os
load_dotenv()

import os
import re
import json
import base64
import requests
from typing import List, Dict, Tuple, Optional
from collections import Counter
import numpy as np
from groq import Groq
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils import DocumentLoader, TextCleaner, TextChunker


class RAGSystem:
    """Advanced RAG system with document grounding and analysis."""
    
    def __init__(self, chunk_size: int = 1000, overlap: int = 200):
        """
        Initialize RAG system.
        
        Args:
            chunk_size: Size of text chunks (1000 chars for performance)
            overlap: Overlap between chunks (200 chars)
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
        
        # Initialize Groq client
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment")
        
        self.groq_client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"
        
        # Google API key for TTS
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        
        # Document storage
        self.documents: Dict[str, Dict] = {}
        self.all_chunks: List[str] = []
        self.chunk_to_doc: Dict[int, str] = {}
        
        # TF-IDF vectorizer for fast retrieval (cached)
        self.tfidf_vectorizer = None
        self.tfidf_matrix = None
        
        # Cache for frequently used results
        self._cache = {}
    
    def add_document(self, file_path: str, doc_name: str) -> Dict:
        """
        Add a document to the RAG system.
        
        Args:
            file_path: Path to document file
            doc_name: Name of document
            
        Returns:
            Dictionary with document info
        """
        # Extract text
        text, metadata = DocumentLoader.extract_text(file_path)
        
        if not text.strip():
            raise ValueError("Document is empty or could not be read")
        
        # Chunk text with specified size and overlap
        chunks = TextChunker.chunk_text(text, self.chunk_size, self.overlap)
        chunk_texts = [chunk[0] for chunk in chunks]
        
        # Store document
        self.documents[doc_name] = {
            "text": text,
            "chunks": chunk_texts,
            "metadata": metadata,
            "char_count": len(text),
            "chunk_count": len(chunk_texts)
        }
        
        # Update chunk mapping
        start_idx = len(self.all_chunks)
        for i, chunk in enumerate(chunk_texts):
            self.all_chunks.append(chunk)
            self.chunk_to_doc[start_idx + i] = doc_name
        
        # Clear cached vectors
        self.tfidf_matrix = None
        self.tfidf_vectorizer = None
        self._cache.clear()
        
        return {
            "doc_name": doc_name,
            "status": "success",
            "chunks_created": len(chunk_texts),
            "char_count": len(text),
            "metadata": metadata
        }
    
    def clear(self):
        """Clear all documents and data."""
        self.documents.clear()
        self.all_chunks.clear()
        self.chunk_to_doc.clear()
        self.tfidf_matrix = None
        self.tfidf_vectorizer = None
        self._cache.clear()
    
    def _get_tfidf_matrix(self):
        """Build TF-IDF matrix with caching."""
        if self.tfidf_matrix is None and len(self.all_chunks) > 0:
            self.tfidf_vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
            self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.all_chunks)
        return self.tfidf_matrix, self.tfidf_vectorizer
    
    def retrieve(self, query: str, top_k: int = 5) -> List[Tuple[int, str, str]]:
        """
        Retrieve most relevant chunks using TF-IDF and cosine similarity.
        
        Args:
            query: Query text
            top_k: Number of top chunks to return
            
        Returns:
            List of (chunk_index, chunk_text, doc_name) tuples
        """
        if not self.all_chunks:
            return []
        
        # Get or build TF-IDF matrix
        matrix, vectorizer = self._get_tfidf_matrix()
        
        if matrix is None:
            return []
        
        # Vectorize query
        query_vector = vectorizer.transform([query])
        
        # Compute cosine similarity
        similarities = cosine_similarity(query_vector, matrix).flatten()
        
        # Get top-k indices
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        # Build results
        results = [
            (idx, self.all_chunks[idx], self.chunk_to_doc.get(idx, "Unknown"))
            for idx in top_indices
            if similarities[idx] > 0.0
        ]
        
        return results
    
    def query(self, query: str, top_k: int = 3) -> Dict:
        """
        Answer a query using RAG.
        
        Args:
            query: User question
            top_k: Number of chunks to retrieve
            
        Returns:
            Dictionary with answer and metadata
        """
        # Retrieve relevant chunks
        relevant_chunks = self.retrieve(query, top_k=top_k)
        
        if not relevant_chunks:
            return {
                "answer": "I couldn't find relevant information in the documents.",
                "sources": [],
                "citations": []
            }
        
        # Build context
        chunk_indices = [idx for idx, _, _ in relevant_chunks]
        chunk_texts = [text for _, text, _ in relevant_chunks]
        doc_names = [doc for _, _, doc in relevant_chunks]
        
        context = "\n\n".join([
            f"[Source: {doc_names[i]}, Chunk {chunk_indices[i]+1}]\n{text}"
            for i, text in enumerate(chunk_texts)
        ])
        
        # Build prompt
        system_prompt = """You are a helpful assistant that answers questions based on provided documents.
You MUST ONLY use information from the provided document chunks.
If the answer is not in the documents, say so clearly.
Always be accurate and provide clear, concise answers.
Cite your sources when making claims."""
        
        user_prompt = f"""Answer this question based ONLY on the provided document chunks: {query}

DOCUMENT CHUNKS:
{context}

Provide a clear, concise answer."""
        
        try:
            response = self.groq_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            answer = response.choices[0].message.content
            
            return {
                "answer": answer,
                "sources": list(set(doc_names)),
                "citations": chunk_indices,
                "relevant_chunks": relevant_chunks
            }
            
        except Exception as e:
            raise Exception(f"Error calling GROQ API: {str(e)}")
    
    def generate_summary(self) -> str:
        """Generate a summary of all documents."""
        if not self.all_chunks:
            return "No documents to summarize."
        
        context = "\n\n".join(self.all_chunks[:5])
        
        prompt = f"""Provide a concise summary (2-3 paragraphs) of the following document excerpt:

{context}

Focus on the main ideas and key points."""
        
        try:
            response = self.groq_client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=400
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating summary: {str(e)}"
    
    def generate_key_insights(self) -> List[str]:
        """Generate key insights from documents."""
        if not self.all_chunks:
            return []
        
        context = "\n\n".join(self.all_chunks[:10])
        
        prompt = f"""Extract 5 key insights from this document text. 
Format as a JSON list of strings.

Document:
{context}

Return ONLY valid JSON in this format:
["insight 1", "insight 2", "insight 3", "insight 4", "insight 5"]"""
        
        try:
            response = self.groq_client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=500
            )
            
            response_text = response.choices[0].message.content
            json_match = re.search(r'\[.*?\]', response_text, re.DOTALL)
            if json_match:
                insights = json.loads(json_match.group())
                return insights
            return ["Unable to parse insights"]
        except Exception as e:
            return [f"Error generating insights: {str(e)}"]
    
    def generate_mind_map(self) -> str:
        """
        Generate a NotebookLM-style mind map with tree structure.
        
        Returns:
            ASCII tree mind map representation
        """
        if not self.all_chunks:
            return "No documents to analyze."
        
        context = "\n\n".join(self.all_chunks[:10])
        
        prompt = f"""Analyze this content and create a hierarchical mind map with ASCII tree format.

Requirements:
- Use ASCII tree structure with ├─, └─, and │ characters
- 3-4 levels of hierarchy
- 8-12 total nodes
- Be logical and clear
- Clean markdown/ASCII format

Content:
{context}

Output format example:
ROOT TOPIC
 ├─ Key Idea 1
 │   ├─ Subpoint A
 │   └─ Subpoint B
 ├─ Key Idea 2
 │   ├─ Subpoint C
 │   └─ Subpoint D
 └─ Conclusion

Output ONLY the mind map, no explanation."""
        
        try:
            response = self.groq_client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=800
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating mind map: {str(e)}"
    
    def generate_quiz(self, num_questions: int = 5) -> List[Dict]:
        """
        Generate multiple choice quiz questions with retry logic.
        
        Args:
            num_questions: Number of questions to generate
            
        Returns:
            List of quiz questions with options and answers
        """
        if not self.all_chunks:
            return []
        
        context = "\n\n".join(self.all_chunks[:10])
        
        prompt = f"""Generate {num_questions} multiple choice quiz questions based on this document.
Return ONLY valid JSON, no other text.

Document:
{context}

JSON format (MUST be valid):
[
  {{"question": "What is...", "options": ["A", "B", "C", "D"], "answer": "A"}},
  {{"question": "How does...", "options": ["A", "B", "C", "D"], "answer": "B"}}
]"""
        
        max_retries = 2
        for attempt in range(max_retries):
            try:
                response = self.groq_client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.5,
                    max_tokens=1500
                )
                
                response_text = response.choices[0].message.content.strip()
                
                # Extract JSON
                json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
                if json_match:
                    json_str = json_match.group()
                    # Validate JSON
                    questions = json.loads(json_str)
                    
                    # Validate structure
                    if isinstance(questions, list) and len(questions) > 0:
                        for q in questions:
                            if not all(k in q for k in ["question", "options", "answer"]):
                                raise ValueError("Invalid question structure")
                        return questions
            except (json.JSONDecodeError, ValueError) as e:
                if attempt == max_retries - 1:
                    return [{
                        "question": "Sample Question",
                        "options": ["Option A", "Option B", "Option C", "Option D"],
                        "answer": "Option A"
                    }]
                continue
        
        return []
    
    def generate_flashcards(self, num_cards: int = 10) -> List[Dict]:
        """Generate flashcard questions and answers."""
        if not self.all_chunks:
            return []
        
        context = "\n\n".join(self.all_chunks[:8])
        
        prompt = f"""Generate {num_cards} flashcard pairs (Q&A) from this document.
Return ONLY valid JSON, no other text.

Document:
{context}

JSON format (MUST be valid):
[
  {{"question": "What is...", "answer": "..."}},
  {{"question": "How does...", "answer": "..."}}
]"""
        
        try:
            response = self.groq_client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1500
            )
            
            response_text = response.choices[0].message.content
            json_match = re.search(r'\[.*?\]', response_text, re.DOTALL)
            if json_match:
                flashcards = json.loads(json_match.group())
                return flashcards
            return []
        except Exception as e:
            return []
    
    def synthesize_audio(self, text: str) -> bytes:
        """
        Convert text to speech using Google Text-to-Speech API.
        
        Args:
            text: Text to convert to speech
            
        Returns:
            MP3 audio bytes
        """
        if not self.google_api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment")
        
        url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={self.google_api_key}"
        
        payload = {
            "input": {
                "text": text
            },
            "voice": {
                "languageCode": "en-US",
                "name": "en-US-Neural2-F"
            },
            "audioConfig": {
                "audioEncoding": "MP3"
            }
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            
            result = response.json()
            audio_base64 = result.get("audioContent")
            
            if audio_base64:
                audio_bytes = base64.b64decode(audio_base64)
                return audio_bytes
            else:
                raise ValueError("No audio content in response")
        except Exception as e:
            raise Exception(f"Error generating audio: {str(e)}")
    
    def generate_audio_script(self) -> Tuple[str, bytes]:
        """
        Generate an audio script and convert to MP3.
        
        Returns:
            Tuple of (script_text, audio_bytes)
        """
        if not self.all_chunks:
            raise ValueError("No documents to summarize.")
        
        context = "\n\n".join(self.all_chunks[:5])
        
        prompt = f"""Create a 2-3 minute audio script summarizing this document.
Make it conversational and engaging, as if explaining to a friend.
Include main points and key takeaways.

Document:
{context}

Write the script directly without any formatting."""
        
        try:
            response = self.groq_client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=600
            )
            
            script = response.choices[0].message.content
            
            # Generate audio
            audio_bytes = self.synthesize_audio(script)
            
            return script, audio_bytes
        except Exception as e:
            raise Exception(f"Error generating audio script: {str(e)}")
    
    def generate_table_of_contents(self) -> List[str]:
        """Generate table of contents."""
        if not self.all_chunks:
            return []
        
        context = "\n\n".join(self.all_chunks[:6])
        
        prompt = f"""Generate a table of contents with 5-8 main sections from this document.
Return as a JSON array of strings with section titles.

Document:
{context}

Return ONLY valid JSON in this format:
["Section 1", "Section 2", "Section 3"]"""
        
        try:
            response = self.groq_client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=300
            )
            
            response_text = response.choices[0].message.content
            json_match = re.search(r'\[.*?\]', response_text, re.DOTALL)
            if json_match:
                toc = json.loads(json_match.group())
                return toc
            return []
        except Exception as e:
            return []
    
    def get_stats(self) -> Dict:
        """Get statistics about loaded documents."""
        total_chunks = len(self.all_chunks)
        total_chars = sum(len(chunk) for chunk in self.all_chunks)
        
        return {
            "total_documents": len(self.documents),
            "total_chunks": total_chunks,
            "total_characters": total_chars,
            "documents": [
                {
                    "name": name,
                    "chunks": doc["chunk_count"],
                    "characters": doc["char_count"]
                }
                for name, doc in self.documents.items()
            ]
        }
