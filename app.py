# ============================================================
# FUNCTIONING AI ENCYCLOPEDIA - REBBE SECURITY (STREAMLIT CLOUD)
# ============================================================
# NEXT DEVELOPMENT STEP: MULTI-TOPIC DYNAMIC AI ENCYCLOPEDIA
# Now capable of handling multiple topics while keeping structured encyclopedia style
# ============================================================

import streamlit as st
from openai import OpenAI

# ------------------------------
# Page Setup
# ------------------------------
st.set_page_config(page_title="Rebbe Security Encyclopedia", layout="wide")
st.title("Rebbe Security Encyclopedia")
st.markdown(
    "This AI generates full encyclopedia-style articles based on the teachings of the Lubavitcher Rebbe regarding security for the Land of Israel."
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
# Select Topic
# ------------------------------
topics = [
    "Preemptive Defense",
    "Ownership of Israel",
    "The 329 Paradigm"
]

selected_topic = st.selectbox("Select the topic you want an encyclopedia article on:", topics)

# ------------------------------
# Optional Context Input
# ------------------------------
context = st.text_area(
    "Additional context or notes (optional)",
    height=100,
    placeholder="You can type extra details or leave blank."
)

# ------------------------------
# Generate AI Encyclopedia Article
# ------------------------------
def generate_article(topic: str, context: str) -> str:
    prompt = (
        f"You are writing an encyclopedia entry on the topic **{topic}**.\n"
        "Answer ONLY based on the teachings of the Lubavitcher Rebbe regarding security and the Land of Israel.\n"
        "Write in a descriptive + explanatory style.\n"
        "Use formal, structured language with sections: Overview, Core Principles, Halachic Foundation, Security Implications, Conclusion.\n"
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
    with st.spinner(f"Generating encyclopedia article for {selected_topic}..."):
        try:
            answer = generate_article(selected_topic, context.strip())
            st.subheader(selected_topic)
            st.write(answer)
        except Exception as e:
            st.error(f"Error generating article: {e}")
