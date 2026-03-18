import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.styles import apply_global_styles
from utils.storage import load_articles, get_articles_by_category, search_articles, CATEGORIES

st.set_page_config(
    page_title="Browse — Rebbe Encyclopedia",
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
    if st.button("Ask a Question", key="nav_ask"):
        st.switch_page("pages/2_Ask.py")
with col_n3:
    if st.button("Admin / Load Docs", key="nav_admin"):
        st.switch_page("pages/5_Admin.py")

st.markdown("---")

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding: 32px 32px 8px;">
  <h1 style="font-family:'Cinzel',serif; font-size:1.8rem; color:#c9a84c; letter-spacing:1px; margin-bottom:4px;">
    Browse Articles
  </h1>
  <p style="color:#6a5f40; font-style:italic;">
    Browse by category or search the entire encyclopedia
  </p>
</div>
""", unsafe_allow_html=True)

# ── Search bar ────────────────────────────────────────────────────────────────
_, col_s, _ = st.columns([1, 4, 1])
with col_s:
    search_q = st.text_input("", placeholder="🔍  Search articles…", label_visibility="collapsed", key="browse_search")

all_articles = load_articles()

# ── Search results ────────────────────────────────────────────────────────────
if search_q.strip():
    results = search_articles(search_q.strip())
    st.markdown(f"""
    <div style="padding: 16px 32px;">
      <span style="font-family:'Cinzel',serif; font-size:0.82rem; color:#c9a84c; letter-spacing:1px;">
        SEARCH RESULTS — {len(results)} article{"s" if len(results)!=1 else ""} found for "{search_q}"
      </span>
    </div>
    """, unsafe_allow_html=True)
    
    if not results:
        st.markdown('<div style="padding:24px 32px; color:#6a5f40; font-style:italic;">No articles found. Try asking a question to create one!</div>', unsafe_allow_html=True)
    else:
        _show_article_list(results)
    
    st.stop()

# ── Category selector ─────────────────────────────────────────────────────────
default_cat = st.session_state.pop("browse_category", CATEGORIES[0])
default_idx = CATEGORIES.index(default_cat) if default_cat in CATEGORIES else 0

selected_cat = st.selectbox(
    "Category:",
    CATEGORIES,
    index=default_idx,
    key="cat_select"
)

cat_articles = get_articles_by_category(all_articles, selected_cat)
icon = CAT_ICONS.get(selected_cat, "📖")

st.markdown(f"""
<div style="padding: 8px 32px 24px;">
  <span style="font-family:'Cinzel',serif; font-size:0.82rem; color:#c9a84c; letter-spacing:1px;">
    {icon} {selected_cat.upper()} — {len(cat_articles)} article{"s" if len(cat_articles)!=1 else ""}
  </span>
</div>
""", unsafe_allow_html=True)

def _show_article_list(articles):
    if not articles:
        col_e1, col_e2, col_e3 = st.columns([1,3,1])
        with col_e2:
            st.markdown("""
            <div style="text-align:center; padding:48px 24px; color:#4a3d28;">
              <div style="font-size:2rem; margin-bottom:12px;">📖</div>
              <div style="font-family:'Cinzel',serif; color:#6a5028; font-size:0.9rem; letter-spacing:0.8px; margin-bottom:8px;">
                NO ARTICLES YET IN THIS CATEGORY
              </div>
              <div style="font-style:italic; font-size:0.88rem;">
                Ask a question to create the first article here.
              </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("✦ Ask a Question", use_container_width=True, type="primary"):
                st.switch_page("pages/2_Ask.py")
        return
    
    for art in articles:
        col_a, col_b = st.columns([5, 1])
        with col_a:
            cat = art.get("category", "Other")
            badge_icon = CAT_ICONS.get(cat, "📖")
            date_str = art.get("created_at","")[:10] if art.get("created_at") else ""
            st.markdown(f"""
            <div class="browse-article-row">
              <div style="flex:1;">
                <div style="font-size:0.72rem; color:#4a3d28; margin-bottom:4px;">
                  {badge_icon} {cat} &nbsp;·&nbsp; {date_str}
                </div>
                <div class="browse-article-title">{art['title']}</div>
                <div class="browse-article-summary">{art.get('summary','')[:180]}…</div>
              </div>
            </div>
            """, unsafe_allow_html=True)
        with col_b:
            if st.button("Read →", key=f"browse_read_{art['id']}", use_container_width=True):
                st.session_state["open_article_id"] = art["id"]
                st.switch_page("pages/4_Article.py")

_show_article_list(cat_articles)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<div class="footer">Built on the Rebbe\'s teachings &nbsp;·&nbsp; Growing with every question asked</div>', unsafe_allow_html=True)
