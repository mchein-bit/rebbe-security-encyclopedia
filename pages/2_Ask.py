import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.styles import apply_global_styles
from utils.ai import generate_article
from utils.storage import add_article, load_articles, search_articles

st.set_page_config(
    page_title="Ask — Rebbe Encyclopedia",
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
    if st.button("Admin / Load Docs", key="nav_admin"):
        st.switch_page("pages/5_Admin.py")

st.markdown("---")

st.markdown("""
<div style="max-width:680px; margin: 32px auto 0; padding: 0 24px;">
  <h1 style="font-family:'Cinzel',serif; font-size:1.8rem; color:#c9a84c; letter-spacing:1px; margin-bottom:6px;">
    Ask a Question
  </h1>
  <p style="color:#6a5f40; font-style:italic; margin-bottom:28px;">
    The AI will search the Rebbe's teachings and write a full encyclopedia article from the sources.
  </p>
</div>
""", unsafe_allow_html=True)

_, col_c, _ = st.columns([1, 3, 1])

with col_c:
    # Pre-fill from homepage if redirected
    default_q = st.session_state.pop("pending_question", "")
    
    question = st.text_input(
        "Your question:",
        value=default_q,
        placeholder="e.g. What did the Rebbe say about the Yom Kippur War?",
    )
    
    # Suggested questions
    st.markdown("""
    <p style="font-size:0.82rem; color:#4a3d28; margin-top:8px; margin-bottom:20px;">
    💡 Try: &nbsp;<em>"What is the 329 Paradigm?"</em> &nbsp;·&nbsp;
    <em>"The Rebbe's view on Operation Litani"</em> &nbsp;·&nbsp;
    <em>"What does Torah say about land for peace?"</em>
    </p>
    """, unsafe_allow_html=True)
    
    generate_btn = st.button("✦ Generate Article", use_container_width=True, type="primary")

# ── Check for existing articles on same topic ─────────────────────────────────
if question and not generate_btn:
    existing = search_articles(question)
    if existing:
        st.markdown('<div style="max-width:680px; margin:24px auto 0; padding: 0 24px;">', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background:#181408; border:1px solid #3a3018; border-left:4px solid #c9a84c; padding:16px 20px; border-radius:2px; margin-bottom:20px;">
          <div style="font-family:'Cinzel',serif; font-size:0.82rem; color:#c9a84c; letter-spacing:0.8px; margin-bottom:10px;">
            SIMILAR ARTICLES ALREADY EXIST
          </div>
          <div style="font-size:0.88rem; color:#7a6d50; font-style:italic; margin-bottom:12px;">
            These articles may already answer your question:
          </div>
        </div>
        """, unsafe_allow_html=True)
        for art in existing[:3]:
            if st.button(f"📖 {art['title']}", key=f"exist_{art['id']}"):
                st.session_state["open_article_id"] = art["id"]
                st.switch_page("pages/4_Article.py")
        st.markdown('</div>', unsafe_allow_html=True)

# ── Generate ──────────────────────────────────────────────────────────────────
if generate_btn and question.strip():
    st.markdown('<div style="max-width:680px; margin:32px auto 0; padding: 0 24px;">', unsafe_allow_html=True)
    
    with st.spinner(""):
        st.markdown("""
        <div class="generating-box">
          <div class="generating-title">✦ Writing Article</div>
          <div class="generating-sub">Searching the Rebbe's teachings and composing the article…</div>
        </div>
        """, unsafe_allow_html=True)
        
        article = generate_article(question.strip())
    
    if article is None:
        st.error("Could not generate the article. Make sure documents are loaded in the Admin panel first.")
    else:
        # Save the article
        article_id = add_article(article)
        st.success(f"✅ Article written and saved to the encyclopedia!")
        
        st.session_state["open_article_id"] = article_id
        st.switch_page("pages/4_Article.py")
    
    st.markdown('</div>', unsafe_allow_html=True)

elif generate_btn and not question.strip():
    st.warning("Please type a question first.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<div class="footer">Built on the Rebbe\'s teachings &nbsp;·&nbsp; Growing with every question asked</div>', unsafe_allow_html=True)
