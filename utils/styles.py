import streamlit as st

def apply_global_styles():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Source+Serif+4:ital,opsz,wght@0,8..60,300;0,8..60,400;0,8..60,600;0,8..60,700;1,8..60,400&display=swap');

:root {
  --bg:           #f5f2ed;
  --bg2:          #efecea;
  --bg3:          #e8e4de;
  --white:        #ffffff;
  --amber:        #d4820a;
  --amber-light:  #e8a020;
  --amber-dark:   #a86208;
  --amber-pale:   #fef3e2;
  --text:         #1a1a1a;
  --text-mid:     #3d3830;
  --text-muted:   #6b6458;
  --text-dim:     #9c9080;
  --border:       #ddd8d0;
  --border2:      #ccc6bc;
  --navy:         #1c2b3a;
  --shadow:       rgba(0,0,0,0.08);
  --shadow-md:    rgba(0,0,0,0.14);
}

html, body, [class*="css"] {
  font-family: 'Source Serif 4', Georgia, serif;
  background-color: var(--bg) !important;
  color: var(--text);
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stSidebar"] { display: none; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── NAVBAR ──────────────────────────────── */
.ep-nav {
  background: var(--white);
  border-bottom: 1px solid var(--border);
  padding: 0 40px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 60px;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 1px 4px var(--shadow);
}
.ep-nav-brand {
  display: flex;
  flex-direction: column;
  line-height: 1.1;
}
.ep-nav-super {
  font-family: 'Source Serif 4', serif;
  font-size: 0.65rem;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--text-dim);
}
.ep-nav-title {
  font-family: 'Libre Baskerville', serif;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--navy);
  letter-spacing: 0.2px;
}
.ep-nav-links {
  display: flex;
  gap: 28px;
  align-items: center;
}
.ep-nav-link {
  font-family: 'Source Serif 4', serif;
  font-size: 0.88rem;
  color: var(--text-muted);
  letter-spacing: 0.3px;
  cursor: pointer;
  transition: color 0.15s;
  border: none;
  background: none;
}
.ep-nav-link:hover { color: var(--amber); }

/* ── HERO ────────────────────────────────── */
.ep-hero {
  background: var(--white);
  border-bottom: 1px solid var(--border);
  padding: 56px 40px 48px;
  max-width: 780px;
  margin: 0 auto;
  text-align: left;
}
.ep-hero-super {
  font-family: 'Source Serif 4', serif;
  font-size: 0.72rem;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  color: var(--amber);
  margin-bottom: 14px;
  display: block;
}
.ep-hero-title {
  font-family: 'Libre Baskerville', serif;
  font-size: clamp(1.8rem, 4vw, 2.8rem);
  font-weight: 700;
  color: var(--navy);
  line-height: 1.2;
  margin: 0 0 16px 0;
  letter-spacing: -0.3px;
}
.ep-hero-desc {
  font-size: 1.1rem;
  color: var(--text-muted);
  line-height: 1.75;
  max-width: 560px;
  margin: 0 0 28px 0;
}
.ep-hero-divider {
  width: 48px;
  height: 3px;
  background: var(--amber);
  margin-bottom: 28px;
}

/* ── ASK BOX ─────────────────────────────── */
.ep-ask-box {
  background: var(--amber-pale);
  border: 1px solid #f0d090;
  border-radius: 4px;
  padding: 24px 28px;
  margin: 32px 0 0;
}
.ep-ask-label {
  font-family: 'Source Serif 4', serif;
  font-size: 0.78rem;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: var(--amber-dark);
  margin-bottom: 10px;
  display: block;
}
.ep-suggestion {
  font-size: 0.82rem;
  color: var(--text-dim);
  font-style: italic;
  margin-top: 8px;
}

/* ── SECTION HEADERS ─────────────────────── */
.ep-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 48px 40px 16px;
}
.ep-section-title {
  font-family: 'Libre Baskerville', serif;
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--navy);
  margin: 0 0 6px 0;
  letter-spacing: -0.2px;
}
.ep-section-sub {
  font-size: 0.88rem;
  color: var(--text-dim);
  margin-bottom: 24px;
}
.ep-count {
  font-size: 0.85rem;
  color: var(--text-dim);
  font-style: italic;
  margin-bottom: 20px;
}
.ep-count strong { color: var(--amber-dark); }

/* ── ARTICLE CARDS ───────────────────────── */
.ep-card {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: 3px;
  overflow: hidden;
  transition: box-shadow 0.2s, transform 0.2s;
  margin-bottom: 4px;
}
.ep-card:hover {
  box-shadow: 0 4px 16px var(--shadow-md);
  transform: translateY(-2px);
}
.ep-card-img {
  width: 100%;
  height: 160px;
  background: var(--bg3);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  color: var(--border2);
  border-bottom: 1px solid var(--border);
}
.ep-card-body { padding: 18px 18px 14px; }
.ep-card-tag {
  font-size: 0.68rem;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: var(--amber);
  font-family: 'Source Serif 4', serif;
  margin-bottom: 7px;
}
.ep-card-title {
  font-family: 'Libre Baskerville', serif;
  font-size: 1rem;
  font-weight: 700;
  color: var(--navy);
  line-height: 1.3;
  margin-bottom: 8px;
}
.ep-card-excerpt {
  font-size: 0.88rem;
  color: var(--text-muted);
  line-height: 1.6;
  margin-bottom: 12px;
}
.ep-card-read {
  font-size: 0.8rem;
  color: var(--amber-dark);
  font-family: 'Source Serif 4', serif;
  letter-spacing: 0.3px;
}

