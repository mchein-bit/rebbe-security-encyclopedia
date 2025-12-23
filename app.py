# ============================================================
# GROKPEDIA-STYLE AI ENCYCLOPEDIA - REBBE SECURITY (STREAMLIT CLOUD)
# ============================================================
# We are now following the 5-step roadmap to create a Grokpedia-like encyclopedia.
# Steps being implemented:
# 1. Lock AI to your sources (JEM texts & website material)
# 2. Generate real, structured articles for each topic
# 3. Add citations and source references
# 4. Internal linking between topics
# 5. Search/index functionality for navigation
# ============================================================

import streamlit as st
from openai import OpenAI

# ------------------------------
# Page Setup
# ------------------------------
st.set_page_config(page_title="Rebbe Security Encyclopedia", layout="wide")
st.title("Rebbe Security Encyclopedia")
st.markdown(
    "This AI generates encyclopedia-style articles based strictly on the teachings of the Lubavitcher Rebbe regarding security for the Land of Israel, with structured content and cross-topic links like Grokpedia."
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
# Multi-Topic Setup for Grokpedia
# ------------------------------
topics = [
    "Preemptive Defense",
    "Ownership of Israel",
    "The 329 Paradigm"
]

# Store generated articles and references
if 'articles' not in st.session_state:
    st.session_state['articles'] = {}

if 'references' not in st.session_state:
    st.session_state['references'] = {}

# ------------------------------
# Topic Selection
# ------------------------------
selected_topic = st.selectbox("Select a topic to generate/view:", topics)

# ------------------------------
# Optional Context Input
# ------------------------------
context = st.text_area(
    "Additional context or notes (optional)",
    height=100,
    placeholder="Add context to guide the AI (optional)"
)

# ------------------------------
# Generate AI Encyclopedia Article with citations
# ------------------------------
def generate_grokpedia_article(topic: str, context: str) -> str:
    prompt = (
        f"You are writing a Grokpedia-style encyclopedia entry on **{topic}**.\n"
        "Answer ONLY using the teachings of the Lubavitcher Rebbe on security for the Land of Israel.\n"
        "Provide a structured article in descriptive + explanatory style with these sections: Overview, Core Principles, Halachic Foundation, Security Implications, Conclusion.\n"
        "Include citations or references whenever a specific letter, sicha, or source applies.\n"
        "Highlight internal links to related topics (Preemptive Defense, Ownership of Israel, The 329 Paradigm).\n"
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
    with st.spinner(f"Generating Grokpedia-style article for {selected_topic}..."):
        try:
            article = generate_grokpedia_article(selected_topic, context.strip())
            st.session_state['articles'][selected_topic] = article
            st.subheader(selected_topic)
            st.write(article)
        except Exception as e:
            st.error(f"Error generating article: {e}")

# ------------------------------
# Display previously generated articles
# ------------------------------
if selected_topic in st.session_state['articles']:
    st.markdown("---")
    st.subheader(f"Previously generated article for {selected_topic}")
    st.write(st.session_state['articles'][selected_topic])
