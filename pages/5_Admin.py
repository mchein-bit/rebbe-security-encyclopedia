import streamlit as st
import sys, os, io, json, pickle
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.styles import apply_global_styles
from utils.storage import load_articles
import docx

# Always save data files to the repo root
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHUNKS_FILE = os.path.join(ROOT_DIR, "library_chunks.pkl")
EMBEDDINGS_FILE = os.path.join(ROOT_DIR, "embeddings.pkl")

st.set_page_config(
    page_title="Admin — Rebbe Encyclopedia",
    page_icon="✡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

apply_global_styles()

# ── Navbar ────────────────────────────────────────────────────────────────────
col_n1, col_n2, col_n3 = st.columns([2, 1, 1])
with col_n1:
    if st.button("✡ Rebbe's Encyclopedia", key="nav_home"):
        st.switch_page("app.py")
with col_n2:
    if st.button("Browse Articles", key="nav_browse"):
        st.switch_page("pages/3_Browse.py")
with col_n3:
    if st.button("Ask a Question", key="nav_ask"):
        st.switch_page("pages/2_Ask.py")

st.markdown("---")

st.markdown("""
<div style="padding: 32px 32px 8px;">
  <h1 style="font-family:'Cinzel',serif; font-size:1.6rem; color:#c9a84c; letter-spacing:1px; margin-bottom:4px;">
    Admin Panel
  </h1>
  <p style="color:#6a5f40; font-style:italic;">
    Load source documents and manage the knowledge base
  </p>
</div>
""", unsafe_allow_html=True)

# ── Initialize session state ──────────────────────────────────────────────────
if "library_chunks" not in st.session_state:
    try:
        with open(CHUNKS_FILE,"rb") as f:
            st.session_state["library_chunks"] = pickle.load(f)
    except FileNotFoundError:
        st.session_state["library_chunks"] = []

if "embeddings" not in st.session_state:
    try:
        with open(EMBEDDINGS_FILE,"rb") as f:
            st.session_state["embeddings"] = pickle.load(f)
    except FileNotFoundError:
        st.session_state["embeddings"] = []

n_chunks = len(st.session_state.get("library_chunks", []))
n_embed  = len(st.session_state.get("embeddings", []))
n_arts   = len(load_articles())

# ── Stats ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="display:flex; gap:16px; padding: 8px 32px 32px; flex-wrap:wrap;">
  <div style="background:#111008; border:1px solid #2a2210; border-radius:3px; padding:20px 28px; text-align:center; min-width:140px;">
    <div style="font-family:'Cinzel',serif; font-size:2rem; color:#c9a84c; font-weight:900;">{n_chunks}</div>
    <div style="font-size:0.78rem; color:#4a3d28; text-transform:uppercase; letter-spacing:0.5px;">Source Passages</div>
  </div>
  <div style="background:#111008; border:1px solid #2a2210; border-radius:3px; padding:20px 28px; text-align:center; min-width:140px;">
    <div style="font-family:'Cinzel',serif; font-size:2rem; color:#c9a84c; font-weight:900;">{'✅' if n_embed > 0 else '❌'}</div>
    <div style="font-size:0.78rem; color:#4a3d28; text-transform:uppercase; letter-spacing:0.5px;">Search Index</div>
  </div>
  <div style="background:#111008; border:1px solid #2a2210; border-radius:3px; padding:20px 28px; text-align:center; min-width:140px;">
    <div style="font-family:'Cinzel',serif; font-size:2rem; color:#c9a84c; font-weight:900;">{n_arts}</div>
    <div style="font-size:0.78rem; color:#4a3d28; text-transform:uppercase; letter-spacing:0.5px;">Published Articles</div>
  </div>
</div>
""", unsafe_allow_html=True)

_, col_main, _ = st.columns([0.2, 3, 0.2])

with col_main:

    # ── Google Drive ──────────────────────────────────────────────────────
    st.markdown("""
    <h2 style="font-family:'Cinzel',serif; font-size:1.1rem; color:#c9a84c; letter-spacing:1px; 
        border-bottom:1px solid #2a2210; padding-bottom:8px; margin-bottom:16px;">
      📂 Load Documents from Google Drive
    </h2>
    """, unsafe_allow_html=True)

    # Setup Drive connection
    try:
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaIoBaseDownload
        from google.oauth2 import service_account

        service_account_json_str = st.secrets["google"]["service_account_json"]
        service_account_info = json.loads(service_account_json_str)
        SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
        credentials = service_account.Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
        drive_service = build("drive", "v3", credentials=credentials)
        drive_ok = True
        st.success("✅ Google Drive connected")
    except Exception as e:
        drive_ok = False
        st.warning(f"Google Drive not connected: {e}")

    folder_input = st.text_area(
        "Google Drive Folder IDs (one per line):",
        height=100,
        help="Get the folder ID from the end of the Google Drive folder URL"
    )

    def _extract_text(file_meta, svc):
        fid  = file_meta["id"]
        mime = file_meta["mimeType"]
        if mime == "application/vnd.google-apps.document":
            req = svc.files().export_media(fileId=fid, mimeType="text/plain")
        else:
            req = svc.files().get_media(fileId=fid)
        fh = io.BytesIO()
        dl = MediaIoBaseDownload(fh, req)
        done = False
        while not done:
            _, done = dl.next_chunk()
        fh.seek(0)
        if mime in ("application/vnd.google-apps.document","text/plain"):
            return fh.read().decode("utf-8")
        if mime == "application/pdf":
            try:
                import PyPDF2
                reader = PyPDF2.PdfReader(fh)
                return "\n".join([p.extract_text() or "" for p in reader.pages])
            except Exception:
                return ""
        if mime == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = docx.Document(fh)
            return "\n".join([p.text for p in doc.paragraphs])
        return ""

    def _walk_folder(folder_id, svc, counter, placeholder):
        try:
            results = svc.files().list(
                q=f"'{folder_id}' in parents and trashed=false",
                pageSize=1000,
                fields="files(id,name,mimeType)",
                includeItemsFromAllDrives=True,
                supportsAllDrives=True
            ).execute()
            for item in results.get("files",[]):
                if item["mimeType"] == "application/vnd.google-apps.folder":
                    _walk_folder(item["id"], svc, counter, placeholder)
                    continue
                if item["mimeType"] in [
                    "text/plain","application/pdf",
                    "application/vnd.google-apps.document",
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                ]:
                    placeholder.info(f"Loading: {item['name']}…")
                    text = _extract_text(item, svc)
                    if text:
                        # 300-word chunks with 60-word overlap
                        # This keeps full thoughts/paragraphs together
                        # so the AI reads complete ideas, not cut-off sentences
                        chunk_size, overlap = 300, 60
                        words = text.split()
                        i = 0
                        while i < len(words):
                            chunk = " ".join(words[i:i+chunk_size])
                            st.session_state["library_chunks"].append({
                                "source": item["name"],
                                "text": chunk
                            })
                            i += chunk_size - overlap
                        counter[0] += 1
        except Exception as e:
            st.error(f"Error in folder {folder_id}: {e}")

    if st.button("📥 Load Documents", type="primary", disabled=not drive_ok):
        folder_ids = [f.strip() for f in folder_input.splitlines() if f.strip()]
        if not folder_ids:
            st.warning("Enter at least one Folder ID.")
        else:
            prog = st.empty()
            for fid in folder_ids:
                added = [0]
                _walk_folder(fid, drive_service, added, prog)
                if added[0]:
                    st.success(f"Loaded {added[0]} file(s) from folder.")
                else:
                    st.warning(f"No files found in folder {fid}.")
            prog.empty()
            with open(CHUNKS_FILE,"wb") as f:
                pickle.dump(st.session_state["library_chunks"], f)
            st.success(f"✅ {len(st.session_state['library_chunks'])} total passages in library.")
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Search Index ──────────────────────────────────────────────────────
    st.markdown("""
    <h2 style="font-family:'Cinzel',serif; font-size:1.1rem; color:#c9a84c; letter-spacing:1px; 
        border-bottom:1px solid #2a2210; padding-bottom:8px; margin-bottom:16px;">
      🔍 Search Index
    </h2>
    """, unsafe_allow_html=True)

    st.write(f"Index status: **{'Built ✅' if n_embed > 0 else 'Not built ❌'}** &nbsp;·&nbsp; {n_embed} embeddings")
    st.caption("The search index must be built after loading documents so the AI can find the right passages.")

    if st.button("⚙️ Build / Rebuild Search Index", type="primary"):
        chunks = st.session_state.get("library_chunks", [])
        if not chunks:
            st.warning("No documents loaded yet.")
        else:
            from openai import OpenAI
            import os
            oai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            prog2 = st.progress(0, text="Building index…")
            vecs = []
            for i, ch in enumerate(chunks):
                try:
                    resp = oai.embeddings.create(model="text-embedding-3-small", input=ch["text"])
                    vecs.append(resp.data[0].embedding)
                except Exception:
                    vecs.append(None)
                prog2.progress((i+1)/len(chunks), text=f"Indexing {i+1}/{len(chunks)}…")
            st.session_state["embeddings"] = vecs
            with open(EMBEDDINGS_FILE,"wb") as f:
                pickle.dump(vecs, f)
            prog2.empty()
            st.success(f"✅ Index built — {len(vecs)} passages indexed.")
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Article management ────────────────────────────────────────────────
    st.markdown("""
    <h2 style="font-family:'Cinzel',serif; font-size:1.1rem; color:#c9a84c; letter-spacing:1px; 
        border-bottom:1px solid #2a2210; padding-bottom:8px; margin-bottom:16px;">
      📚 Published Articles
    </h2>
    """, unsafe_allow_html=True)

    articles = load_articles()
    if articles:
        for art in sorted(articles, key=lambda a: a.get("created_at",""), reverse=True):
            c1, c2 = st.columns([4,1])
            with c1:
                st.markdown(f"""
                <div style="padding:10px 0; border-bottom:1px solid #1a1608;">
                  <span style="font-family:'Cinzel',serif; font-size:0.88rem; color:#c9a84c;">{art['title']}</span>
                  <span style="font-size:0.75rem; color:#4a3d28; margin-left:12px;">{art.get('category','')}</span>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                if st.button("View", key=f"admin_view_{art['id']}"):
                    st.session_state["open_article_id"] = art["id"]
                    st.switch_page("pages/4_Article.py")
    else:
        st.info("No articles published yet. Ask a question to create the first one!")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<div class="footer">Built on the Rebbe\'s teachings &nbsp;·&nbsp; Growing with every question asked</div>', unsafe_allow_html=True)
