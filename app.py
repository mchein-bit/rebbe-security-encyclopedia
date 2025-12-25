import streamlit as st

st.title("Rebbe Security Encyclopedia")
st.write("Ask any question about the Rebbe's teachings on security for Israel.")

# ------------------------------
# AI FUNCTION WITH DEBUGGING AND STABILITY
# ------------------------------

def answer_question_or_generate_article(question: str) -> str:
    '''Answer questions using uploaded documents and prior articles, with debug messages.'''
    try:
        st.write("Debug: AI function called")

        # Merge previously generated articles safely
        article_context = "\n\n".join([str(a) for a in st.session_state.get('articles', {}).values()])
        st.write(f"Debug: article_context length = {len(article_context)}")

        # Pull ONLY relevant passages from uploaded documents
        results = st.session_state.get('library_chunks', [])
        library_context = "\n\n".join([f"[From {r['source']}]\n{r['text']}" for r in results])
        st.write(f"Debug: library_context length = {len(library_context)}")

        # Prepare the prompt for the AI
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

        st.write("Debug: Prompt created")

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.15,
        )

        st.write("Debug: Response received")
        return response.choices[0].message.content

    except Exception as e:
        st.error(f"Error in generating answer: {e}")
        return ""

# ------------------------------
# USER QUESTION UI
# ------------------------------

question = st.text_input("Type your question here:")

if question:
    answer = answer_question_or_generate_article(question)
    st.subheader("Answer")
    st.write(answer)
