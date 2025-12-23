# ============================================================
# FUNCTIONING AI ENCYCLOPEDIA - REBBE SECURITY (STREAMLIT CLOUD)
# ============================================================
# LOCKED TO ONE TOPIC: PREEMPTIVE DEFENSE
# STEP: Descriptive + Explanatory (B)
# ============================================================

import streamlit as st
from openai import OpenAI

# ------------------------------
# Page Setup
# ------------------------------
st.set_page_config(page_title="Rebbe Security Encyclopedia", layout="wide")
st.title("Rebbe Security Encyclopedia")
st.markdown(
    "This AI generates a full encyclopedia-style article on the topic **Preemptive Defense** according to the teachings of the Lubavitcher Rebbe."
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
    "Your prompt (optional, the AI will focus on Preemptive Defense)",
    height=150,
    placeholder="You can type additional context or leave blank."
)

# ------------------------------
# Generate Encyclopedia Article
# ------------------------------
def generate_preemptive_defense_article(context: str) -> str:
    prompt = (
        "You are writing an encyclopedia entry on the topic **Preemptive Defense**.\n"
        "Answer ONLY based on the teachings of the Lubavitcher Rebbe regarding security and the Land of Israel.\n"
        "Write in a descriptive + explanatory style.\n"
        "Use formal, structured language, with sections: Overview, Core Principles, Halachic Foundation, Security Implications, Conclusion.\n"
        "Do NOT provide opinion or unrelated information.\n\n"
        f"Additional context from the user: {context}"
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
if st.button("Generate Article"):
    with st.spinner("Generating Preemptive Defense encyclopedia article..."):
        try:
            answer = generate_preemptive_defense_article(question.strip())
            st.subheader("Preemptive Defense")
            st.write(answer)
        except Exception as e:
            st.error(f"Error generating article: {e}")
