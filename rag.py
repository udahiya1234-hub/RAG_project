"""
Advanced RAG System with NotebookLM-style features.
"""

import os
import re
import json
from typing import List, Dict, Tuple, Optional
from collections import Counter
import numpy as np
from groq import Groq
from sklearn.metrics.pairwise import cosine_similarity
from utils import DocumentLoader, TextCleaner, TextChunker


class RAGSystem:
    """Advanced RAG system with document grounding and analysis."""
    
    def __init__(self, chunk_size: int = 1200, overlap: int = 200):
        """
        Initialize RAG system.
        
        Args:
            chunk_size: Size of text chunks (increased to 1200 for speed)
            overlap: Overlap between chunks
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
        
        # Initialize Groq client without proxy
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment")
        
        self.groq_client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"  # Updated model
        self.vector_matrix = None  # For fast cosine similarity

        
        # Document storage
        self.documents: Dict[str, Dict] = {}  # {doc_name: {text, chunks, metadata}}
        self.all_chunks: List[str] = []  # All chunks from all docs
        self.chunk_to_doc: Dict[int, str] = {}  # Map chunk index to doc name
        self.vectors: Dict[str, np.ndarray] = {}  # Simple TF-IDF vectors
    
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
        
        # Chunk text
        chunks = TextChunker.chunk_text(text, self.chunk_size, self.overlap)
        chunk_texts = [chunk[0] for chunk in chunks]
        
        # Store document
        doc_index = len(self.documents)
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
        self.vectors.clear()
    
    def _simple_tfidf(self, text: str) -> np.ndarray:
        """
        Create simple TF-IDF vector for text.
        
        Args:
            text: Text to vectorize
            
        Returns:
            TF-IDF vector
        """
        # Extract words
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Build vocabulary from all chunks
        all_words = set()
        for chunk in self.all_chunks:
            words_in_chunk = re.findall(r'\b\w+\b', chunk.lower())
            all_words.update(words_in_chunk)
        
        vocabulary = sorted(list(all_words))[:300]  # Limit vocab size
        
        # Count words in this text
        word_counts = Counter(words)
        
        # Create TF vector
        vector = np.zeros(len(vocabulary))
        for i, word in enumerate(vocabulary):
            vector[i] = word_counts.get(word, 0)
        
        # Normalize
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        
        return vector
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors."""
        # Ensure same length
        if len(vec1) != len(vec2):
            max_len = max(len(vec1), len(vec2))
            v1 = np.zeros(max_len)
            v2 = np.zeros(max_len)
            v1[:len(vec1)] = vec1
            v2[:len(vec2)] = vec2
            vec1, vec2 = v1, v2
        
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return float(dot_product / (norm1 * norm2))
    
    def retrieve(self, query: str, top_k: int = 5) -> List[Tuple[int, str, str]]:
        """
        Retrieve most relevant chunks using fast cosine similarity.
        
        Args:
            query: Query text
            top_k: Number of top chunks to return
            
        Returns:
            List of (chunk_index, chunk_text, doc_name) tuples
        """
        if not self.all_chunks:
            return []
        
        # Build vector matrix if not exists
        if self.vector_matrix is None:
            vectors = [self._simple_tfidf(chunk) for chunk in self.all_chunks]
            self.vector_matrix = np.array(vectors)
        
        # Get query vector
        query_vector = self._simple_tfidf(query).reshape(1, -1)
        
        # Fast cosine similarity ranking
        try:
            scores = cosine_similarity(query_vector, self.vector_matrix)[0]
        except:
            # Fallback to manual similarity if sklearn fails
            scores = np.array([self._cosine_similarity(query_vector[0], vec) 
                              for vec in self.vector_matrix])
        
        # Get top-k indices
        top_indices = np.argsort(scores)[-top_k:][::-1]
        
        # Build results
        results = [
            (idx, self.all_chunks[idx], self.chunk_to_doc.get(idx, "Unknown"))
            for idx in top_indices
            if scores[idx] > 0.01  # Threshold to filter irrelevant chunks
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
        """
        Generate a summary of all documents.
        
        Returns:
            Summary text
        """
        if not self.all_chunks:
            return "No documents to summarize."
        
        # Take first few chunks as context
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
        """
        Generate key insights from documents.
        
        Returns:
            List of insights
        """
        if not self.all_chunks:
            return []
        
        # Combine chunks for analysis
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
            
            # Parse JSON response
            response_text = response.choices[0].message.content
            # Extract JSON from response
            json_match = re.search(r'\[.*?\]', response_text, re.DOTALL)
            if json_match:
                insights = json.loads(json_match.group())
                return insights
            return ["Unable to parse insights"]
        except Exception as e:
            return [f"Error generating insights: {str(e)}"]
    
    def generate_mind_map(self) -> str:
        """
        Generate a NotebookLM-quality mind map with 4-level hierarchy.
        
        Returns:
            Mind map text representation
        """
        if not self.all_chunks:
            return "No documents to analyze."
        
        context = "\n\n".join(self.all_chunks[:8])
        
        prompt = """You are a senior knowledge architect specializing in rich hierarchical mind maps.

Rules:
1. Output MUST start with: ### 🌳 Mind Map
2. Use 4 levels:
   - Level 1 → Main Themes
   - Level 2 → Subtopics
   - Level 3 → Key Points
   - Level 4 → Micro-details
3. Use logical grouping, not summaries.
4. Use meaningful emojis for each bullet.
5. NO intro, NO explanation, ONLY the mind map.
6. Keep bullets concise but informative.

Content:
---
{}
---

### 🌳 Mind Map""".format(context)
        
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
        Generate multiple choice quiz questions.
        
        Args:
            num_questions: Number of questions to generate
            
        Returns:
            List of quiz questions with options and answers
        """
        if not self.all_chunks:
            return []
        
        context = "\n\n".join(self.all_chunks[:10])
        
        prompt = f"""Generate {num_questions} multiple choice quiz questions based on this document.
Format as a JSON array of objects with: question, options (array of 4), correct_answer (0-3), explanation

Document:
{context}

Return ONLY valid JSON in this format:
[{{"question": "...", "options": ["A) ...", "B) ...", "C) ...", "D) ..."], "correct_answer": 0, "explanation": "..."}}]"""
        
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
                questions = json.loads(json_match.group())
                return questions
            return []
        except Exception as e:
            return []
    
    def generate_flashcards(self, num_cards: int = 10) -> List[Dict]:
        """
        Generate flashcard questions and answers.
        
        Args:
            num_cards: Number of flashcards to generate
            
        Returns:
            List of flashcards with question/answer
        """
        if not self.all_chunks:
            return []
        
        context = "\n\n".join(self.all_chunks[:8])
        
        prompt = f"""Generate {num_cards} flashcard pairs (Q&A) from this document.
Format as a JSON array with: question, answer

Document:
{context}

Return ONLY valid JSON in this format:
[{{"question": "What is...", "answer": "..."}}]"""
        
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
    
    def generate_audio(self, text: str) -> str:
        """
        Convert text to speech using GROQ API and save as MP3.
        
        Args:
            text: Text to convert to speech
            
        Returns:
            Path to the generated MP3 file
        """
        try:
            speech_file_path = "audio_summary.mp3"
            response = self.groq_client.audio.speech.create(
                model="groq-tts-1",
                voice="alloy",
                input=text,
                format="mp3"
            )
            
            with open(speech_file_path, "wb") as f:
                f.write(response.content)
            
            return speech_file_path
        except Exception as e:
            return f"Error generating audio: {str(e)}"
    
    def generate_audio_script(self) -> str:
        """
        Generate a script for audio summary and convert to MP3.
        
        Returns:
            Path to generated MP3 file or error message
        """
        if not self.all_chunks:
            return "Error: No documents to summarize."
        
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
            return self.generate_audio(script)
        except Exception as e:
            return f"Error generating audio script: {str(e)}"
    
    def generate_table_of_contents(self) -> List[str]:
        """
        Generate table of contents.
        
        Returns:
            List of chapters/sections
        """
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
