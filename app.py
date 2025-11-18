"""
NotebookLM-style RAG Application built with Streamlit
"""

import streamlit as st
import os
from pathlib import Path
from rag import RAGSystem

# Configure Streamlit
st.set_page_config(
    page_title="NotebookLM RAG",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful UI with light mode and dark mode support
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .sub-header {
        font-size: 1.2em;
        color: #666;
        margin-bottom: 20px;
    }
    .doc-card {
        padding: 15px;
        border-radius: 8px;
        background-color: #f0f2f6;
        margin: 10px 0;
        border-left: 4px solid #0066cc;
        color: #000000 !important;
    }
    .doc-card p, .doc-card div, .doc-card span {
        color: #000000 !important;
    }
    .insight-box {
        padding: 10px;
        border-radius: 5px;
        background-color: #e3f2fd;
        margin: 5px 0;
        border-left: 3px solid #2196F3;
        color: #000000 !important;
    }
    .insight-box p, .insight-box div, .insight-box span {
        color: #000000 !important;
    }
    
    /* ==================== LIGHT MODE TEXT FIX ====================*/
    [data-theme="light"] body,
    [data-theme="light"] p,
    [data-theme="light"] h1,
    [data-theme="light"] h2,
    [data-theme="light"] h3,
    [data-theme="light"] h4,
    [data-theme="light"] h5,
    [data-theme="light"] h6,
    [data-theme="light"] div,
    [data-theme="light"] span,
    [data-theme="light"] li,
    [data-theme="light"] label,
    [data-theme="light"] .stMarkdown,
    [data-theme="light"] .stText,
    [data-theme="light"] .stWrite {
        color: #000000 !important;
    }
    
    [data-theme="light"] input,
    [data-theme="light"] textarea,
    [data-theme="light"] select,
    [data-theme="light"] .stTextInput input,
    [data-theme="light"] .stTextArea textarea,
    [data-theme="light"] .stSelectbox select {
        color: #000000 !important;
        background-color: #f7f7f7 !important;
        border-color: #cccccc !important;
    }
    
    [data-theme="light"] .stButton button {
        color: #ffffff !important;
        background-color: #0066cc !important;
    }
    
    [data-theme="light"] [data-testid="stFileUploader"] {
        color: #000000 !important;
    }
    
    [data-theme="light"] [data-testid="stFileUploader"] label,
    [data-theme="light"] [data-testid="stFileUploader"] div {
        color: #000000 !important;
    }
    
    [data-theme="light"] div.stAlert {
        color: #000000 !important;
        background-color: #f0f0f0 !important;
        border-color: #999999 !important;
    }
    
    /* ==================== DARK MODE TEXT FIX ====================*/
    body, .stMarkdown, .stText, .stWrite, p {
        color: #e6e6e6 !important;
    }
    
    /* File uploader dark mode fix */
    [data-testid="stFileUploader"] {
        color: #e6e6e6 !important;
    }
    [data-testid="stFileUploader"] label, [data-testid="stFileUploader"] div {
        color: #e6e6e6 !important;
    }
    
    /* Alert and message styling */
    div.stAlert {
        color: #e6e6e6 !important;
        border-color: #555 !important;
    }
    div[data-testid="stAlert"] {
        color: #e6e6e6 !important;
    }
    
    /* Input fields dark mode fix */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        background-color: #262730 !important;
        color: #e6e6e6 !important;
        border-color: #555 !important;
    }
    .stTextInput input::placeholder, .stTextArea textarea::placeholder {
        color: #999 !important;
    }
    
    /* General text visibility */
    label, .stLabel {
        color: #e6e6e6 !important;
    }
    
    /* Loading spinner and animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    .stSpinner {
        animation: fadeIn 0.3s ease-in;
    }
    
    /* Success and error boxes with better contrast */
    div[class*="success"] {
        background-color: #0f3d1f !important;
        border-color: #2ecc71 !important;
    }
    div[class*="error"] {
        background-color: #3d0f0f !important;
        border-color: #e74c3c !important;
    }
    div[class*="warning"] {
        background-color: #3d2f0f !important;
        border-color: #f39c12 !important;
    }
    div[class*="info"] {
        background-color: #0f1f3d !important;
        border-color: #3498db !important;
    }
    
    /* Force visibility for insight boxes and document cards */
    .insight-box {
        background-color: #e3f2fd !important;
        color: #000000 !important;
    }
    .doc-card {
        background-color: #f0f2f6 !important;
        color: #000000 !important;
    }
    
    /* Light mode specific fixes for all containers */
    [data-theme="light"] .insight-box,
    [data-theme="light"] .doc-card {
        color: #000000 !important;
        background-color: #f0f2f6 !important;
    }
    
    [data-theme="light"] .insight-box p,
    [data-theme="light"] .insight-box div,
    [data-theme="light"] .doc-card p,
    [data-theme="light"] .doc-card div {
        color: #000000 !important;
    }
    
    /* Force text visibility in all metric/stat boxes */
    [data-theme="light"] [data-testid="metric-container"],
    [data-theme="light"] [class*="metric"],
    [data-theme="light"] [class*="stat"] {
        color: #000000 !important;
    }
    
    /* Expander visibility */
    [data-theme="light"] [data-testid="stExpander"],
    [data-theme="light"] details summary {
        color: #000000 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "rag_system" not in st.session_state:
    try:
        st.session_state.rag_system = RAGSystem()
    except ValueError as e:
        st.error(f"❌ Error: {str(e)}")
        st.stop()

if "documents_loaded" not in st.session_state:
    st.session_state.documents_loaded = False

if "current_tab" not in st.session_state:
    st.session_state.current_tab = "Overview"

# Header
st.markdown('<div class="main-header">📚 NotebookLM-Style RAG Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Upload documents and explore with AI-powered tools</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📤 Document Manager")
    
    # Document upload section
    uploaded_files = st.file_uploader(
        "Upload documents (PDF, DOCX, TXT)",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        key="file_uploader"
    )
    
    if uploaded_files:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📥 Process", use_container_width=True, key="process_btn"):
                with st.spinner("Processing documents..."):
                    try:
                        st.session_state.rag_system.clear()
                        
                        for uploaded_file in uploaded_files:
                            file_path = f"temp_{uploaded_file.name}"
                            with open(file_path, "wb") as f:
                                f.write(uploaded_file.getbuffer())
                            
                            result = st.session_state.rag_system.add_document(file_path, uploaded_file.name)
                            os.remove(file_path)
                        
                        st.session_state.documents_loaded = True
                        st.success(f"✅ Processed {len(uploaded_files)} document(s)!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
        
        with col2:
            if st.button("🗑️ Clear", use_container_width=True, key="clear_btn"):
                st.session_state.rag_system.clear()
                st.session_state.documents_loaded = False
                st.rerun()
    
    # Document list
    if st.session_state.documents_loaded:
        st.divider()
        st.subheader("📄 Loaded Documents")
        stats = st.session_state.rag_system.get_stats()
        
        for doc in stats["documents"]:
            with st.container():
                st.markdown(f"""
                <div class="doc-card">
                    <strong>{doc['name']}</strong><br/>
                    Chunks: {doc['chunks']} | Size: {doc['characters']:,} chars
                </div>
                """, unsafe_allow_html=True)

# Main content
if st.session_state.documents_loaded:
    # Tab navigation
    tab1, tab2, tab3 = st.tabs(["📖 Overview", "💬 Chat", "🛠️ Tools"])
    
    # === OVERVIEW TAB ===
    with tab1:
        st.header("Document Overview")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            stats = st.session_state.rag_system.get_stats()
            st.metric("📊 Total Documents", stats["total_documents"])
        with col2:
            st.metric("📝 Total Chunks", stats["total_chunks"])
        with col3:
            st.metric("📄 Total Characters", f"{stats['total_characters']:,}")
        
        st.divider()
        
        # Summary
        st.subheader("📋 Summary")
        with st.spinner("Generating summary..."):
            summary = st.session_state.rag_system.generate_summary()
            st.write(summary)
        
        st.divider()
        
        # Key Insights
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.subheader("💡 Key Insights")
            with st.spinner("Extracting key insights..."):
                insights = st.session_state.rag_system.generate_key_insights()
                for i, insight in enumerate(insights, 1):
                    st.markdown(f"""
                    <div class="insight-box">
                    <strong>{i}.</strong> {insight}
                    </div>
                    """, unsafe_allow_html=True)
        
        with col_right:
            st.subheader("📑 Table of Contents")
            with st.spinner("Generating table of contents..."):
                toc = st.session_state.rag_system.generate_table_of_contents()
                for section in toc:
                    st.write(f"• {section}")
    
    # === CHAT TAB ===
    with tab2:
        st.header("💬 Document-Grounded Chat")
        
        # Query input
        query = st.text_input(
            "Ask a question about your documents:",
            placeholder="What are the main topics covered?"
        )
        
        if query:
            with st.spinner("🤔 Searching and generating answer..."):
                try:
                    result = st.session_state.rag_system.query(query)
                    
                    # Display answer
                    st.markdown("### 📝 Answer")
                    st.write(result["answer"])
                    
                    # Display sources
                    if result["sources"]:
                        st.markdown("### 📌 Sources")
                        sources_text = ", ".join(result["sources"])
                        st.info(f"✓ Based on: {sources_text}")
                    
                    # Display relevant chunks
                    with st.expander("📖 View Relevant Chunks"):
                        for idx, (chunk_idx, chunk_text, doc_name) in enumerate(result["relevant_chunks"], 1):
                            st.markdown(f"**Chunk {idx}** | {doc_name}")
                            st.markdown(f"> {chunk_text[:400]}..." if len(chunk_text) > 400 else f"> {chunk_text}")
                            st.divider()
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    # === TOOLS TAB ===
    with tab3:
        st.header("🛠️ Learning Tools")
        
        tool_col1, tool_col2 = st.columns(2)
        
        # Mind Map
        with tool_col1:
            st.subheader("🧠 Mind Map")
            if st.button("Generate Mind Map", key="mindmap_btn"):
                with st.spinner("🔄 Creating mind map..."):
                    try:
                        mindmap = st.session_state.rag_system.generate_mind_map()
                        st.success("✅ Mind map generated!")
                        st.code(mindmap, language="text")
                    except Exception as e:
                        st.error(f"❌ Error generating mind map: {str(e)}")
        
        # Audio Summary
        with tool_col2:
            st.subheader("🎤 Audio Summary")
            if st.button("Generate Audio", key="audio_btn"):
                with st.spinner("🔄 Creating audio..."):
                    try:
                        audio_path = st.session_state.rag_system.generate_audio_script()
                        if audio_path.startswith("Error"):
                            st.error(f"❌ {audio_path}")
                        else:
                            st.success("✅ Audio generated!")
                            with open(audio_path, "rb") as f:
                                st.audio(f, format="audio/mp3")
                    except Exception as e:
                        st.error(f"❌ Error generating audio: {str(e)}")
        
        st.divider()
        
        # Quiz
        st.subheader("❓ Quiz Generator")
        num_questions = st.slider("Number of questions:", 3, 10, 5, key="quiz_slider")
        if st.button("Generate Quiz", key="quiz_btn"):
            with st.spinner("🔄 Creating quiz..."):
                try:
                    quiz = st.session_state.rag_system.generate_quiz(num_questions)
                    
                    if quiz:
                        st.success(f"✅ Generated {len(quiz)} quiz questions!")
                        for idx, q in enumerate(quiz, 1):
                            with st.container():
                                st.markdown(f"### Question {idx}")
                                st.write(q.get("question", ""))
                                
                                options = q.get("options", [])
                                correct = q.get("correct_answer", 0)
                                explanation = q.get("explanation", "")
                                
                                selected = st.radio(
                                    "Select your answer:",
                                    options,
                                    key=f"quiz_q{idx}"
                                )
                                
                                if selected == options[correct]:
                                    st.success("✅ Correct!")
                                else:
                                    st.error(f"❌ Incorrect. Correct answer: {options[correct]}")
                                
                                st.info(f"**Explanation:** {explanation}")
                                st.divider()
                    else:
                        st.warning("⚠️ Could not generate quiz questions")
                except Exception as e:
                    st.error(f"❌ Error generating quiz: {str(e)}")
        
        st.divider()
        
        # Flashcards
        st.subheader("📇 Flashcard Generator")
        num_cards = st.slider("Number of flashcards:", 5, 20, 10, key="flashcard_slider")
        if st.button("Generate Flashcards", key="flashcard_btn"):
            with st.spinner("🔄 Creating flashcards..."):
                try:
                    flashcards = st.session_state.rag_system.generate_flashcards(num_cards)
                    
                    if flashcards:
                        st.success(f"✅ Generated {len(flashcards)} flashcards!")
                        for idx, card in enumerate(flashcards, 1):
                            col_q, col_a = st.columns([1, 1])
                            
                            with col_q:
                                st.markdown(f"**Card {idx} - Question**")
                                st.write(card.get("question", ""))
                            
                            with col_a:
                                st.markdown(f"**Card {idx} - Answer**")
                                with st.expander("Show Answer"):
                                    st.write(card.get("answer", ""))
                    else:
                        st.warning("⚠️ Could not generate flashcards")
                except Exception as e:
                    st.error(f"❌ Error generating flashcards: {str(e)}")

else:
    # No documents loaded
    st.info("👉 Upload and process documents in the sidebar to begin")
    
    with st.container():
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 💬 Chat with Docs")
            st.write("Ask questions and get document-grounded answers")
        
        with col2:
            st.markdown("### 🧠 Mind Maps")
            st.write("Visualize document structure")
        
        with col3:
            st.markdown("### 📇 Flashcards & Quiz")
            st.write("Test your knowledge")

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: #999; font-size: 0.9em; margin-top: 20px;'>
    🚀 Powered by GROQ API | Powered by Streamlit<br/>
    NotebookLM-style RAG System for Document Analysis
    </div>
""", unsafe_allow_html=True)
