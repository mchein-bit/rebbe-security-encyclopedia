import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.styles import apply_global_styles
from utils.ai import generate_article
from utils.storage import add_article, search_articles

st.set_page_config(page_title="Ask — Enduring Peace", page_icon="📖", layout="wide", initial_sidebar_state="collapsed")
apply_global_styles()

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
    if st.button("Admin", key="nav_admin", use_container_width=True):
        st.switch_page("pages/5_Admin.py")
with c4:
    st.markdown("")
st.markdown("<hr style='margin:0;'>", unsafe_allow_html=True)

_, mid, _ = st.columns([1, 3, 1])
with mid:
    st.markdown("""
    <div style="padding: 48px 0 32px;">
      <h1 style="font-family:'Libre Baskerville',serif; font-size:1.8rem; font-weight:700;
           color:#1c2b3a; margin-bottom:6px;">Ask a Question</h1>
      <p style="color:#9c9080; font-style:italic; margin-bottom:28px;">
        The AI searches the Rebbe's teachings and writes a full encyclopedia article from the sources.
      </p>
    </div>
    """, unsafe_allow_html=True)

    default_q = st.session_state.pop("pending_question","")
    question = st.text_input("Your question:", value=default_q,
        placeholder="e.g. What did the Rebbe say about the Yom Kippur War?")
    st.markdown("""
    <p style="font-size:0.82rem; color:#9c9080; font-style:italic; margin-top:4px; margin-bottom:20px;">
    Try: "What is the 329 Paradigm?" &nbsp;·&nbsp; "The Rebbe's view on the Sinai withdrawal" &nbsp;·&nbsp; "Operation Litani"
    </p>
    """, unsafe_allow_html=True)
    gen_btn = st.button("Generate Article →", use_container_width=True, type="primary", key="ask_gen")

    # Show similar existing articles
    if question and not gen_btn:
        existing = search_articles(question)
        if existing:
            st.markdown("""
            <div style="background:#fef3e2; border:1px solid #f0d090; border-left:3px solid #d4820a;
                 padding:14px 18px; border-radius:2px; margin-bottom:16px;">
              <div style="font-size:0.72rem; letter-spacing:1.5px; text-transform:uppercase;
                   color:#a86208; margin-bottom:8px;">Similar articles already exist</div>
            </div>
            """, unsafe_allow_html=True)
            for art in existing[:3]:
                if st.button(f"📖  {art['title']}", key=f"exist_{art['id']}"):
                    st.session_state["open_article_id"] = art["id"]
                    st.switch_page("pages/4_Article.py")

    if gen_btn:
        if not question.strip():
            st.warning("Please type a question first.")
        else:
            with st.spinner("Searching the Rebbe's teachings and writing article…"):
                article = generate_article(question.strip())
            if article is None:
                st.error("Could not generate article. Make sure documents are loaded in Admin first.")
            else:
                aid = add_article(article)
                st.session_state["open_article_id"] = aid
                st.switch_page("pages/4_Article.py")

st.markdown('<div class="ep-footer">Enduring Peace Knowledge Base &nbsp;·&nbsp; Torah\'s roadmap for peace, as articulated by the Lubavitcher Rebbe</div>', unsafe_allow_html=True)