/* ── CATEGORY CARDS ──────────────────────── */
.ep-cat-card {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: 3px;
  padding: 20px 18px;
  margin-bottom: 4px;
  border-top: 3px solid var(--amber);
  transition: box-shadow 0.2s;
}
.ep-cat-card:hover { box-shadow: 0 3px 12px var(--shadow); }
.ep-cat-icon { font-size: 1.5rem; margin-bottom: 8px; }
.ep-cat-name {
  font-family: 'Libre Baskerville', serif;
  font-size: 0.88rem;
  font-weight: 700;
  color: var(--navy);
  margin-bottom: 4px;
  line-height: 1.3;
}
.ep-cat-count { font-size: 0.78rem; color: var(--text-dim); }

/* ── BROWSE ROW ──────────────────────────── */
.ep-browse-row {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: 3px;
  padding: 18px 20px;
  margin-bottom: 8px;
  transition: box-shadow 0.15s;
}
.ep-browse-row:hover { box-shadow: 0 2px 8px var(--shadow); }
.ep-browse-tag {
  font-size: 0.68rem;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: var(--amber);
  margin-bottom: 5px;
}
.ep-browse-title {
  font-family: 'Libre Baskerville', serif;
  font-size: 1rem;
  font-weight: 700;
  color: var(--navy);
  margin-bottom: 5px;
}
.ep-browse-summary {
  font-size: 0.88rem;
  color: var(--text-muted);
  line-height: 1.6;
  font-style: italic;
}

/* ── ARTICLE PAGE ────────────────────────── */
.ep-article-wrap {
  max-width: 900px;
  margin: 0 auto;
  padding: 48px 40px 80px;
}
.ep-article-cat {
  display: inline-block;
  font-size: 0.68rem;
  letter-spacing: 1.8px;
  text-transform: uppercase;
  color: var(--amber-dark);
  border: 1px solid #f0d090;
  background: var(--amber-pale);
  padding: 3px 10px;
  border-radius: 2px;
  margin-bottom: 16px;
  font-family: 'Source Serif 4', serif;
}
.ep-article-h1 {
  font-family: 'Libre Baskerville', serif;
  font-size: clamp(1.6rem, 3.5vw, 2.4rem);
  font-weight: 700;
  color: var(--navy);
  line-height: 1.2;
  margin: 0 0 14px 0;
  letter-spacing: -0.3px;
}
.ep-article-meta {
  font-size: 0.82rem;
  color: var(--text-dim);
  padding-bottom: 20px;
  border-bottom: 2px solid var(--amber);
  margin-bottom: 28px;
}
.ep-article-built-on {
  font-size: 0.78rem;
  color: var(--amber-dark);
  font-style: italic;
  margin-top: 6px;
}
.ep-article-lead {
  font-size: 1.15rem;
  line-height: 1.85;
  color: var(--text-mid);
  border-left: 4px solid var(--amber);
  padding-left: 20px;
  margin-bottom: 36px;
  font-style: italic;
}
.ep-article-section { margin-bottom: 36px; }
.ep-article-section h2 {
  font-family: 'Libre Baskerville', serif;
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--navy);
  border-bottom: 1px solid var(--border);
  padding-bottom: 8px;
  margin-bottom: 16px;
  letter-spacing: -0.1px;
}
.ep-article-body {
  font-size: 1.05rem;
  line-height: 1.9;
  color: var(--text);
}
.ep-article-body p { margin-bottom: 16px; }

.ep-quote {
  background: var(--bg2);
  border-left: 4px solid var(--amber);
  padding: 18px 22px;
  margin: 24px 0;
  border-radius: 0 3px 3px 0;
}
.ep-quote-text {
  font-size: 1.05rem;
  line-height: 1.8;
  color: var(--text-mid);
  font-style: italic;
  margin-bottom: 8px;
}
.ep-quote-source {
  font-size: 0.8rem;
  color: var(--text-dim);
  font-style: normal;
  letter-spacing: 0.3px;
}

.ep-footnote {
  font-size: 0.82rem;
  color: var(--text-dim);
  line-height: 1.6;
  padding: 5px 0;
  border-bottom: 1px solid var(--border);
}
.ep-footnote-num { color: var(--amber-dark); margin-right: 6px; font-weight: 700; }

.ep-further-link {
  display: block;
  font-size: 0.9rem;
  color: var(--amber-dark);
  text-decoration: none;
  padding: 5px 0;
  border-bottom: 1px solid var(--border);
  transition: color 0.15s;
}
.ep-further-link:hover { color: var(--amber); }

