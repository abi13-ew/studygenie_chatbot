import os
import tempfile
import streamlit as st
import faiss
import numpy as np
import google.generativeai as genai

from sentence_transformers import SentenceTransformer
from transformers import pipeline
from pypdf import PdfReader

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="StudyGenie AI",
    page_icon="📚",
    layout="wide"
)

st.title("📚 StudyGenie AI")

# ==================================================
# SESSION STATE INIT
# ==================================================

defaults = {
    "processed": False,
    "content": "",
    "summary": "",
    "chunks": [],
    "index": None,
    "messages": [],
    "result": ""
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

st.markdown(
    "### Upload your PDF or lecture recording and start learning."
)

# ==================================================
# GEMINI CONFIG
# ==================================================

API_KEY = "Enter your API Key here"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

# ==================================================
# LOAD MODELS
# ==================================================

@st.cache_resource
def load_models():

    embedder = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    transcriber = pipeline(
        "automatic-speech-recognition",
        model="openai/whisper-small"
    )

    return embedder, transcriber


embedder, transcriber = load_models()

# ==================================================
# HELPER FUNCTIONS
# ==================================================

def ask_gemini(prompt):

    response = model.generate_content(prompt)

    return response.text


def chunk_text(text, chunk_size=300):

    words = text.split()

    chunks = []

    for i in range(0, len(words), chunk_size):

        chunk = " ".join(
            words[i:i + chunk_size]
        )

        chunks.append(chunk)

    return chunks


def build_faiss(chunks):

    embeddings = embedder.encode(
        chunks,
        show_progress_bar=False
    )

    embeddings = np.array(
        embeddings
    ).astype("float32")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(
        dimension
    )

    index.add(embeddings)

    return index


def retrieve_context(question, chunks, index):

    q_emb = embedder.encode(
        [question]
    )

    q_emb = np.array(
        q_emb
    ).astype("float32")

    D, I = index.search(
        q_emb,
        k=min(3, len(chunks))
    )

    context = "\n\n".join(
        [chunks[i] for i in I[0]]
    )

    return context


# ==================================================
# CONTENT GENERATORS
# ==================================================

def generate_summary(text):

    prompt = f"""
Summarize the following study material.

Requirements:
- Student friendly
- Bullet points
- Important concepts
- Easy to revise

{text[:12000]}
"""

    return ask_gemini(prompt)


def generate_quiz(text):

    prompt = f"""
Generate 10 MCQs.

Requirements:
- Four options
- Mark correct answer
- Exam style

{text[:12000]}
"""

    return ask_gemini(prompt)


def generate_flashcards(text):

    prompt = f"""
Generate flashcards.

Format:

Q:
A:

{text[:12000]}
"""

    return ask_gemini(prompt)


def generate_exam_prep(text):

    prompt = f"""
Generate:

1. Important Topics

2. 2-Mark Questions

3. 5-Mark Questions

4. Revision Checklist

{text[:12000]}
"""

    return ask_gemini(prompt)


def generate_study_plan(text):

    prompt = f"""
Generate a 7-Day Study Plan.

Include:

Day 1
Day 2
Day 3
Day 4
Day 5
Day 6
Day 7

{text[:12000]}
"""

    return ask_gemini(prompt)


# if st.sidebar.button("➕ New Chat"):

#     keys = [
#         "processed",
#         "content",
#         "summary",
#         "chunks",
#         "index",
#         "messages",
#         "result"
#     ]

#     for key in keys:
#         if key in st.session_state:
#             del st.session_state[key]

#     st.rerun()


# ==================================================
# FILE UPLOAD
# ==================================================

if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = "uploader_1"

# if st.sidebar.button("➕ New Chat"):

#     st.session_state.clear()

#     st.session_state.uploader_key = (
#         f"uploader_{np.random.randint(100000)}"
#     )

#     st.rerun()

uploaded_files = st.file_uploader(
    "Upload PDF(s) or Audio File(s)",
    type=["pdf", "mp3", "wav", "m4a"],
    accept_multiple_files=True,
    key=st.session_state.get("uploader_key", "uploader_1")
)

process_btn = False

if uploaded_files:

    st.success(f"{len(uploaded_files)} file(s) uploaded")

    for file in uploaded_files:
        st.write(f"📄 {file.name}")

    process_btn = st.button(
        "🚀 Process Documents",
        use_container_width=True
    )

# ==================================================
# PROCESS FILE
# ==================================================

if uploaded_files and process_btn:

    combined_content = ""

    with st.spinner(
        "Processing files..."
    ):

        for uploaded_file in uploaded_files:

            # PDF
            if uploaded_file.type == "application/pdf":

                reader = PdfReader(
                    uploaded_file
                )

                for page in reader.pages:

                    page_text = page.extract_text()

                    if page_text:
                        combined_content += (
                            page_text + "\n"
                        )

            # AUDIO
            else:

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".wav"
                ) as tmp:

                    tmp.write(
                        uploaded_file.read()
                    )

                    temp_path = tmp.name

                transcript = transcriber(
                    temp_path
                )

                combined_content += (
                    transcript["text"] + "\n"
                )

                os.remove(temp_path)

    with st.spinner(
        "Building Knowledge Base..."
    ):

        chunks = chunk_text(
            combined_content
        )

        st.session_state.content = (
            combined_content
        )

        st.session_state.chunks = chunks

        st.session_state.index = (
            build_faiss(chunks)
        )

    with st.spinner(
        "Generating Summary..."
    ):

        st.session_state.summary = (
            generate_summary(
                combined_content
            )
        )

    st.session_state.processed = True

    st.success(
        "Documents processed successfully!"
    )
    # ==================================================
    # SUMMARY
    # ==================================================

if st.session_state.processed:

    with st.chat_message(
        "assistant"
    ):

        st.markdown(
            "## 📄 Summary"
        )

        st.write(
            st.session_state.summary
        )

    # ==================================================
# ACTION BUTTONS
# ==================================================

if uploaded_files and st.session_state.processed:

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        if st.button(
            "❓ Quiz",
            use_container_width=True
        ):

            with st.spinner("Generating Quiz..."):

                st.session_state.result = generate_quiz(
                    st.session_state.content
                )

    with col2:

        if st.button(
            "🧠 Flashcards",
            use_container_width=True
        ):

            with st.spinner("Generating Flashcards..."):

                st.session_state.result = generate_flashcards(
                    st.session_state.content
                )

    with col3:

        if st.button(
            "📚 Exam Prep",
            use_container_width=True
        ):

            with st.spinner("Generating Exam Prep..."):

                st.session_state.result = generate_exam_prep(
                    st.session_state.content
                )

    with col4:

        if st.button(
            "📅 Study Plan",
            use_container_width=True
        ):

            with st.spinner("Generating Study Plan..."):

                st.session_state.result = generate_study_plan(
                    st.session_state.content
                )

# ==================================================
# DISPLAY GENERATED CONTENT
# ==================================================

if st.session_state.result:

    with st.chat_message("assistant"):

        st.write(st.session_state.result)

st.divider()

# ==================================================
# CHATBOT
# ==================================================

if st.sidebar.button("➕ New Chat", key="new_chat_btn"):

    st.session_state.clear()

    st.session_state.uploader_key = (
        f"uploader_{np.random.randint(100000)}"
    )

    st.rerun()
