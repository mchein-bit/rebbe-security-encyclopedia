# ------------------------------
# AI FUNCTION (USES SEARCHED CONTEXT ONLY)
# ------------------------------

def answer_question_or_generate_article(question: str) -> str:
    """Answer questions using searched context + prior articles."""

    # Merge previously generated content (safe newline string)
    article_context = "\n\n".join(st.session_state['articles'].values())

    # Pull ONLY the relevant passages from uploaded docs
    results = search_library(question)
    library_context = "\n\n".join([
        f"[From {r['source']}]\n{r['text']}" for r in results
    ])

    # Safer, cleaner multiline prompt
    prompt = f"""
You are an AI Grokpedia assistant.
Answer ONLY using the material provided below.
If a clear source is not present in the context, say that you don't have enough information.
Prefer accuracy over speculation.

When helpful, organize answers with sections like:
- Overview
- Principles
- Halachic Basis
- Implications
- Conclusion

Quote or summarize specific passages and name the document when possible.

=== CONTEXT: PREVIOUS ARTICLES ===
{article_context}

=== CONTEXT: RELEVANT SOURCES (SEARCHED) ===
{library_context}

=== USER QUESTION ===
{question}
"""

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.15,
    )

    return response.choices[0].message.content
