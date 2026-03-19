import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.storage import load_articles, get_articles_by_category, CATEGORIES, add_article
from utils.styles import apply_global_styles
from utils.ai import generate_article

st.set_page_config(
    page_title="Rebbe Encyclopedia — Israel & the Middle East",
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

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-inner">
    <div class="hero-star">✡</div>
    <h1 class="hero-title">The Rebbe's Encyclopedia</h1>
    <p class="hero-tagline">Israel &amp; the Middle East Through the Lens of Torah</p>
    <p class="hero-desc">
      A living, growing knowledge base of the Lubavitcher Rebbe's teachings —
      rooted in halacha, growing with every question asked.
    </p>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Ask a question — generates RIGHT HERE, no redirect ───────────────────────
st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)

col_l, col_mid, col_r = st.columns([1, 3, 1])
with col_mid:
    st.markdown('<p class="ask-label">Ask a question — the AI will write a full article from the Rebbe\'s teachings</p>', unsafe_allow_html=True)
    question = st.text_input("", placeholder="e.g. What did the Rebbe say about the Sinai withdrawal?", label_visibility="collapsed", key="homepage_q")
    st.markdown("""
    <p style="font-size:0.82rem; color:#4a3d28; margin-top:4px; margin-bottom:12px;">
    💡 Try: <em>"What is the 329 Paradigm?"</em> &nbsp;·&nbsp;
    <em>"The Rebbe's view on Operation Litani"</em> &nbsp;·&nbsp;
    <em>"What does Torah say about land for peace?"</em>
    </p>
    """, unsafe_allow_html=True)
    generate_btn = st.button("✦ Generate Article", use_container_width=True, key="homepage_ask", type="primary")

if generate_btn:
    if not question.strip():
        with col_mid:
            st.warning("Please type a question first.")
    else:
        with col_mid:
            with st.spinner("Searching the Rebbe's teachings and writing article…"):
                article = generate_article(question.strip())
            if article is None:
                st.error("Could not generate the article. Make sure documents are loaded in the Admin panel first.")
            else:
                article_id = add_article(article)
                st.session_state["open_article_id"] = article_id
                st.switch_page("pages/4_Article.py")

# ── Category Browse ───────────────────────────────────────────────────────────
st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">Browse by Category</h2>', unsafe_allow_html=True)

all_articles = load_articles()
total = len(all_articles)
st.markdown(f'<p class="article-count">Encyclopedia contains <strong>{total}</strong> article{"s" if total != 1 else ""}</p>', unsafe_allow_html=True)

cols = st.columns(3)
for i, cat in enumerate(CATEGORIES):
    articles_in_cat = get_articles_by_category(all_articles, cat)
    icon = CAT_ICONS.get(cat, "📖")
    with cols[i % 3]:
        count = len(articles_in_cat)
        st.markdown(f"""
        <div class="cat-card">
          <div class="cat-icon">{icon}</div>
          <div class="cat-name">{cat}</div>
          <div class="cat-count">{count} article{"s" if count != 1 else ""}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Browse {cat.split('&')[0].strip()}", key=f"cat_{i}", use_container_width=True):
            st.session_state["browse_category"] = cat
            st.switch_page("pages/3_Browse.py")

# ── Recent Articles ───────────────────────────────────────────────────────────
if all_articles:
    st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Recently Added Articles</h2>', unsafe_allow_html=True)

    recent = sorted(all_articles, key=lambda a: a.get("created_at", ""), reverse=True)[:6]
    cols2 = st.columns(3)
    for i, art in enumerate(recent):
        with cols2[i % 3]:
            cat = art.get("category", "Other")
            icon = CAT_ICONS.get(cat, "📖")
            st.markdown(f"""
            <div class="article-card">
              <div class="article-cat-tag">{icon} {cat}</div>
              <div class="article-title-card">{art['title']}</div>
              <div class="article-summary-card">{art.get('summary','')[:120]}…</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Read Article →", key=f"recent_{i}", use_container_width=True):
                st.session_state["open_article_id"] = art["id"]
                st.switch_page("pages/4_Article.py")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  <span>Built on the Rebbe's teachings &nbsp;·&nbsp; Growing with every question asked</span>
</div>
""", unsafe_allow_html=True)
