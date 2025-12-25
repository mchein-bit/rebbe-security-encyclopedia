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
# AI FUNCTION (USES ARTICLES + UPLOADED DOCUMENTS)
# ------------------------------

def answer_question_or_generate_article(question: str) -> str:
    # Merge previously generated content
    article_context = "\n\n".join(st.session_state['articles'].values())

    # Merge uploaded documents
    library_context = "\n\n".join(st.session_state['library_texts'])

    prompt = (
        "You are an AI Grokpedia assistant. Answer ONLY using the material provided.\n"
        "If a clear source is not present in the context, say you don't have enough information.\n"
        "Prefer accuracy over speculation.\n\n"
        "Write answers in a structured way when helpful (Overview, Principles, Halachic Basis, Implications, Conclusion).\n"
        "Quote or summarize specific lines when possible, and reference which document or idea it comes from.\n\n"
        f"=== CONTEXT: PREVIOUS ARTICLES ===\n{article_context}\n\n"
        f"=== CONTEXT: UPLOADED DOCUMENTS ===\n{library_context}\n\n"
        f"=== USER QUESTION ===\n{question}"
    )

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
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
