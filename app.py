# ============================================================
# FUNCTIONING AI ENCYCLOPEDIA - REBBE SECURITY (STREAMLIT CLOUD)
# ============================================================
# FIXED (IMPORTANT):
# Streamlit Cloud now installs openai>=1.0.0 by default.
# This version correctly uses the NEW OpenAI Python SDK.
# ============================================================

import streamlit as st
from openai import OpenAI

# ------------------------------
# Page Setup
# ------------------------------
st.set_page_config(page_title="Rebbe Security Encyclopedia", layout="wide")
st.title("Rebbe Security Encyclopedia")
st.markdown(
    "Ask a question and receive an encyclopedia-style answer based on the teachings of the Lubavitcher Rebbe on security for the Land of Israel."
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

# Initialize OpenAI client (NEW SDK)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ------------------------------
# Question Input (MAIN PAGE)
# ------------------------------
question = st.text_area(
    "Your question",
    height=150,
    placeholder="e.g. What did the Rebbe say about preemptive defense?"
)

# ------------------------------
# Generate AI Answer
# ------------------------------
def generate_ai_answer(question: str) -> str:
    prompt = (
        "You are writing an encyclopedia entry.\n"
        "Answer ONLY based on the teachings of the Lubavitcher Rebbe regarding security and the Land of Israel.\n"
        "Write clearly, with structure, sources implied, and depth.\n\n"
        f"Question: {question}"
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
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Generating encyclopedia entry..."):
            try:
                answer = generate_ai_answer(question)
                st.subheader("Answer")
                st.write(answer)
            except Exception as e:
                st.error(f"Error generating answer: {e}")
