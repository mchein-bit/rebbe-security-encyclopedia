import streamlit as st
import sys, os, io, json, pickle
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.styles import apply_global_styles
from utils.storage import load_articles
import docx

st.set_page_config(page_title="Admin — Enduring Peace", page_icon="📖", layout="wide", initial_sidebar_state="collapsed")
apply_global_styles()

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHUNKS_FILE = os.path.join(ROOT_DIR, "library_chunks.pkl")
EMBEDDINGS_FILE = os.path.join(ROOT_DIR, "embeddings.pkl")

# ── Navbar ────────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
with c1:
    if st.button("← Enduring Peace Knowledge Base", key="nav_home"):
        st.switch_page("app.py")
with c2:
    st.markdown("<div style='margin-top:6px;'></div>", unsafe_allow_html=True)
    if st.button("Browse", key="nav_browse", use_container_width=True):
        st.switch_page("pages/3_Browse.py")
with c3:
    st.markdown("<div style='margin-top:6px;'></div>", unsafe_allow_html=True)
    if st.button("Ask a Question", key="nav_ask", use_container_width=True):
        st.switch_page("pages/2_Ask.py")
with c4:
    st.markdown("")
st.markdown("<hr style='margin:0;'>", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "library_chunks" not in st.session_state:
    try:
        with open(CHUNKS_FILE,"rb") as f: st.session_state["library_chunks"] = pickle.load(f)
    except FileNotFoundError:
        st.session_state["library_chunks"] = []

if "embeddings" not in st.session_state:
    try:
        with open(EMBEDDINGS_FILE,"rb") as f: st.session_state["embeddings"] = pickle.load(f)
    except FileNotFoundError:
        st.session_state["embeddings"] = []

n_chunks  = len(st.session_state.get("library_chunks",[]))
n_embed   = len(st.session_state.get("embeddings",[]))
n_arts    = len(load_articles())

# ── Header ────────────────────────────────────────────────────────────────────
_, main_col, _ = st.columns([1, 5, 1])
with main_col:
    st.markdown("""
    <div style="padding:40px 0 24px;">
      <h1 style="font-family:'Libre Baskerville',serif; font-size:1.8rem; font-weight:700;
           color:#1c2b3a; margin-bottom:4px;">Admin Panel</h1>
      <p style="color:#9c9080; font-style:italic;">Load documents and manage the knowledge base</p>
    </div>
    """, unsafe_allow_html=True)

    # Stats
    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown(f'<div class="ep-stat-box"><div class="ep-stat-num">{n_chunks}</div><div class="ep-stat-label">Source Passages</div></div>', unsafe_allow_html=True)
    with s2:
        st.markdown(f'<div class="ep-stat-box"><div class="ep-stat-num">{"✅" if n_embed>0 else "❌"}</div><div class="ep-stat-label">Search Index</div></div>', unsafe_allow_html=True)
    with s3:
        st.markdown(f'<div class="ep-stat-box"><div class="ep-stat-num">{n_arts}</div><div class="ep-stat-label">Published Articles</div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:32px;'></div>", unsafe_allow_html=True)

    # ── Google Drive ──────────────────────────────────────────────────────
    st.markdown("""
    <h2 style="font-family:'Libre Baskerville',serif; font-size:1.1rem; font-weight:700;
        color:#1c2b3a; border-bottom:2px solid #d4820a; padding-bottom:8px; margin-bottom:16px;">
      Load Documents from Google Drive
    </h2>
    """, unsafe_allow_html=True)

    try:
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaIoBaseDownload
        from google.oauth2 import service_account
        svc_json = st.secrets["google"]["service_account_json"]
        svc_info = json.loads(svc_json)
        creds = service_account.Credentials.from_service_account_info(svc_info, scopes=["https://www.googleapis.com/auth/drive.readonly"])
        drive_service = build("drive","v3",credentials=creds)
        drive_ok = True
        st.success("Google Drive connected ✓")
    except Exception as e:
        drive_ok = False
        st.warning(f"Google Drive not connected: {e}")

    folder_input = st.text_area("Google Drive Folder IDs (one per line):", height=90,
        help="Copy the folder ID from the end of your Google Drive folder URL")

    def _extract_text(fm, svc):
        fid, mime = fm["id"], fm["mimeType"]
        req = svc.files().export_media(fileId=fid, mimeType="text/plain") if mime=="application/vnd.google-apps.document" else svc.files().get_media(fileId=fid)
        fh = io.BytesIO()
        dl = MediaIoBaseDownload(fh, req)
        done = False
        while not done: _, done = dl.next_chunk()
        fh.seek(0)
        if mime in ("application/vnd.google-apps.document","text/plain"):
            return fh.read().decode("utf-8")
        if mime == "application/pdf":
            try:
                import PyPDF2
                return "\n".join([p.extract_text() or "" for p in PyPDF2.PdfReader(fh).pages])
            except: return ""
        if mime == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return "\n".join([p.text for p in docx.Document(fh).paragraphs])
        return ""

    def _walk(fid, svc, counter, ph):
        try:
            items = svc.files().list(q=f"'{fid}' in parents and trashed=false", pageSize=1000,
                fields="files(id,name,mimeType)", includeItemsFromAllDrives=True, supportsAllDrives=True
            ).execute().get("files",[])
            for item in items:
                if item["mimeType"]=="application/vnd.google-apps.folder":
                    _walk(item["id"],svc,counter,ph); continue
                if item["mimeType"] in ["text/plain","application/pdf","application/vnd.google-apps.document",
                                         "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
                    ph.info(f"Loading: {item['name']}…")
                    text = _extract_text(item, svc)
                    if text:
                        chunk_size, overlap = 300, 60
                        words = text.split()
                        i = 0
                        while i < len(words):
                            st.session_state["library_chunks"].append({"source":item["name"],"text":" ".join(words[i:i+chunk_size])})
                            i += chunk_size - overlap
                        counter[0] += 1
        except Exception as e:
            st.error(f"Error in folder {fid}: {e}")

    if st.button("Load Documents from Drive", type="primary", disabled=not drive_ok):
        fids = [f.strip() for f in folder_input.splitlines() if f.strip()]
        if not fids:
            st.warning("Enter at least one Folder ID.")
        else:
            prog = st.empty()
            for fid in fids:
                added = [0]
                _walk(fid, drive_service, added, prog)
                st.success(f"Loaded {added[0]} file(s).") if added[0] else st.warning(f"No files found in {fid}.")
            prog.empty()
            with open(CHUNKS_FILE,"wb") as f: pickle.dump(st.session_state["library_chunks"],f)
            st.success(f"Total passages in library: {len(st.session_state['library_chunks'])}")
            st.rerun()

    st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)

    # ── Search Index ──────────────────────────────────────────────────────
    st.markdown("""
    <h2 style="font-family:'Libre Baskerville',serif; font-size:1.1rem; font-weight:700;
        color:#1c2b3a; border-bottom:2px solid #d4820a; padding-bottom:8px; margin-bottom:16px;">
      Search Index
    </h2>
    """, unsafe_allow_html=True)
    st.write(f"Status: **{'Built ✅' if n_embed>0 else 'Not built ❌'}** &nbsp;·&nbsp; {n_embed} embeddings indexed")
    st.caption("Rebuild the index any time you add new documents.")

    if st.button("Build / Rebuild Search Index", type="primary"):
        chunks = st.session_state.get("library_chunks",[])
        if not chunks:
            st.warning("No documents loaded yet.")
        else:
            from openai import OpenAI
            oai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            prog2 = st.progress(0, text="Building index…")
            vecs = []
            for i, ch in enumerate(chunks):
                try:
                    resp = oai.embeddings.create(model="text-embedding-3-small", input=ch["text"])
                    vecs.append(resp.data[0].embedding)
                except: vecs.append(None)
                prog2.progress((i+1)/len(chunks), text=f"Indexing {i+1}/{len(chunks)}…")
            st.session_state["embeddings"] = vecs
            with open(EMBEDDINGS_FILE,"wb") as f: pickle.dump(vecs,f)
            prog2.empty()
            st.success(f"Index built — {len(vecs)} passages indexed.")
            st.rerun()

    st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)

    # ── Articles ──────────────────────────────────────────────────────────
    st.markdown("""
    <h2 style="font-family:'Libre Baskerville',serif; font-size:1.1rem; font-weight:700;
        color:#1c2b3a; border-bottom:2px solid #d4820a; padding-bottom:8px; margin-bottom:16px;">
      Published Articles
    </h2>
    """, unsafe_allow_html=True)
    articles = load_articles()
    if articles:
        for art in sorted(articles, key=lambda a: a.get("created_at",""), reverse=True):
            ca, cb = st.columns([5,1])
            with ca:
                st.markdown(f"""
                <div style="padding:10px 0; border-bottom:1px solid #ddd8d0;">
                  <span style="font-family:'Libre Baskerville',serif; font-size:0.95rem; color:#1c2b3a; font-weight:700;">{art['title']}</span>
                  <span style="font-size:0.75rem; color:#9c9080; margin-left:12px;">{art.get('category','')}</span>
                </div>
                """, unsafe_allow_html=True)
            with cb:
                if st.button("View", key=f"adm_{art['id']}"):
                    st.session_state["open_article_id"] = art["id"]
                    st.switch_page("pages/4_Article.py")
    else:
        st.info("No articles yet. Ask a question to create the first one!")

st.markdown('<div class="ep-footer">Enduring Peace Knowledge Base &nbsp;·&nbsp; Torah\'s roadmap for peace, as articulated by the Lubavitcher Rebbe</div>', unsafe_allow_html=True)
