import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.styles import apply_global_styles
from utils.storage import load_articles, get_articles_by_category, search_articles, CATEGORIES

st.set_page_config(page_title="Browse — Enduring Peace", page_icon="📖", layout="wide", initial_sidebar_state="collapsed")
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
    if st.button("Ask a Question", key="nav_ask", use_container_width=True):
        st.switch_page("pages/2_Ask.py")
with c3:
    st.markdown("<div style='margin-top:6px;'></div>", unsafe_allow_html=True)
    if st.button("Admin", key="nav_admin", use_container_width=True):
        st.switch_page("pages/5_Admin.py")
with c4:
    st.markdown("")
st.markdown("<hr style='margin:0;'>", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
_, main_col, _ = st.columns([1, 5, 1])
with main_col:
    st.markdown("""
    <div style="padding: 40px 0 24px;">
      <h1 style="font-family:'Libre Baskerville',serif; font-size:1.8rem; font-weight:700;
           color:#1c2b3a; margin-bottom:4px;">Browse Articles</h1>
      <p style="color:#9c9080; font-style:italic; margin-bottom:20px;">Search or browse by category</p>
    </div>
    """, unsafe_allow_html=True)

    search_q = st.text_input("", placeholder="Search articles…", label_visibility="collapsed", key="browse_search")

    all_articles = load_articles()

    # Search mode
    if search_q.strip():
        results = search_articles(search_q.strip())
        st.markdown(f"""
        <div style="margin:16px 0; padding:12px 16px; background:#fff; border:1px solid #ddd8d0;
             border-left:3px solid #d4820a; border-radius:2px; font-size:0.88rem; color:#6b6458;">
          {len(results)} result{"s" if len(results)!=1 else ""} for "<strong>{search_q}</strong>"
        </div>
        """, unsafe_allow_html=True)
        articles_to_show = results
    else:
        # Category filter
        default_cat = st.session_state.pop("browse_category", CATEGORIES[0])
        default_idx = CATEGORIES.index(default_cat) if default_cat in CATEGORIES else 0
        selected_cat = st.selectbox("Category:", CATEGORIES, index=default_idx)
        articles_to_show = get_articles_by_category(all_articles, selected_cat)
        icon = CAT_ICONS.get(selected_cat,"📖")
        st.markdown(f"""
        <div style="margin-bottom:20px; font-size:0.78rem; color:#9c9080; letter-spacing:1px; text-transform:uppercase;">
          {icon} {selected_cat} &nbsp;·&nbsp; {len(articles_to_show)} article{"s" if len(articles_to_show)!=1 else ""}
        </div>
        """, unsafe_allow_html=True)

    # Article list
    if not articles_to_show:
        st.markdown("""
        <div style="text-align:center; padding:60px 24px; color:#9c9080;">
          <div style="font-size:2rem; margin-bottom:12px;">📖</div>
          <div style="font-family:'Libre Baskerville',serif; font-size:1rem; color:#6b6458; margin-bottom:8px;">
            No articles yet in this category
          </div>
          <div style="font-style:italic; font-size:0.9rem;">Ask a question to create the first one.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Ask a Question →", type="primary"):
            st.switch_page("pages/2_Ask.py")
    else:
        for art in articles_to_show:
            cat = art.get("category","Other")
            art_icon = CAT_ICONS.get(cat,"📖")
            date_str = art.get("created_at","")[:10] if art.get("created_at") else ""
            col_a, col_b = st.columns([5, 1])
            with col_a:
                st.markdown(f"""
                <div class="ep-browse-row">
                  <div class="ep-browse-tag">{art_icon} {cat} &nbsp;·&nbsp; {date_str}</div>
                  <div class="ep-browse-title">{art['title']}</div>
                  <div class="ep-browse-summary">{art.get('summary','')[:200]}…</div>
                </div>
                """, unsafe_allow_html=True)
            with col_b:
                st.markdown("<div style='margin-top:24px;'></div>", unsafe_allow_html=True)
                if st.button("Read →", key=f"browse_{art['id']}", use_container_width=True):
                    st.session_state["open_article_id"] = art["id"]
                    st.switch_page("pages/4_Article.py")

st.markdown('<div class="ep-footer">Enduring Peace Knowledge Base &nbsp;·&nbsp; Torah\'s roadmap for peace, as articulated by the Lubavitcher Rebbe</div>', unsafe_allow_html=True)
