import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.styles import apply_global_styles
from utils.storage import get_article_by_id, load_articles, find_related_articles

st.set_page_config(
    page_title="Article — Rebbe Encyclopedia",
    page_icon="✡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

apply_global_styles()

CAT_ICONS = {
    "Principles & Halacha": "⚖️",
    "Wars & Military Operations": "🎖️",
    "People": "👤",
    "Diplomacy & Peace Negotiations": "🤝",
    "Territories & Geography": "🗺️",
    "Prophecy & Spiritual Dimensions": "✡️",
    "Other": "📖",
}

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

# ── Load article ──────────────────────────────────────────────────────────────
article_id = st.session_state.get("open_article_id")

if not article_id:
    st.warning("No article selected. Please browse or ask a question.")
    if st.button("← Back to Browse"):
        st.switch_page("pages/3_Browse.py")
    st.stop()

article = get_article_by_id(article_id)

if not article:
    st.error("Article not found.")
    if st.button("← Back to Browse"):
        st.switch_page("pages/3_Browse.py")
    st.stop()

# ── Layout: main + sidebar ────────────────────────────────────────────────────
col_main, col_side = st.columns([3, 1])

with col_main:
    st.markdown('<div class="article-page">', unsafe_allow_html=True)
    
    # ── Header ──────────────────────────────────────────────────────────
    cat = article.get("category", "Other")
    icon = CAT_ICONS.get(cat, "📖")
    date_str = article.get("created_at","")[:10] if article.get("created_at") else ""
    
    st.markdown(f"""
    <div class="article-header">
      <div class="article-category-badge">{icon} {cat}</div>
      <h1 class="article-h1">{article['title']}</h1>
      <div class="article-meta">
        Generated from: {', '.join(article.get('source_docs', [])[:3])}
        {f'&nbsp;·&nbsp; {date_str}' if date_str else ''}
      </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ── Summary / lead ───────────────────────────────────────────────────
    summary = article.get("summary","")
    if summary:
        st.markdown(f'<div class="article-summary-block">{summary}</div>', unsafe_allow_html=True)
    
    # ── Sections ─────────────────────────────────────────────────────────
    sections = article.get("sections", [])
    for sec in sections:
        heading = sec.get("heading","")
        content = sec.get("content","")
        if not content.strip():
            continue
        
        st.markdown(f"""
        <div class="article-section">
          <h2>{heading}</h2>
          <div class="article-body">
        """, unsafe_allow_html=True)
        
        for para in content.split("\n\n"):
            para = para.strip()
            if para:
                st.markdown(f'<p>{para}</p>', unsafe_allow_html=True)
        
        st.markdown('</div></div>', unsafe_allow_html=True)
    
    # ── Rebbe Quotes ──────────────────────────────────────────────────────
    quotes = article.get("rebbe_quotes", [])
    if quotes:
        st.markdown('<div class="article-section"><h2>The Rebbe\'s Words</h2>', unsafe_allow_html=True)
        for q in quotes:
            quote_text = q.get("quote","")
            source = q.get("source","")
            if quote_text:
                st.markdown(f"""
                <div class="rebbe-quote">
                  {quote_text}
                  {f'<span class="quote-source">— {source}</span>' if source else ''}
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ── Footnotes ─────────────────────────────────────────────────────────
    footnotes = article.get("footnotes", [])
    if footnotes:
        with st.expander(f"📚 Sources & Footnotes ({len(footnotes)})"):
            st.markdown('<div class="footnote-list">', unsafe_allow_html=True)
            for i, fn in enumerate(footnotes, 1):
                st.markdown(f'<div class="footnote-item"><span class="footnote-num">{i}.</span>{fn}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # ── Further Reading ───────────────────────────────────────────────────
    further = article.get("further_reading", [])
    if further:
        with st.expander("🔗 Further Reading"):
            for item in further:
                title = item.get("title","")
                url = item.get("url","")
                if url:
                    st.markdown(f'<a class="further-reading-link" href="{url}" target="_blank">↗ {title}</a>', unsafe_allow_html=True)
                elif title:
                    st.markdown(f'<div class="further-reading-link" style="color:#4a3d28; cursor:default;">📖 {title}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # close article-page

# ── Sidebar ───────────────────────────────────────────────────────────────────
with col_side:
    st.markdown('<div style="padding: 32px 0 0 16px;">', unsafe_allow_html=True)
    
    # Related articles
    all_articles = load_articles()
    related = find_related_articles(article, all_articles)
    
    if related:
        st.markdown("""
        <div style="font-family:'Cinzel',serif; font-size:0.75rem; letter-spacing:1.2px; 
             color:#7a6428; text-transform:uppercase; margin-bottom:12px; border-bottom:1px solid #2a2210; padding-bottom:8px;">
          Related Articles
        </div>
        """, unsafe_allow_html=True)
        
        for rel in related:
            rel_cat = rel.get("category","Other")
            rel_icon = CAT_ICONS.get(rel_cat, "📖")
            st.markdown(f"""
            <div style="background:#111008; border:1px solid #2a2210; border-radius:2px; 
                 padding:12px 14px; margin-bottom:8px;">
              <div style="font-size:0.7rem; color:#4a3d28; margin-bottom:4px;">{rel_icon} {rel_cat}</div>
              <div style="font-family:'Cinzel',serif; font-size:0.85rem; color:#c9a84c; line-height:1.35;">
                {rel['title']}
              </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Read", key=f"rel_{rel['id']}", use_container_width=True):
                st.session_state["open_article_id"] = rel["id"]
                st.rerun()
    
    # Ask follow-up
    st.markdown('<div style="margin-top:32px;">', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-family:'Cinzel',serif; font-size:0.75rem; letter-spacing:1.2px; 
         color:#7a6428; text-transform:uppercase; margin-bottom:12px; border-bottom:1px solid #2a2210; padding-bottom:8px;">
      Dig Deeper
    </div>
    """, unsafe_allow_html=True)
    
    followup = st.text_input("", placeholder="Ask a follow-up question…", label_visibility="collapsed", key="followup_q")
    if st.button("✦ Generate Article", key="followup_btn", use_container_width=True):
        if followup.strip():
            st.session_state["pending_question"] = followup.strip()
            st.switch_page("pages/2_Ask.py")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Source docs used
    source_docs = article.get("source_docs", [])
    if source_docs:
        st.markdown('<div style="margin-top:32px;">', unsafe_allow_html=True)
        st.markdown("""
        <div style="font-family:'Cinzel',serif; font-size:0.75rem; letter-spacing:1.2px; 
             color:#7a6428; text-transform:uppercase; margin-bottom:12px; border-bottom:1px solid #2a2210; padding-bottom:8px;">
          Sources Used
        </div>
        """, unsafe_allow_html=True)
        for doc in source_docs:
            st.markdown(f'<div style="font-size:0.78rem; color:#4a3d28; padding:4px 0; border-bottom:1px solid #1a1608;">📄 {doc}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<div class="footer">Built on the Rebbe\'s teachings &nbsp;·&nbsp; Growing with every question asked</div>', unsafe_allow_html=True)
