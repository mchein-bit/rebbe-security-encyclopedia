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

# ------------------------------
# OPENAI CLIENT SETUP
# ------------------------------
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

st.title("Rebbe Security Encyclopedia")
st.write("Ask any question about the Rebbe's teachings on security for Israel.")

# ------------------------------
# GOOGLE DRIVE INTEGRATION USING STREAMLIT SECRETS
# ------------------------------
st.subheader("Load documents from Google Drive")

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

try:
    service_account_json_str = st.secrets["google"]["service_account_json"]
    service_account_info = json.loads(service_account_json_str)
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=SCOPES
    )
    service = build('drive', 'v3', credentials=credentials)
except Exception as e:
    st.error(f"Google Drive authentication failed. Check that your JSON in secrets is valid: {e}")
    st.stop()

folder_ids_input = st.text_area("Enter Google Drive Folder IDs (one per line):")
folder_ids = [f.strip() for f in folder_ids_input.splitlines() if f.strip()]

# ------------------------------
# HELPER FUNCTIONS
# ------------------------------

# --- STEP 3A: EMBEDDING INDEX (store searchable vectors) ---
# We will build this gradually. For now, we only define helper functions.

def _get_embedding(text: str):
    """Return OpenAI embedding vector for a chunk of text."""
    try:
        resp = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return resp.data[0].embedding
    except Exception:
        return None


def _cosine_similarity(a, b):
    """Compute cosine similarity between two vectors (pure python)."""
    if not a or not b:
        return 0
    dot = sum(x*y for x, y in zip(a, b))
    norm_a = sum(x*x for x in a) ** 0.5
    norm_b = sum(x*x for x in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0
    return dot / (norm_a * norm_b)


def build_embeddings_index():
    """Create embeddings for every chunk and cache them on disk."""
    st.info("Building embeddings index (first time may take a while)...")
    vectors = []
    for ch in st.session_state.get('library_chunks', []):
        vec = _get_embedding(ch["text"])
        vectors.append(vec)
    st.session_state['embeddings'] = vectors
    # persist to disk
    with open("embeddings.pkl", "wb") as f:
        pickle.dump(vectors, f)
    st.success("Embedding index created and saved.")


# --- STEP 3B: SEARCH THE EMBEDDINGS INDEX ---
# Given a question, we compute its embedding and return the best‑matching chunks.

def search_chunks(query: str, top_k: int = 8):
    if not st.session_state.get("embeddings"):
        return []

    q_vec = _get_embedding(query)
    if not q_vec:
        return []

    scored = []
    for chunk, vec in zip(st.session_state.get("library_chunks", []), st.session_state.get("embeddings", [])):
        if vec:
            scored.append(( _cosine_similarity(q_vec, vec), chunk))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [c for _, c in scored[:top_k]]


def _extract_text_from_drive_file(file_meta):
    file_id = file_meta["id"]
    mime = file_meta["mimeType"]

    if mime == "application/vnd.google-apps.document":
        request = service.files().export_media(fileId=file_id, mimeType="text/plain")
    else:
        request = service.files().get_media(fileId=file_id)

    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    fh.seek(0)

    if mime == "application/vnd.google-apps.document" or mime == "text/plain":
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

# Recursively walk folders

def load_folder_recursive(folder_id, added_counter):
    try:
        results = service.files().list(
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
                load_folder_recursive(item["id"], added_counter)
                continue

            if mime in [
                "text/plain",
                "application/pdf",
                "application/vnd.google-apps.document",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ]:
                text = _extract_text_from_drive_file(item)
                if text:
                    # Further reduce chunk size and overlap to limit tokens
                    chunk_size = 30
                    overlap = 10
                    words = text.split()
                    i = 0
                    while i < len(words):
                        chunk = " ".join(words[i:i+chunk_size])
                        st.session_state['library_chunks'].append({
                            "source": item['name'],
                            "text": chunk
                        })
                        i += chunk_size - overlap
                    added_counter[0] += 1
    except Exception as e:
        st.error(f"Error loading files from folder {folder_id}: {e}")

# Load library from disk if available
# (and later we will pair it with an embeddings index)
if 'library_chunks' not in st.session_state:
    try:
        with open("library_chunks.pkl", "rb") as f:
            st.session_state['library_chunks'] = pickle.load(f)
        st.success("Loaded document library from disk.")
    except FileNotFoundError:
        st.session_state['library_chunks'] = []

# Try loading embeddings index (optional at this stage)
if 'embeddings' not in st.session_state:
    try:
        with open("embeddings.pkl", "rb") as f:
            st.session_state['embeddings'] = pickle.load(f)
        st.info("Loaded existing embeddings index.")
    except FileNotFoundError:
        st.session_state['embeddings'] = []

if folder_ids:
    for FOLDER_ID in folder_ids:
        added = [0]
        load_folder_recursive(FOLDER_ID, added)
        if added[0] > 0:
            st.success(f"Added {added[0]} file(s) (including sub‑folders) from folder {FOLDER_ID}.")
        else:
            st.warning(f"No supported documents found in folder {FOLDER_ID}.")

    # Save library to disk
    with open("library_chunks.pkl", "wb") as f:
        pickle.dump(st.session_state['library_chunks'], f)

# --- ALWAYS SHOW INDEX BUTTON ---
st.markdown("---")
st.subheader("Search Index")
st.write(f"Chunks loaded: {len(st.session_state.get('library_chunks', []))}")
st.write(f"Embeddings loaded: {len(st.session_state.get('embeddings', []))}")

if st.button("Build / Rebuild Search Index"):
    build_embeddings_index()

# ------------------------------
# AI FUNCTION AND USER UI
# ------------------------------

def answer_question_or_generate_article(question: str) -> str:
    st.write("Debug: AI function called")

    # No article generation yet
    article_context = ""

    # Safety check
    if not st.session_state.get('library_chunks'):
        st.warning("No documents available.")
        return ""

    # ---- SEARCH ----
    selected_chunks = []

    # Use embeddings search ONLY if embeddings exist
    if st.session_state.get('embeddings'):
        selected_chunks = search_chunks(question, top_k=12)
        st.write(f"DEBUG — vector search returned {len(selected_chunks)} results")
    else:
        st.write("DEBUG — embeddings not built, skipping vector search")

    # Keyword fallback (always available)
    if not selected_chunks:
        q_low = question.lower()
        selected_chunks = [
            ch for ch in st.session_state['library_chunks']
            if q_low in ch['text'].lower()
        ][:12]
        st.write(f"DEBUG — keyword fallback returned {len(selected_chunks)} results")

        # Build context safely (FIXED — valid Python string join)
    library_context = 

.join(
        f"[From {ch['source']}]
{ch['text']}"
        for ch in selected_chunks
    )

    st.write(f"DEBUG — library_context length = {len(library_context)}")

    prompt = f"""
You are a Grokpedia-style scholarly assistant.
Answer ONLY using the sources below.
If the sources do not answer the question, say so.

=== SOURCES ===
{library_context}

=== QUESTION ===
{question}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.15,
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"OpenAI API error: {e}")
        return ""


# ------------------------------
# USER INPUT
# ------------------------------
question = st.text_input("Type your question here:")

if question:
    answer = answer_question_or_generate_article(question)
    st.subheader("Answer")
    st.write(answer)