/* ── SIDEBAR (article page) ──────────────── */
.ep-sidebar { padding: 48px 0 0 28px; }
.ep-sidebar-header {
  font-family: 'Libre Baskerville', serif;
  font-size: 0.72rem;
  letter-spacing: 1.8px;
  text-transform: uppercase;
  color: var(--text-dim);
  border-bottom: 2px solid var(--amber);
  padding-bottom: 6px;
  margin-bottom: 14px;
}
.ep-rel-card {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: 3px;
  padding: 12px 14px;
  margin-bottom: 8px;
  transition: border-color 0.15s;
}
.ep-rel-card:hover { border-color: var(--amber); }
.ep-rel-tag { font-size: 0.65rem; color: var(--text-dim); letter-spacing: 1px; text-transform: uppercase; margin-bottom: 4px; }
.ep-rel-title {
  font-family: 'Libre Baskerville', serif;
  font-size: 0.88rem;
  color: var(--navy);
  font-weight: 700;
  line-height: 1.3;
}

/* ── DIG DEEPER ──────────────────────────── */
.ep-dig-box {
  background: var(--amber-pale);
  border: 1px solid #f0d090;
  border-radius: 3px;
  padding: 16px 16px 12px;
  margin-bottom: 24px;
}
.ep-dig-label {
  font-size: 0.7rem;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: var(--amber-dark);
  margin-bottom: 8px;
  display: block;
}

/* ── BUTTONS ─────────────────────────────── */
.stButton > button {
  background: transparent !important;
  border: 1px solid var(--border2) !important;
  color: var(--text-mid) !important;
  font-family: 'Source Serif 4', serif !important;
  font-size: 0.82rem !important;
  border-radius: 2px !important;
  padding: 7px 14px !important;
  transition: all 0.15s !important;
  letter-spacing: 0.2px !important;
}
.stButton > button:hover {
  border-color: var(--amber) !important;
  color: var(--amber-dark) !important;
  background: var(--amber-pale) !important;
}
.stButton > button[kind="primary"] {
  background: var(--amber) !important;
  border-color: var(--amber) !important;
  color: var(--white) !important;
  font-weight: 600 !important;
}
.stButton > button[kind="primary"]:hover {
  background: var(--amber-dark) !important;
  border-color: var(--amber-dark) !important;
}

/* ── INPUTS ──────────────────────────────── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
  background: var(--white) !important;
  border: 1px solid var(--border2) !important;
  color: var(--text) !important;
  font-family: 'Source Serif 4', serif !important;
  font-size: 1rem !important;
  border-radius: 2px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
  border-color: var(--amber) !important;
  box-shadow: 0 0 0 2px rgba(212,130,10,0.12) !important;
}
::placeholder { color: var(--text-dim) !important; }

/* ── SELECT ──────────────────────────────── */
.stSelectbox > div > div {
  background: var(--white) !important;
  border-color: var(--border2) !important;
  color: var(--text) !important;
  font-family: 'Source Serif 4', serif !important;
}

/* ── ALERTS ──────────────────────────────── */
.stAlert {
  background: var(--bg2) !important;
  border-color: var(--border) !important;
  color: var(--text-muted) !important;
  border-radius: 2px !important;
}

/* ── EXPANDER ────────────────────────────── */
details { border-color: var(--border) !important; background: var(--white) !important; border-radius: 2px !important; }
summary { color: var(--navy) !important; font-family: 'Libre Baskerville', serif !important; font-size: 0.88rem !important; }

/* ── DIVIDER ─────────────────────────────── */
hr { border-color: var(--border) !important; }

/* ── FOOTER ──────────────────────────────── */
.ep-footer {
  text-align: center;
  padding: 32px 24px 48px;
  color: var(--text-dim);
  font-size: 0.82rem;
  border-top: 1px solid var(--border);
  margin-top: 48px;
  background: var(--white);
}
.ep-footer a { color: var(--amber-dark); text-decoration: none; }

/* ── GENERATING BOX ──────────────────────── */
.ep-generating {
  background: var(--white);
  border: 1px solid var(--border);
  border-top: 3px solid var(--amber);
  border-radius: 3px;
  padding: 28px 28px;
  text-align: center;
  margin: 32px auto;
  max-width: 480px;
}
.ep-generating-title {
  font-family: 'Libre Baskerville', serif;
  font-size: 1rem;
  color: var(--navy);
  margin-bottom: 6px;
}
.ep-generating-sub { color: var(--text-dim); font-style: italic; font-size: 0.9rem; }

/* ── ADMIN STATS ─────────────────────────── */
.ep-stat-box {
  background: var(--white);
  border: 1px solid var(--border);
  border-top: 3px solid var(--amber);
  border-radius: 3px;
  padding: 20px 24px;
  text-align: center;
}
.ep-stat-num {
  font-family: 'Libre Baskerville', serif;
  font-size: 2rem;
  font-weight: 700;
  color: var(--navy);
}
.ep-stat-label {
  font-size: 0.72rem;
  color: var(--text-dim);
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-top: 2px;
}
</style>
""", unsafe_allow_html=True)
