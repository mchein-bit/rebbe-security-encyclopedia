import os
import json
import pickle
import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Always use the repo root directory for data files, no matter which page loads this
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHUNKS_FILE = os.path.join(ROOT_DIR, "library_chunks.pkl")
EMBEDDINGS_FILE = os.path.join(ROOT_DIR, "embeddings.pkl")

ARTICLE_SYSTEM_PROMPT = """You are a senior scholar writing for the Rebbe's Encyclopedia — a Grokipedia-style knowledge base of the Lubavitcher Rebbe's teachings on Israel, security, and the Middle East as grounded in Torah.

TONE & STYLE:
- Encyclopedic, dignified, scholarly — like a well-sourced Wikipedia article meets a Torah journal
- Draw ONLY from the provided source passages. Never invent quotes or facts.
- When quoting the Rebbe, preserve his exact words and cite the source (date/occasion if available)
- Be factually precise — if sources don't cover something, say so honestly

ARTICLE LENGTH & STRUCTURE — use your judgment:
- Let the content dictate the length. A rich topic with many sources deserves a long, detailed article. A narrow topic may only need a few paragraphs. Never pad or repeat.
- Choose section headings that make sense for THIS specific topic. Don't force every article into the same mold.
- Good examples of headings depending on topic: "Overview", "Historical Background", "The Halachic Principle", "The Rebbe's Position", "Key Events", "The Rebbe's Critique", "Spiritual Dimensions", "Counterarguments", "Legacy & Significance", "The Rebbe's Words" — use only what fits.
- A short focused article (2-3 sections) is better than a long padded one.
- A deeply documented topic should have many sections, subsections, and quotes.

FURTHER READING — only include if the sources themselves mention specific books, articles, or websites. If no real sources are mentioned, return an empty array []. Never invent titles or URLs.

Return ONLY valid JSON. No markdown fences, no preamble. Just the raw JSON object.

JSON structure:
{
  "title": "Clear encyclopedic title",
  "category": "One of: Principles & Halacha | Wars & Military Operations | People | Diplomacy & Peace Negotiations | Territories & Geography | Prophecy & Spiritual Dimensions | Other",
  "summary": "2-4 sentence lead paragraph summarizing the article",
  "sections": [
    {
      "heading": "Choose a heading that fits this specific article",
      "content": "Prose paragraphs separated by double newlines. Write as much or as little as the content warrants."
    }
  ],
  "rebbe_quotes": [
    {
      "quote": "Exact quote only — never paraphrase here",
      "source": "Date, occasion, letter, or talk if known"
    }
  ],
  "footnotes": [
    "Only real citations found in the source passages"
  ],
  "further_reading": [],
  "keywords": ["keyword1", "keyword2"]
}
"""

def _get_embedding(text: str):
    try:
        resp = client.embeddings.create(model="text-embedding-3-small", input=text)
        return resp.data[0].embedding
    except Exception:
        return None

def _cosine_similarity(a, b):
    if not a or not b:
        return 0
    dot = sum(x * y for x, y in zip(a, b))
    na = sum(x*x for x in a)**0.5
    nb = sum(x*x for x in b)**0.5
    if na == 0 or nb == 0:
        return 0
    return dot / (na * nb)

def search_chunks(query: str, top_k: int = 14):
    chunks = st.session_state.get("library_chunks", [])
    embeddings = st.session_state.get("embeddings", [])
    
    if not chunks:
        return []
    
    if embeddings and len(embeddings) == len(chunks):
        q_vec = _get_embedding(query)
        if q_vec:
            scored = [
                (_cosine_similarity(q_vec, vec), ch)
                for ch, vec in zip(chunks, embeddings) if vec
            ]
            scored.sort(key=lambda x: x[0], reverse=True)
            return [c for _, c in scored[:top_k]]
    
    # keyword fallback
    q_low = query.lower()
    return [ch for ch in chunks if q_low in ch["text"].lower()][:top_k]

