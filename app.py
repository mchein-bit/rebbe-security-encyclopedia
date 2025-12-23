# ============================================================
# AI-POWERED GROKPEDIA-STYLE ENCYCLOPEDIA WITH QUESTION ANSWERING
# REBBE SECURITY (STREAMLIT CLOUD)
# ============================================================
# Now the AI serves dual purpose: answers user questions based on the knowledge base and existing articles,
# and generates structured encyclopedia-style entries.
# ============================================================

import streamlit as st
from openai import OpenAI

# ------------------------------
# Page Setup
# ------------------------------
st.set_page_config(page_title="Rebbe Security Encyclopedia", layout="wide")
st.title("Rebbe Security Encyclopedia")
st.markdown(
    "This AI answers user questions and generates encyclopedia-style articles strictly based on the teachings of the Lubavitcher Rebbe regarding security for the Land of Israel."
)

# ------------------------------
# READ API KEY FROM STREAMLIT SECRETS
# ------------------------------
if "OPENAI_API_KEY" not in st.secrets:
    st.error(
        "OpenAI API key not found.\n\n"
        "You are using Streamlit Cloud. You must add your API key in **Secrets**.\n\n"
        "Steps:\n"
        "1. Click ⚙️ Settings\n"
        "2. Click Secrets\n"
        "3. Add:\n"
        "OPENAI_API_KEY = sk-..."
    )
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ------------------------------
# Multi-Topic Knowledge Base
# ------------------------------
topics = [
    "Preemptive Defense",
    "Ownership of Israel",
    "The 329 Paradigm"
]

# Store generated articles
if 'articles' not in st.session_state:
    st.session_state['articles'] = {}

# ------------------------------
# User Question Input
# ------------------------------
user_question = st.text_area(
    "Ask a question or request an article:",
    height=150,
    placeholder="e.g., What did the Rebbe say about preemptive defense?"
)

# ------------------------------
# AI Function: Answer Questions or Generate Articles
# ------------------------------
def answer_question_or_generate_article(question: str) -> str:
    # Collect context from previously generated articles
    knowledge_context = "\n\n".join(st.session_state['articles'].values())

    prompt = (
        f"You are an AI Grokpedia assistant. Answer the user's question or generate an encyclopedia-style article.\n"
        f"Use ONLY the knowledge from the Lubavitcher Rebbe's teachings and any previously generated articles provided.\n"
        f"Structure the answer clearly and include sections if appropriate (Overview, Core Principles, Halachic Foundation, Security Implications, Conclusion).\n"
        f"Cite sources or previously generated material when relevant.\n\n"
        f"Knowledge context: {knowledge_context}\n"
        f"User question: {question}"
    )

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    return response.choices[0].message.content

# ------------------------------
# Submit Button
# ------------------------------
if st.button("Ask"):
    if not user_question.strip():
        st.warning("Please enter a question or request.")
    else:
        with st.spinner("Generating answer/article..."):
            try:
                answer = answer_question_or_generate_article(user_question.strip())
                st.subheader("Answer / Article")
                st.write(answer)

                # Optionally store article if it appears encyclopedic
                st.session_state['articles'][user_question] = answer

            except Exception as e:
                st.error(f"Error generating answer/article: {e}")

# ------------------------------
# Display Previously Generated Articles
# ------------------------------
if st.session_state['articles']:
    st.markdown("---")
    st.subheader("Previously generated articles / answers")
    for q, a in st.session_state['articles'].items():
        st.markdown(f"**Request / Question:** {q}")
        st.write(a)
        st.markdown("---")
