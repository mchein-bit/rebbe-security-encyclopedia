import os
import json
import pickle
import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

ARTICLE_SYSTEM_PROMPT = """You are a senior scholar writing for the Rebbe's Encyclopedia — a Grokipedia-style knowledge base of the Lubavitcher Rebbe's teachings on Israel, security, and the Middle East as grounded in Torah.

Your articles must:
- Be encyclopedic, dignified, and scholarly in tone — like a well-sourced Wikipedia article meets a Torah journal
- Draw ONLY from the provided source passages. Never invent quotes or facts.
- Structure every article with these exact JSON fields (described below)
- When quoting the Rebbe, preserve his exact words and cite the source (date/occasion)
- Be factually precise — if sources don't cover something, say so honestly in that section

Return ONLY valid JSON. No markdown fences, no preamble, no explanation. Just the raw JSON object.

JSON structure to return:
{
  "title": "Clear encyclopedic title for this article",
  "category": "One of: Principles & Halacha | Wars & Military Operations | People | Diplomacy & Peace Negotiations | Territories & Geography | Prophecy & Spiritual Dimensions | Other",
  "summary": "2-3 sentence summary of the article — appears as the lead paragraph",
  "sections": [
    {
      "heading": "Overview",
      "content": "Full prose content for this section..."
    },
    {
      "heading": "Background",
      "content": "..."
    },
    {
      "heading": "The Rebbe's Teaching",
      "content": "..."
    },
    {
      "heading": "Application & Significance",
      "content": "..."
    }
  ],
  "rebbe_quotes": [
    {
      "quote": "Exact quote from the Rebbe",
      "source": "Occasion/date/letter if available"
    }
  ],
  "footnotes": [
    "Citation or source note 1",
    "Citation or source note 2"
  ],
  "further_reading": [
    {
      "title": "Title of resource",
      "url": ""
    }
  ],
  "keywords": ["keyword1", "keyword2"]
}

The sections array must always include at minimum: Overview, The Rebbe's Teaching. Add additional sections as appropriate based on the content.
Each section's content should be 2-5 substantial paragraphs of encyclopedic prose.
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

def generate_article(question: str) -> dict | None:
    """Generate a full structured article from the question using source documents."""
    
    # Load library from disk if not in session
    if "library_chunks" not in st.session_state or not st.session_state["library_chunks"]:
        try:
            with open("library_chunks.pkl", "rb") as f:
                st.session_state["library_chunks"] = pickle.load(f)
        except FileNotFoundError:
            st.session_state["library_chunks"] = []
    
    if "embeddings" not in st.session_state:
        try:
            with open("embeddings.pkl", "rb") as f:
                st.session_state["embeddings"] = pickle.load(f)
        except FileNotFoundError:
            st.session_state["embeddings"] = []

    chunks = search_chunks(question, top_k=16)
    
    if not chunks:
        return None
    
    context = "\n\n".join(
        f"[Source: {ch['source']}]\n{ch['text']}"
        for ch in chunks
    )
    
    user_prompt = (
        f"Write a complete encyclopedia article answering this question: \"{question}\"\n\n"
        f"=== SOURCE PASSAGES ===\n{context}\n\n"
        "Remember: Return ONLY valid JSON matching the specified structure. No markdown fences."
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": ARTICLE_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.15,
            max_tokens=3000,
        )
        
        raw = response.choices[0].message.content.strip()
        
        # Strip any accidental markdown fences
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        if raw.endswith("```"):
            raw = raw[:-3]
        raw = raw.strip()
        
        article = json.loads(raw)
        article["question"] = question
        article["source_docs"] = list(dict.fromkeys(ch["source"] for ch in chunks))
        return article
    
    except json.JSONDecodeError as e:
        st.error(f"Could not parse AI response as JSON: {e}")
        return None
    except Exception as e:
        st.error(f"OpenAI API error: {e}")
        return None
