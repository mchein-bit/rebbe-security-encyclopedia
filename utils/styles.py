import streamlit as st

def apply_global_styles():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,600;0,800;1,400;1,600&family=Cinzel:wght@400;600;900&display=swap');

:root {
  --gold:       #c9a84c;
  --gold-light: #e8c97a;
  --gold-dim:   #7a5f28;
  --bg:         #0b0b0b;
  --bg2:        #111008;
  --bg3:        #181408;
  --border:     #2a2210;
  --border2:    #3a3018;
  --text:       #e4d9c0;
  --text-muted: #8a7d60;
  --text-dim:   #4a4230;
  --red-dim:    #6b1a1a;
}

html, body, [class*="css"] {
  font-family: 'EB Garamond', Georgia, serif;
  background-color: var(--bg) !important;
  color: var(--text);
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stSidebar"] { display: none; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── HERO ──────────────────────────── */
.hero {
  background: linear-gradient(170deg, #1a1200 0%, #0e0c04 50%, #0b0b0b 100%);
  border-bottom: 1px solid var(--border2);
  padding: 72px 24px 56px;
  text-align: center;
  position: relative;
  overflow: hidden;
}
.hero::before {
  content: '';
  position: absolute; inset: 0;
  background: radial-gradient(ellipse 60% 40% at 50% 0%, rgba(201,168,76,0.07) 0%, transparent 70%);
  pointer-events: none;
}
.hero-star {
  font-size: 2.2rem;
  color: var(--gold);
  opacity: 0.7;
  margin-bottom: 12px;
}
.hero-title {
  font-family: 'Cinzel', serif;
  font-size: clamp(2rem, 5vw, 3.4rem);
  font-weight: 900;
  color: var(--gold-light);
  margin: 0 0 10px 0;
  letter-spacing: 2px;
  line-height: 1.15;
}
.hero-tagline {
  font-family: 'EB Garamond', serif;
  font-style: italic;
  font-size: 1.25rem;
  color: var(--gold-dim);
  margin: 0 0 18px 0;
  letter-spacing: 0.5px;
}
.hero-desc {
  font-size: 1.05rem;
  color: var(--text-muted);
  max-width: 560px;
  margin: 0 auto;
  line-height: 1.7;
}

/* ── ASK LABEL ─────────────────────── */
.ask-label {
  text-align: center;
  color: var(--text-muted);
  font-style: italic;
  font-size: 1rem;
  margin-bottom: 10px;
}

/* ── SECTION ───────────────────────── */
.section-gap { height: 48px; }
.section-title {
  font-family: 'Cinzel', serif;
  font-size: 1.3rem;
  font-weight: 600;
  color: var(--gold);
  letter-spacing: 1.5px;
  text-transform: uppercase;
  margin: 0 0 6px 0;
  padding: 0 24px;
  border-left: 3px solid var(--gold-dim);
  margin-left: 8px;
}
.article-count {
  color: var(--text-muted);
  font-size: 0.9rem;
  font-style: italic;
  padding-left: 8px;
  margin-bottom: 20px;
}
.article-count strong { color: var(--gold); }

/* ── CATEGORY CARDS ────────────────── */
.cat-card {
  background: linear-gradient(160deg, var(--bg3), var(--bg2));
  border: 1px solid var(--border);
  border-radius: 3px;
  padding: 22px 18px 14px;
  margin-bottom: 8px;
  text-align: center;
  transition: border-color 0.2s;
}
.cat-card:hover { border-color: var(--gold-dim); }
.cat-icon { font-size: 1.8rem; margin-bottom: 8px; }
.cat-name {
  font-family: 'Cinzel', serif;
  font-size: 0.82rem;
  color: var(--gold);
  letter-spacing: 0.8px;
  font-weight: 600;
  margin-bottom: 4px;
}
.cat-count { font-size: 0.8rem; color: var(--text-dim); }

/* ── ARTICLE CARDS ──────────────────── */
.article-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-left: 3px solid var(--gold-dim);
  border-radius: 2px;
  padding: 18px 16px 14px;
  margin-bottom: 8px;
  min-height: 130px;
}
.article-cat-tag {
  font-size: 0.72rem;
  color: var(--text-dim);
  text-transform: uppercase;
  letter-spacing: 0.8px;
  margin-bottom: 8px;
}
.article-title-card {
  font-family: 'Cinzel', serif;
  font-size: 0.95rem;
  color: var(--gold-light);
  font-weight: 600;
  margin-bottom: 8px;
  line-height: 1.35;
}
.article-summary-card {
  font-size: 0.88rem;
  color: var(--text-muted);
  line-height: 1.6;
  font-style: italic;
}

/* ── BUTTONS ────────────────────────── */
.stButton > button {
  background: transparent !important;
  border: 1px solid var(--border2) !important;
  color: var(--gold) !important;
  font-family: 'Cinzel', serif !important;
  font-size: 0.78rem !important;
  letter-spacing: 0.8px !important;
  border-radius: 2px !important;
  padding: 8px 16px !important;
  transition: all 0.2s !important;
}
.stButton > button:hover {
  background: var(--bg3) !important;
  border-color: var(--gold) !important;
  color: var(--gold-light) !important;
}

/* Primary button override */
.stButton > button[kind="primary"] {
  background: linear-gradient(135deg, #2e2200, #4a3800) !important;
  border-color: var(--gold-dim) !important;
  color: var(--gold-light) !important;
}
.stButton > button[kind="primary"]:hover {
  background: linear-gradient(135deg, #4a3800, #6a5200) !important;
  border-color: var(--gold) !important;
}

/* ── INPUTS ─────────────────────────── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
  background: var(--bg3) !important;
  border: 1px solid var(--border2) !important;
  color: var(--text) !important;
  font-family: 'EB Garamond', serif !important;
  font-size: 1.05rem !important;
  border-radius: 2px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
  border-color: var(--gold-dim) !important;
  box-shadow: 0 0 0 2px rgba(201,168,76,0.12) !important;
}
::placeholder { color: var(--text-dim) !important; }

/* ── SELECT BOX ──────────────────────── */
.stSelectbox > div > div {
  background: var(--bg3) !important;
  border-color: var(--border2) !important;
  color: var(--text) !important;
  font-family: 'EB Garamond', serif !important;
}

/* ── ARTICLE PAGE ────────────────────── */
.article-page { max-width: 860px; margin: 0 auto; padding: 48px 24px 80px; }
.article-header { margin-bottom: 32px; border-bottom: 1px solid var(--border2); padding-bottom: 28px; }
.article-category-badge {
  display: inline-block;
  font-family: 'Cinzel', serif;
  font-size: 0.72rem;
  letter-spacing: 1.2px;
  color: var(--gold-dim);
  text-transform: uppercase;
  border: 1px solid var(--border2);
  padding: 3px 10px;
  border-radius: 20px;
  margin-bottom: 16px;
}
.article-h1 {
  font-family: 'Cinzel', serif;
  font-size: clamp(1.6rem, 4vw, 2.6rem);
  font-weight: 900;
  color: var(--gold-light);
  line-height: 1.2;
  margin: 0 0 16px 0;
  letter-spacing: 0.5px;
}
.article-meta { font-size: 0.83rem; color: var(--text-dim); font-style: italic; }

.article-summary-block {
  background: linear-gradient(135deg, var(--bg3), var(--bg2));
  border-left: 4px solid var(--gold);
  padding: 20px 24px;
  margin-bottom: 36px;
  font-size: 1.1rem;
  font-style: italic;
  color: var(--text-muted);
  line-height: 1.75;
  border-radius: 0 3px 3px 0;
}

.article-section { margin-bottom: 36px; }
.article-section h2 {
  font-family: 'Cinzel', serif;
  font-size: 1.05rem;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: var(--gold);
  border-bottom: 1px solid var(--border);
  padding-bottom: 8px;
  margin-bottom: 16px;
}
.article-section h3 {
  font-family: 'Cinzel', serif;
  font-size: 0.9rem;
  letter-spacing: 1px;
  color: var(--gold-dim);
  margin-bottom: 10px;
  margin-top: 24px;
}
.article-body {
  font-size: 1.08rem;
  line-height: 1.9;
  color: var(--text);
}
.article-body p { margin-bottom: 16px; }

.rebbe-quote {
  background: var(--bg3);
  border-left: 4px solid var(--gold-dim);
  border-right: 1px solid var(--border);
  border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
  padding: 18px 22px;
  margin: 24px 0;
  font-style: italic;
  color: var(--text-muted);
  font-size: 1.05rem;
  line-height: 1.8;
  border-radius: 0 3px 3px 0;
  position: relative;
}
.rebbe-quote::before {
  content: '"';
  position: absolute;
  top: -8px; left: 12px;
  font-size: 2.5rem;
  color: var(--gold-dim);
  font-family: 'Cinzel', serif;
  line-height: 1;
}
.quote-source {
  display: block;
  margin-top: 10px;
  font-size: 0.8rem;
  color: var(--text-dim);
  font-style: normal;
  letter-spacing: 0.3px;
}

.footnote-list { margin-top: 8px; }
.footnote-item {
  font-size: 0.82rem;
  color: var(--text-dim);
  line-height: 1.6;
  padding: 4px 0;
  border-bottom: 1px solid var(--border);
}
.footnote-num { color: var(--gold-dim); margin-right: 6px; }

.related-article-link {
  display: block;
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 2px;
  padding: 12px 14px;
  margin-bottom: 8px;
  font-size: 0.9rem;
  color: var(--text-muted);
  transition: border-color 0.2s;
}
.related-article-link:hover { border-color: var(--gold-dim); color: var(--gold); }

.further-reading-link {
  display: block;
  font-size: 0.9rem;
  color: var(--gold-dim);
  text-decoration: none;
  margin-bottom: 6px;
  transition: color 0.2s;
}

/* ── NAV BAR ─────────────────────────── */
.navbar {
  display: flex;
  align-items: center;
  gap: 32px;
  padding: 14px 32px;
  background: var(--bg2);
  border-bottom: 1px solid var(--border);
  position: sticky; top: 0; z-index: 100;
}
.navbar-brand {
  font-family: 'Cinzel', serif;
  font-size: 1rem;
  font-weight: 900;
  color: var(--gold);
  letter-spacing: 1px;
  white-space: nowrap;
}
.navbar-link {
  font-family: 'Cinzel', serif;
  font-size: 0.75rem;
  letter-spacing: 0.8px;
  color: var(--text-dim);
  text-transform: uppercase;
  cursor: pointer;
  transition: color 0.2s;
}
.navbar-link:hover { color: var(--gold); }

/* ── BROWSE PAGE ─────────────────────── */
.browse-article-row {
  display: flex;
  gap: 16px;
  align-items: flex-start;
  padding: 18px 0;
  border-bottom: 1px solid var(--border);
}
.browse-article-title {
  font-family: 'Cinzel', serif;
  font-size: 1rem;
  color: var(--gold-light);
  font-weight: 600;
  margin-bottom: 5px;
}
.browse-article-summary {
  font-size: 0.9rem;
  color: var(--text-muted);
  font-style: italic;
  line-height: 1.6;
}

/* ── GENERATING SPINNER ──────────────── */
.generating-box {
  background: var(--bg3);
  border: 1px solid var(--border2);
  border-left: 4px solid var(--gold);
  border-radius: 3px;
  padding: 28px 28px;
  text-align: center;
  margin: 32px auto;
  max-width: 540px;
}
.generating-title {
  font-family: 'Cinzel', serif;
  font-size: 1.1rem;
  color: var(--gold);
  letter-spacing: 1px;
  margin-bottom: 8px;
}
.generating-sub { color: var(--text-muted); font-style: italic; font-size: 0.95rem; }

/* ── FOOTER ──────────────────────────── */
.footer {
  text-align: center;
  padding: 32px 24px 48px;
  color: var(--text-dim);
  font-size: 0.82rem;
  letter-spacing: 0.5px;
  border-top: 1px solid var(--border);
  margin-top: 48px;
}

/* ── ALERTS ──────────────────────────── */
.stAlert { background: var(--bg3) !important; border-color: var(--border2) !important; color: var(--text-muted) !important; }

/* ── EXPANDER ────────────────────────── */
.stExpander { border-color: var(--border) !important; background: var(--bg2) !important; }
.stExpander summary { color: var(--gold) !important; font-family: 'Cinzel', serif !important; font-size: 0.85rem !important; letter-spacing: 0.5px !important; }
</style>
""", unsafe_allow_html=True)