def _search_published_articles(question: str, top_k: int = 4) -> list[dict]:
    """Search previously published encyclopedia articles for relevant content."""
    import json, os
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    articles_file = os.path.join(ROOT_DIR, "articles.json")
    try:
        with open(articles_file, "r", encoding="utf-8") as f:
            articles = json.load(f)
    except Exception:
        return []

    if not articles:
        return []

    # Build searchable text from each article and score by embedding similarity
    q_vec = _get_embedding(question)
    scored = []

    for art in articles:
        # Combine title + summary + all section content into one searchable block
        full_text = art.get("title", "") + " " + art.get("summary", "")
        for sec in art.get("sections", []):
            full_text += " " + sec.get("content", "")
        for q in art.get("rebbe_quotes", []):
            full_text += " " + q.get("quote", "")

        if q_vec:
            vec = _get_embedding(full_text[:2000])  # embed first 2000 chars
            if vec:
                scored.append((_cosine_similarity(q_vec, vec), art))
        else:
            # keyword fallback
            if question.lower() in full_text.lower():
                scored.append((1.0, art))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [a for _, a in scored[:top_k]]


def generate_article(question: str) -> dict | None:
    """Generate a full structured article, drawing from both source documents
    AND previously published encyclopedia articles."""

    # ── Load source document chunks ───────────────────────────────────────
    if "library_chunks" not in st.session_state or not st.session_state["library_chunks"]:
        try:
            with open(CHUNKS_FILE, "rb") as f:
                st.session_state["library_chunks"] = pickle.load(f)
        except FileNotFoundError:
            st.session_state["library_chunks"] = []

    if "embeddings" not in st.session_state:
        try:
            with open(EMBEDDINGS_FILE, "rb") as f:
                st.session_state["embeddings"] = pickle.load(f)
        except FileNotFoundError:
            st.session_state["embeddings"] = []

    # ── Search source documents ───────────────────────────────────────────
    doc_chunks = search_chunks(question, top_k=14)

    # ── Search published encyclopedia articles ────────────────────────────
    related_articles = _search_published_articles(question, top_k=3)

    if not doc_chunks and not related_articles:
        return None

    # ── Build context block from source documents ─────────────────────────
    context_parts = []

    if doc_chunks:
        doc_context = "\n\n".join(
            f"[Source document: {ch['source']}]\n{ch['text']}"
            for ch in doc_chunks
        )
        context_parts.append("=== SOURCE DOCUMENTS ===\n" + doc_context)

    # ── Build context block from published articles ───────────────────────
    if related_articles:
        art_context_parts = []
        for art in related_articles:
            art_text = f"[Published article: \"{art['title']}\"]\n"
            art_text += f"Summary: {art.get('summary','')}\n"
            for sec in art.get("sections", [])[:3]:  # first 3 sections only
                art_text += f"\n{sec.get('heading','')}:\n{sec.get('content','')[:600]}"
            art_context_parts.append(art_text)
        context_parts.append("=== RELATED ENCYCLOPEDIA ARTICLES (already published — you may reference and build on these) ===\n" + "\n\n".join(art_context_parts))

    full_context = "\n\n".join(context_parts)

    user_prompt = (
        f"Write a complete encyclopedia article answering this question: \"{question}\"\n\n"
        f"{full_context}\n\n"
        "Remember: Return ONLY valid JSON. No markdown fences."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": ARTICLE_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2,
            max_tokens=4000,
        )

        raw = response.choices[0].message.content.strip()

        # Strip accidental markdown fences
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        if raw.endswith("```"):
            raw = raw[:-3]
        raw = raw.strip()

        article = json.loads(raw)
        article["question"] = question
        article["source_docs"] = list(dict.fromkeys(ch["source"] for ch in doc_chunks))
        if related_articles:
            article["built_on"] = [a["title"] for a in related_articles]
        return article

    except json.JSONDecodeError as e:
        st.error(f"Could not parse AI response as JSON: {e}")
        return None
    except Exception as e:
        st.error(f"OpenAI API error: {e}")
        return None
