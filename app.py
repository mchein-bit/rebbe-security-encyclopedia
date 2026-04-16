import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.storage import load_articles, get_articles_by_category, CATEGORIES, add_article
from utils.styles import apply_global_styles
from utils.ai import generate_article

st.set_page_config(
    page_title="Rebbe's Encyclopedia — Israel & the Middle East",
    page_icon="📖",
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
    "Prophecy & Spiritual Dimensions": "🕊️",
    "Other": "📖",
}

# ── Navbar ────────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
with c1:
    st.markdown("""
    <div class="ep-nav-brand" style="padding:14px 0 10px 0;">
      <span class="ep-nav-super">Torah's Roadmap to Peace in Israel</span>
      <span class="ep-nav-title">Enduring Peace Knowledge Base</span>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown("<div style='margin-top:14px;'></div>", unsafe_allow_html=True)
    if st.button("Browse", key="nav_browse", use_container_width=True):
        st.switch_page("pages/3_Browse.py")
with c3:
    st.markdown("<div style='margin-top:14px;'></div>", unsafe_allow_html=True)
    if st.button("Ask a Question", key="nav_ask", use_container_width=True):
        st.switch_page("pages/2_Ask.py")
with c4:
    st.markdown("<div style='margin-top:14px;'></div>", unsafe_allow_html=True)
    if st.button("Admin", key="nav_admin", use_container_width=True):
        st.switch_page("pages/5_Admin.py")

st.markdown("<hr style='margin:0 0 0 0;'>", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
_, hero_col, _ = st.columns([1, 4, 1])
with hero_col:
    all_articles = load_articles()
    total = len(all_articles)

    st.markdown(f"""
    <div style="padding: 52px 0 40px;">
      <span class="ep-hero-super">Torah's Roadmap to Peace in Israel</span>
      <h1 class="ep-hero-title">Enduring Peace Knowledge Base</h1>
      <div class="ep-hero-divider"></div>
      <p class="ep-hero-desc">
        The Enduring Peace Knowledge Base is a collaborative learning space on Torah's roadmap for
        peace, as articulated by the Lubavitcher Rebbe. A living encyclopedia that grows with every question asked.
      </p>
      <p class="ep-count">Encyclopedia contains <strong>{total}</strong> article{"s" if total != 1 else ""}</p>
    </div>
    """, unsafe_allow_html=True)

    # Ask box
    st.markdown("""
    <div class="ep-ask-box">
      <span class="ep-ask-label">Ask a question — AI writes a full article from the Rebbe's teachings</span>
    </div>
    """, unsafe_allow_html=True)
    question = st.text_input("", placeholder='e.g. "What did the Rebbe say about land for peace?"', label_visibility="collapsed", key="homepage_q")
    st.markdown("""
    <p class="ep-suggestion">Try: "What is the 329 Paradigm?" &nbsp;·&nbsp; "The Rebbe's view on Operation Litani" &nbsp;·&nbsp; "Yom Kippur War"</p>
    """, unsafe_allow_html=True)
    gen_btn = st.button("Generate Article →", use_container_width=True, key="homepage_gen", type="primary")

if gen_btn:
    if not question.strip():
        st.warning("Please type a question first.")
    else:
        _, mid, _ = st.columns([1, 4, 1])
        with mid:
            with st.spinner("Searching the Rebbe's teachings and writing article…"):
                article = generate_article(question.strip())
            if article is None:
                st.error("Could not generate article. Make sure documents are loaded in Admin first.")
            else:
                aid = add_article(article)
                st.session_state["open_article_id"] = aid
                st.switch_page("pages/4_Article.py")

st.markdown("<div style='height:48px'></div>", unsafe_allow_html=True)

# ── Featured / Recent Articles ────────────────────────────────────────────────
if all_articles:
    recent = sorted(all_articles, key=lambda a: a.get("created_at",""), reverse=True)[:3]

    st.markdown("""
    <div style="max-width:1100px; margin:0 auto; padding: 0 40px;">
      <h2 class="ep-section-title">Featured Articles</h2>
      <p class="ep-section-sub">Recently added to the knowledge base</p>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(3)
    for i, art in enumerate(recent):
        cat = art.get("category","Other")
        icon = CAT_ICONS.get(cat,"📖")
        excerpt = art.get("summary","")[:130]
        with cols[i]:
            st.markdown(f"""
            <div class="ep-card">
              <div class="ep-card-img">{icon}</div>
              <div class="ep-card-body">
                <div class="ep-card-tag">{cat}</div>
                <div class="ep-card-title">{art['title']}</div>
                <div class="ep-card-excerpt">{excerpt}…</div>
                <div class="ep-card-read">Read more →</div>
              </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Read Article", key=f"feat_{i}", use_container_width=True):
                st.session_state["open_article_id"] = art["id"]
                st.switch_page("pages/4_Article.py")

    st.markdown("<div style='height:48px'></div>", unsafe_allow_html=True)

# ── Categories ────────────────────────────────────────────────────────────────
st.markdown("""
<div style="max-width:1100px; margin:0 auto; padding: 0 40px;">
  <h2 class="ep-section-title">Browse by Category</h2>
  <p class="ep-section-sub">Explore the Rebbe's teachings by topic</p>
</div>
""", unsafe_allow_html=True)

cat_cols = st.columns(4)
for i, cat in enumerate(CATEGORIES):
    count = len(get_articles_by_category(all_articles, cat))
    icon = CAT_ICONS.get(cat,"📖")
    with cat_cols[i % 4]:
        st.markdown(f"""
        <div class="ep-cat-card">
          <div class="ep-cat-icon">{icon}</div>
          <div class="ep-cat-name">{cat}</div>
          <div class="ep-cat-count">{count} article{"s" if count!=1 else ""}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Browse", key=f"cat_{i}", use_container_width=True):
            st.session_state["browse_category"] = cat
            st.switch_page("pages/3_Browse.py")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ep-footer">
  Enduring Peace Knowledge Base &nbsp;·&nbsp; Torah's roadmap for peace, as articulated by the Lubavitcher Rebbe
</div>
""", unsafe_allow_html=True)
