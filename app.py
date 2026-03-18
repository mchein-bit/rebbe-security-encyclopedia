import streamlit as st
import docx
from openai import OpenAI
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
import io
import json
import pickle
import datetime

# ------------------------------
# PAGE CONFIG & CUSTOM STYLING
# ------------------------------
st.set_page_config(
    page_title="Rebbe's Teachings on Israel & the Middle East",
    page_icon="✡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Crimson+Text:ital,wght@0,400;0,600;1,400&display=swap');

/* ---- Base ---- */
html, body, [class*="css"] {
    font-family: 'Crimson Text', serif;
    background-color: #0d0d0d;
    color: #e8dcc8;
}

/* ---- Header banner ---- */
.hero-banner {
    background: linear-gradient(135deg, #1a0a00 0%, #2a1200 40%, #0d0d0d 100%);
    border: 1px solid #8b6914;
    border-radius: 4px;
    padding: 40px 32px 32px 32px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: "✡";
    position: absolute;
    right: 32px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 80px;
    opacity: 0.08;
    color: #d4a843;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.4rem;
    font-weight: 900;
    color: #d4a843;
    margin: 0 0 8px 0;
    line-height: 1.2;
    letter-spacing: 0.5px;
}
.hero-subtitle {
    font-size: 1.15rem;
    color: #b8a88a;
    margin: 0;
    font-style: italic;
}
.hero-divider {
    width: 60px;
    height: 2px;
    background: #8b6914;
    margin: 16px 0;
}

/* ---- Sidebar ---- */
[data-testid="stSidebar"] {
    background-color: #111111 !important;
    border-right: 1px solid #2a1e00;
}
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    font-family: 'Playfair Display', serif;
    color: #d4a843;
}

/* ---- Inputs ---- */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background-color: #1a1200 !important;
    border: 1px solid #4a3a10 !important;
    color: #e8dcc8 !important;
    border-radius: 3px !important;
    font-family: 'Crimson Text', serif !important;
    font-size: 1.05rem !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #d4a843 !important;
    box-shadow: 0 0 0 2px rgba(212,168,67,0.15) !important;
}

