# ------------------------------
# AI FUNCTION (USES SEARCHED CONTEXT ONLY)
# ------------------------------

def answer_question_or_generate_article(question: str) -> str:
    '''Answer questions using searched context + prior articles.'''

    try:
        # Merge previously generated content safely
        article_context = "\n\n".join([str(a) for a in st.session_state.get('articles', {}).values()])

        # Pull ONLY the relevant passages from uploaded docs
        results = search_library(question)
        library_context = "\n\n".join([f"[From {r['source']}]\n{r['text']}" for r in results])

        # Multiline prompt using triple quotes
        prompt = f'''
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
'''

        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.15,
        )

        return response.choices[0].message.content

    except Exception as e:
        st.error(f"Error in generating answer: {e}")
        return ""
