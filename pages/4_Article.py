import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.styles import apply_global_styles
from utils.storage import get_article_by_id, load_articles, find_related_articles, add_article
from utils.ai import generate_article

st.set_page_config(page_title="Article — Enduring Peace", page_icon="📖", layout="wide", initial_sidebar_state="collapsed")
apply_global_styles()

CAT_ICONS = {
    "Principles & Halacha": "⚖️",
    "Wars & Military Operations": "🎖️",
    "People": "👤",
    "Diplomacy & Peace Negotiations": "🤝",
    "Territories & Geography": "🗺️",
    "Prophecy & Spiritual Dimensions": "🕊️",
    "Other": "📖",
}

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
    st.markdown("<div style='margin-top:6px;'></div>", unsafe_allow_html=True)
    if st.button("Admin", key="nav_admin", use_container_width=True):
        st.switch_page("pages/5_Admin.py")
st.markdown("<hr style='margin:0;'>", unsafe_allow_html=True)

# ── Load article ──────────────────────────────────────────────────────────────
article_id = st.session_state.get("open_article_id")
if not article_id:
    st.warning("No article selected.")
    if st.button("← Browse Articles"): st.switch_page("pages/3_Browse.py")
    st.stop()

article = get_article_by_id(article_id)
if not article:
    st.error("Article not found.")
    if st.button("← Browse Articles"): st.switch_page("pages/3_Browse.py")
    st.stop()

# ── Two-column layout ─────────────────────────────────────────────────────────
col_main, col_side = st.columns([3, 1])

with col_main:
    st.markdown('<div class="ep-article-wrap">', unsafe_allow_html=True)

    cat = article.get("category","Other")
    icon = CAT_ICONS.get(cat,"📖")
    date_str = article.get("created_at","")[:10] if article.get("created_at") else ""
    built_on = article.get("built_on",[])

    st.markdown(f"""
    <div style="margin-bottom:28px; padding-bottom:20px; border-bottom: 2px solid #d4820a;">
      <div class="ep-article-cat">{icon} {cat}</div>
      <h1 class="ep-article-h1">{article['title']}</h1>
      <div class="ep-article-meta">
        Sources: {', '.join(article.get('source_docs',[])[:3])}
        {f'&nbsp;·&nbsp; {date_str}' if date_str else ''}
        {f'<div class="ep-article-built-on">Also drew from: {", ".join(built_on[:2])}</div>' if built_on else ''}
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Summary / lead
    if article.get("summary"):
        st.markdown(f'<div class="ep-article-lead">{article["summary"]}</div>', unsafe_allow_html=True)

    # Sections
    for sec in article.get("sections",[]):
        heading = sec.get("heading","").strip()
        content = sec.get("content","").strip()
        if not content:
            continue
        st.markdown(f'<div class="ep-article-section"><h2>{heading}</h2><div class="ep-article-body">', unsafe_allow_html=True)
        for para in content.split("\n\n"):
            para = para.strip()
            if para:
                st.markdown(f"<p>{para}</p>", unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

    # Rebbe quotes
    quotes = [q for q in article.get("rebbe_quotes",[]) if q.get("quote","").strip()]
    if quotes:
        st.markdown('<div class="ep-article-section"><h2>The Rebbe\'s Words</h2>', unsafe_allow_html=True)
        for q in quotes:
            st.markdown(f"""
            <div class="ep-quote">
              <div class="ep-quote-text">{q['quote']}</div>
              {f'<div class="ep-quote-source">— {q["source"]}</div>' if q.get("source") else ''}
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Footnotes
    footnotes = article.get("footnotes",[])
    if footnotes:
        with st.expander(f"Sources & Footnotes ({len(footnotes)})"):
            for i, fn in enumerate(footnotes, 1):
                st.markdown(f'<div class="ep-footnote"><span class="ep-footnote-num">{i}.</span>{fn}</div>', unsafe_allow_html=True)

    # Further reading — real URLs only
    further = [x for x in article.get("further_reading",[]) if x.get("url","").startswith("http") and x.get("title","").strip()]
    if further:
        with st.expander("Further Reading"):
            for item in further:
                st.markdown(f'<a class="ep-further-link" href="{item["url"]}" target="_blank">↗ {item["title"]}</a>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with col_side:
    st.markdown('<div class="ep-sidebar">', unsafe_allow_html=True)

    # Dig Deeper
    st.markdown("""
    <div class="ep-dig-box">
      <span class="ep-dig-label">Dig Deeper</span>
    </div>
    """, unsafe_allow_html=True)
    followup = st.text_input("", placeholder="Ask a follow-up…", label_visibility="collapsed", key="followup_q")
    if st.button("Generate Article →", key="dig_btn", use_container_width=True, type="primary"):
        if followup.strip():
            with st.spinner("Writing…"):
                new_art = generate_article(followup.strip())
            if new_art:
                new_id = add_article(new_art)
                st.session_state["open_article_id"] = new_id
                st.rerun()
            else:
                st.error("Make sure documents are loaded in Admin.")
        else:
            st.warning("Type a question first.")

    # Related articles
    all_articles = load_articles()
    related = find_related_articles(article, all_articles)
    if related:
        st.markdown('<div class="ep-sidebar-header" style="margin-top:24px;">Related Articles</div>', unsafe_allow_html=True)
        for rel in related:
            rel_icon = CAT_ICONS.get(rel.get("category","Other"),"📖")
            st.markdown(f"""
            <div class="ep-rel-card">
              <div class="ep-rel-tag">{rel_icon} {rel.get('category','')}</div>
              <div class="ep-rel-title">{rel['title']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Read →", key=f"rel_{rel['id']}", use_container_width=True):
                st.session_state["open_article_id"] = rel["id"]
                st.rerun()

    # Sources
    if article.get("source_docs"):
        st.markdown('<div class="ep-sidebar-header" style="margin-top:24px;">Sources Used</div>', unsafe_allow_html=True)
        for doc in article["source_docs"]:
            st.markdown(f'<div style="font-size:0.78rem; color:#9c9080; padding:4px 0; border-bottom:1px solid #ddd8d0;">📄 {doc}</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="ep-footer">Enduring Peace Knowledge Base &nbsp;·&nbsp; Torah\'s roadmap for peace, as articulated by the Lubavitcher Rebbe</div>', unsafe_allow_html=True)