/* ---- Buttons ---- */
.stButton > button {
    background: linear-gradient(135deg, #4a2c00, #8b6914) !important;
    color: #fffbe6 !important;
    border: none !important;
    border-radius: 3px !important;
    font-family: 'Playfair Display', serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px !important;
    padding: 10px 24px !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #8b6914, #d4a843) !important;
    color: #0d0d0d !important;
    transform: translateY(-1px) !important;
}

/* ---- Answer box ---- */
.answer-card {
    background: linear-gradient(180deg, #160d00 0%, #0d0d0d 100%);
    border: 1px solid #4a3a10;
    border-left: 4px solid #d4a843;
    border-radius: 4px;
    padding: 28px 28px 24px 28px;
    margin-top: 20px;
}
.answer-card h4 {
    font-family: 'Playfair Display', serif;
    color: #d4a843;
    font-size: 1.1rem;
    margin: 0 0 14px 0;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    font-size: 0.85rem;
}
.answer-text {
    font-size: 1.1rem;
    line-height: 1.85;
    color: #e8dcc8;
}

/* ---- Source chips ---- */
.source-chip {
    display: inline-block;
    background: #1e1400;
    border: 1px solid #4a3a10;
    color: #b8a88a;
    font-size: 0.78rem;
    padding: 3px 10px;
    border-radius: 20px;
    margin: 3px 3px 3px 0;
    font-family: 'Crimson Text', serif;
}

/* ---- Stat boxes ---- */
.stat-row {
    display: flex;
    gap: 12px;
    margin-bottom: 20px;
}
.stat-box {
    flex: 1;
    background: #160d00;
    border: 1px solid #2a1e00;
    border-radius: 4px;
    padding: 14px 16px;
    text-align: center;
}
.stat-number {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    color: #d4a843;
    font-weight: 700;
}
.stat-label {
    font-size: 0.8rem;
    color: #7a6a50;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ---- History entries ---- */
.history-entry {
    background: #130d00;
    border: 1px solid #2a1e00;
    border-radius: 3px;
    padding: 12px 14px;
    margin-bottom: 8px;
    font-size: 0.92rem;
}
.history-q {
    color: #d4a843;
    font-style: italic;
    margin-bottom: 4px;
}
.history-ts {
    color: #4a3a20;
    font-size: 0.75rem;
}

/* ---- Section headers ---- */
.section-header {
    font-family: 'Playfair Display', serif;
    color: #d4a843;
    font-size: 1.3rem;
    border-bottom: 1px solid #2a1e00;
    padding-bottom: 8px;
    margin: 28px 0 16px 0;
}

/* ---- Info / success / warning overrides ---- */
.stAlert {
    background-color: #160d00 !important;
    border-color: #4a3a10 !important;
    color: #b8a88a !important;
}

/* ---- Hide Streamlit default elements ---- */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ------------------------------
# OPENAI CLIENT SETUP
# ------------------------------
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# ------------------------------
# SESSION STATE INITIALIZATION
# ------------------------------
if 'library_chunks' not in st.session_state:
    try:
        with open("library_chunks.pkl", "rb") as f:
            st.session_state['library_chunks'] = pickle.load(f)
    except FileNotFoundError:
        st.session_state['library_chunks'] = []

if 'embeddings' not in st.session_state:
    try:
        with open("embeddings.pkl", "rb") as f:
            st.session_state['embeddings'] = pickle.load(f)
    except FileNotFoundError:
        st.session_state['embeddings'] = []

if 'question_history' not in st.session_state:
    st.session_state['question_history'] = []

if 'last_answer' not in st.session_state:
    st.session_state['last_answer'] = None

if 'last_sources' not in st.session_state:
    st.session_state['last_sources'] = []

# ------------------------------
# HERO BANNER
# ------------------------------
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">The Rebbe's Teachings on Israel & the Middle East</div>
    <div class="hero-divider"></div>
    <div class="hero-subtitle">
        A living knowledge base of the Lubavitcher Rebbe's wisdom on Israel, security, and the Middle East — 
        grounded in Torah and growing with every question asked.
    </div>
</div>
""", unsafe_allow_html=True)

# ------------------------------
# GOOGLE DRIVE SETUP
# ------------------------------
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

try:
    service_account_json_str = st.secrets["google"]["service_account_json"]
    service_account_info = json.loads(service_account_json_str)
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=SCOPES
    )
    drive_service = build('drive', 'v3', credentials=credentials)
    drive_connected = True
except Exception:
    drive_service = None
    drive_connected = False

# ------------------------------
# HELPER FUNCTIONS
# ------------------------------

def _get_embedding(text: str):
    try:
        resp = client.embeddings.create(model="text-embedding-3-small", input=text)
        return resp.data[0].embedding
    except Exception:
        return None


def _cosine_similarity(a, b):
    if not a or not b:
        return 0
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0
    return dot / (norm_a * norm_b)


def build_embeddings_index():
    chunks = st.session_state.get('library_chunks', [])
    if not chunks:
        st.warning("No documents loaded yet. Please load documents first.")
        return
    progress = st.progress(0, text="Building search index…")
    vectors = []
    for i, ch in enumerate(chunks):
        vec = _get_embedding(ch["text"])
        vectors.append(vec)
        progress.progress((i + 1) / len(chunks), text=f"Indexing chunk {i+1} of {len(chunks)}…")
    st.session_state['embeddings'] = vectors
    with open("embeddings.pkl", "wb") as f:
        pickle.dump(vectors, f)
    progress.empty()
    st.success(f"✅ Search index built — {len(vectors)} chunks indexed.")


def search_chunks(query: str, top_k: int = 10):
    if not st.session_state.get("embeddings"):
        return []
    q_vec = _get_embedding(query)
    if not q_vec:
        return []
    scored = []
    for chunk, vec in zip(st.session_state.get("library_chunks", []), st.session_state.get("embeddings", [])):
        if vec:
            scored.append((_cosine_similarity(q_vec, vec), chunk))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [c for _, c in scored[:top_k]]


def _extract_text_from_drive_file(file_meta):
    file_id = file_meta["id"]
    mime = file_meta["mimeType"]
    if mime == "application/vnd.google-apps.document":
        request = drive_service.files().export_media(fileId=file_id, mimeType="text/plain")
    else:
        request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    fh.seek(0)
    if mime in ("application/vnd.google-apps.document", "text/plain"):
        return fh.read().decode("utf-8")
    if mime == "application/pdf":
        try:
            import PyPDF2
            reader = PyPDF2.PdfReader(fh)
            return "\n".join([page.extract_text() or "" for page in reader.pages])
        except Exception:
            return ""
    if mime == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        document = docx.Document(fh)
        return "\n".join([p.text for p in document.paragraphs])
    return ""


def load_folder_recursive(folder_id, added_counter, progress_placeholder):
    try:
        results = drive_service.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            pageSize=1000,
            fields="files(id, name, mimeType)",
            includeItemsFromAllDrives=True,
            supportsAllDrives=True
        ).execute()
        items = results.get("files", [])
        for item in items:
            mime = item["mimeType"]
            if mime == "application/vnd.google-apps.folder":
                load_folder_recursive(item["id"], added_counter, progress_placeholder)
                continue
            if mime in [
                "text/plain", "application/pdf",
                "application/vnd.google-apps.document",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ]:
                progress_placeholder.info(f"Loading: {item['name']}…")
                text = _extract_text_from_drive_file(item)
                if text:
                    chunk_size = 120
                    overlap = 20
                    words = text.split()
                    i = 0
                    while i < len(words):
                        chunk = " ".join(words[i:i + chunk_size])
                        st.session_state['library_chunks'].append({
                            "source": item['name'],
                            "text": chunk
                        })
                        i += chunk_size - overlap
                    added_counter[0] += 1
    except Exception as e:
        st.error(f"Error loading folder {folder_id}: {e}")


def answer_question(question: str):
    library = st.session_state.get('library_chunks', [])
    if not library:
        return "No documents are loaded yet. Please load documents using the sidebar.", []

    # Vector search first, keyword fallback
    embeddings = st.session_state.get('embeddings', [])
    if isinstance(embeddings, list) and len(embeddings) > 0:
        selected_chunks = search_chunks(question, top_k=12)
    else:
        selected_chunks = []

    if not selected_chunks:
        q_low = question.lower()
        selected_chunks = [ch for ch in library if q_low in ch['text'].lower()][:12]

    if not selected_chunks:
        return "I couldn't find relevant passages in the loaded documents for this question.", []

    library_context = "\n\n".join(
        f"[From: {ch['source']}]\n{ch['text']}" for ch in selected_chunks
    )

    sources = list(dict.fromkeys(ch['source'] for ch in selected_chunks))

    system_prompt = (
        "You are a respectful, scholarly assistant specializing in the Lubavitcher Rebbe's teachings — "
        "particularly his views on Israel, security, and the Middle East as rooted in Torah. "
        "Answer clearly, thoughtfully, and faithfully using ONLY the provided source passages. "
        "Cite the source document name when relevant. "
        "If the sources don't contain enough to fully answer the question, say so honestly. "
        "Write in a dignified, encyclopedic tone appropriate for a serious Torah knowledge base."
    )

    prompt = (
        f"=== SOURCE PASSAGES ===\n{library_context}\n\n"
        f"=== QUESTION ===\n{question}"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.15,
        )
        return response.choices[0].message.content, sources
    except Exception as e:
        return f"OpenAI API error: {e}", []


# ------------------------------
# SIDEBAR
# ------------------------------
with st.sidebar:
    st.markdown("## ✡️ Admin Panel")
    st.markdown("---")

    # Stats
    n_chunks = len(st.session_state.get('library_chunks', []))
    n_embeddings = len(st.session_state.get('embeddings', []))
    n_questions = len(st.session_state.get('question_history', []))
    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-box">
            <div class="stat-number">{n_chunks}</div>
            <div class="stat-label">Passages</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">{n_questions}</div>
            <div class="stat-label">Questions</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📂 Load Documents")
    if not drive_connected:
        st.warning("Google Drive not connected.\nAdd credentials to Streamlit Secrets.")
    else:
        st.success("Google Drive connected ✓")
        folder_ids_input = st.text_area(
            "Google Drive Folder IDs (one per line):",
            height=100,
            help="Paste the folder ID from your Google Drive URL"
        )
        folder_ids = [f.strip() for f in folder_ids_input.splitlines() if f.strip()]

        if st.button("📥 Load Documents from Drive"):
            if folder_ids:
                progress_placeholder = st.empty()
                for fid in folder_ids:
                    added = [0]
                    load_folder_recursive(fid, added, progress_placeholder)
                    if added[0] > 0:
                        st.success(f"Loaded {added[0]} file(s) from folder.")
                    else:
                        st.warning(f"No supported files found in folder {fid}.")
                progress_placeholder.empty()
                with open("library_chunks.pkl", "wb") as f:
                    pickle.dump(st.session_state['library_chunks'], f)
                st.success(f"Total passages: {len(st.session_state['library_chunks'])}")
            else:
                st.warning("Please enter at least one Folder ID.")

    st.markdown("### 🔍 Search Index")
    index_status = "✅ Built" if n_embeddings > 0 else "❌ Not built"
    st.write(f"Index status: {index_status}")
    if st.button("⚙️ Build / Rebuild Search Index"):
        build_embeddings_index()

    st.markdown("---")
    st.markdown("### 📜 Recent Questions")
    history = st.session_state.get('question_history', [])
    if history:
        for entry in reversed(history[-5:]):
            st.markdown(f"""
            <div class="history-entry">
                <div class="history-q">"{entry['question']}"</div>
                <div class="history-ts">{entry['timestamp']}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.caption("No questions yet. Be the first to ask!")

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.78rem; color:#4a3a20; text-align:center; padding-top:8px;">
        Built on the Rebbe's teachings.<br>
        Growing with every question asked.
    </div>
    """, unsafe_allow_html=True)

# ------------------------------
# MAIN — QUESTION INPUT
# ------------------------------
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown('<div class="section-header">Ask a Question</div>', unsafe_allow_html=True)
    question = st.text_input(
        "",
        placeholder="e.g. What did the Rebbe say about giving back land for peace?",
        label_visibility="collapsed"
    )

with col2:
    st.markdown("<div style='margin-top: 44px;'></div>", unsafe_allow_html=True)
    ask_clicked = st.button("Ask the Rebbe's Teachings →", use_container_width=True)

# Suggested questions
st.markdown("""
<div style="font-size: 0.85rem; color: #5a4a30; margin-top: 6px; margin-bottom: 24px;">
💡 Try asking: <em>"What is the Rebbe's view on the security of Israel?"</em> &nbsp;·&nbsp; 
<em>"What does Torah say about the borders of Israel?"</em> &nbsp;·&nbsp; 
<em>"How did the Rebbe respond to peace negotiations?"</em>
</div>
""", unsafe_allow_html=True)

# ------------------------------
# ANSWER DISPLAY
# ------------------------------
if ask_clicked and question.strip():
    with st.spinner("Searching the Rebbe's teachings…"):
        answer, sources = answer_question(question.strip())

    st.session_state['last_answer'] = answer
    st.session_state['last_sources'] = sources

    # Save to history
    st.session_state['question_history'].append({
        'question': question.strip(),
        'timestamp': datetime.datetime.now().strftime("%b %d, %Y %I:%M %p")
    })

    # Display answer
    source_chips = "".join(f'<span class="source-chip">📄 {s}</span>' for s in sources)
    st.markdown(f"""
    <div class="answer-card">
        <h4>Answer from the Rebbe's Teachings</h4>
        <div class="answer-text">{answer.replace(chr(10), '<br>')}</div>
        <div style="margin-top: 20px; border-top: 1px solid #2a1e00; padding-top: 14px;">
            <div style="font-size:0.78rem; color:#7a6a50; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px;">Sources Referenced</div>
            {source_chips if source_chips else '<span style="color:#4a3a20; font-size:0.85rem;">No specific source documents cited.</span>'}
        </div>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.get('last_answer'):
    answer = st.session_state['last_answer']
    sources = st.session_state.get('last_sources', [])
    source_chips = "".join(f'<span class="source-chip">📄 {s}</span>' for s in sources)
    st.markdown(f"""
    <div class="answer-card">
        <h4>Answer from the Rebbe's Teachings</h4>
        <div class="answer-text">{answer.replace(chr(10), '<br>')}</div>
        <div style="margin-top: 20px; border-top: 1px solid #2a1e00; padding-top: 14px;">
            <div style="font-size:0.78rem; color:#7a6a50; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px;">Sources Referenced</div>
            {source_chips if source_chips else '<span style="color:#4a3a20; font-size:0.85rem;">No specific source documents cited.</span>'}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------
# ABOUT SECTION
# ------------------------------
st.markdown("---")
with st.expander("ℹ️ About This Knowledge Base"):
    st.markdown("""
    **What is this?**  
    This is a living, growing encyclopedia of the Lubavitcher Rebbe's teachings on Israel, security, and the Middle East — all grounded in Torah.

    **How does it work?**  
    Documents from the Rebbe's writings are loaded into a searchable library. When you ask a question, the AI finds the most relevant passages and crafts a faithful, scholarly answer using only those sources.

    **How does it grow?**  
    Anyone with admin access can add new documents to Google Drive. The knowledge base automatically learns from them once they're indexed.

    **Is it accurate?**  
    The AI only answers from the loaded documents — it does not invent or guess. If it can't find an answer in the sources, it says so.
    """)
