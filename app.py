# ============================================================
# AI-POWERED GROKPEDIA-STYLE ENCYCLOPEDIA WITH QUESTION ANSWERING
# + DOCUMENT UPLOAD KNOWLEDGE LIBRARY (DOCX + PDF + TXT)
# REBBE SECURITY (STREAMLIT CLOUD)
# ============================================================
# The AI now:
# - Answers questions AND writes encyclopedia-style responses
# - Uses previously generated articles
# - Uses uploaded documents (letters, talks, PDFs, etc.) as sources
# ============================================================

import streamlit as st
from openai import OpenAI

# Libraries for reading uploaded files
from io import BytesIO

try:
    import docx  # python-docx
except Exception:
    docx = None

try:
    import PyPDF2
except Exception:
    PyPDF2 = None

# ------------------------------
# Page Setup
# ------------------------------
st.set_page_config(page_title="Rebbe Security Encyclopedia", layout="wide")
st.title("Rebbe Security Encyclopedia")
st.markdown(
    "This AI answers questions and generates encyclopedia-style articles based only on authentic source material — including your uploaded documents and site content."
)

# ------------------------------
# READ API KEY FROM STREAMLIT SECRETS
# ------------------------------
if "OPENAI_API_KEY" not in st.secrets:
    st.error(
        "OpenAI API key not found.\n\n"
        "You are using Streamlit Cloud. Add your key in **Settings → Secrets**.\n\n"
        "Add a line like:\n"
        "OPENAI_API_KEY = sk-..."
    )
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ------------------------------
# SESSION STORAGE
# ------------------------------
if 'articles' not in st.session_state:
    st.session_state['articles'] = {}

if 'library_texts' not in st.session_state:
    st.session_state['library_texts'] = []  # Holds text extracted from uploaded docs

# ------------------------------
# FILE UPLOAD SECTION (YOUR GOOGLE DRIVE MATERIAL)
# ------------------------------
st.subheader("Upload Source Documents (DOCX, PDF, TXT)")

uploaded_files = st.file_uploader(
    "Upload letters, talks, essays — the AI will learn from them.",
    accept_multiple_files=True,
    type=["docx", "pdf", "txt"],
)


def extract_text_from_file(f):
    """Return plain text from supported file types."""
    name = f.name.lower()

    # DOCX
    if name.endswith(".docx") and docx is not None:
        doc = docx.Document(f)
        return "\n".join(p.text for p in doc.paragraphs)

    # PDF
    if name.endswith(".pdf") and PyPDF2 is not None:
        reader = PyPDF2.PdfReader(f)
        pages = []
        for p in reader.pages:
            try:
                pages.append(p.extract_text() or "")
            except Exception:
                pages.append("")
        return "\n".join(pages)

    # TXT (fallback)
    if name.endswith(".txt"):
        return f.read().decode("utf-8", errors="ignore")

    return ""  # unsupported or failed


if uploaded_files:
    added = 0
    for f in uploaded_files:
        text = extract_text_from_file(f)
        if text.strip():
            st.session_state['library_texts'].append(text)
            added += 1
    st.success(f"Added {added} document(s) to the knowledge library.")

# Show library status
if st.session_state['library_texts']:
    st.info(f"Knowledge library contains {len(st.session_state['library_texts'])} document(s). Yiddish is supported — the AI will understand it.")

# ------------------------------
# QUESTION INPUT
# ------------------------------
user_question = st.text_area(
    "Ask anything (the AI answers only from your sources):",
    height=140,
    placeholder="e.g., What did the Rebbe say about preemptive defense?",
)

# ------------------------------
# KNOWLEDGE SEARCH (RETRIEVAL)
# ------------------------------

# We switch from "dump everything" to a search system:
# 1) Break each document into small chunks.
# 2) When the user asks something, find the most relevant chunks.
# 3) Send ONLY those chunks to the AI (faster + more accurate).

if 'library_chunks' not in st.session_state:
    st.session_state['library_chunks'] = []  # each item: {"text": str, "source": str}


def chunk_text(text: str, size: int = 600, overlap: int = 120):
    """Split long text into overlapping chunks."""
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i : i + size])
        chunks.append(chunk)
        i += size - overlap
    return chunks

# Convert uploaded docs -> searchable chunks
if st.session_state['library_texts']:
    st.session_state['library_chunks'] = []
    for idx, doc in enumerate(st.session_state['library_texts']):
        for ch in chunk_text(doc):
            st.session_state['library_chunks'].append({
                "text": ch,
                "source": f"Document {idx + 1}"
            })


def score_chunk(question: str, chunk: str) -> int:
    """Very simple keyword scoring (no extra libraries)."""
    q_words = set(question.lower().split())
    c_words = set(chunk.lower().split())
    return len(q_words & c_words)


def search_library(question: str, top_k: int = 6):
    """Return the most relevant chunks for the question."""
    ranked = sorted(
        st.session_state['library_chunks'],
        key=lambda c: score_chunk(question, c['text']),
        reverse=True,
    )
    return ranked[:top_k]


# ------------------------------
# AI FUNCTION (USES SEARCHED CONTEXT ONLY)
# ------------------------------

def answer_question_or_generate_article(question: str) -> str:
    """Answer questions using searched context + prior articles."""

    # Merge previously generated content (safe newline string)
    article_context = "

".join(st.session_state['articles'].values())

    # Pull ONLY the relevant passages from uploaded docs
    results = search_library(question)
    library_context = "

".join([
        f"[From {r['source']}]
{r['text']}" for r in results
    ])

    # Safer, cleaner multiline prompt
    prompt = f"""
You are an AI Grokpedia assistant.
Answer ONLY using the material provided below.
If a clear source is not present in the context, say that you don't have enough information.
Prefer accuracy over speculation.

When helpful, organize answers with sections like:
- Overview
- Principles
- Halachic Basis
- Implications
- Conclusion

Quote or summarize specific passages and name the document when possible.

=== CONTEXT: PREVIOUS ARTICLES ===
{article_context}

=== CONTEXT: RELEVANT SOURCES (SEARCHED) ===
{library_context}

=== USER QUESTION ===
{question}
"""

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.15,
    )

    return response.choices[0].message.content

# ------------------------------
# SUBMIT
# ------------------------------
if st.button("Ask"):
    if not user_question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            try:
                answer = answer_question_or_generate_article(user_question.strip())
                st.subheader("Answer")
                st.write(answer)

                # Save to article history
                st.session_state['articles'][user_question] = answer
            except Exception as e:
                st.error(f"Error generating answer/article: {e}")

# ------------------------------
# HISTORY
# ------------------------------
if st.session_state['articles']:
    st.markdown("---")
    st.subheader("History of questions & answers")
    for q, a in st.session_state['articles'].items():
        st.markdown(f"**Question:** {q}")
        st.write(a)
        st.markdown("---")
