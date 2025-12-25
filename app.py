import streamlit as st
import docx
from openai import OpenAI
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
import io
import json

# ------------------------------
# OPENAI CLIENT SETUP
# ------------------------------
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

st.title("Rebbe Security Encyclopedia")
st.write("Ask any question about the Rebbe's teachings on security for Israel.")

# ------------------------------
# GOOGLE DRIVE INTEGRATION USING STREAMLIT SECRETS
# ------------------------------
st.subheader("Load documents from Google Drive")

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# Read the service account JSON from Streamlit secrets safely
try:
    service_account_json_str = st.secrets["google"]["service_account_json"]
    # Replace literal newlines with escaped newlines
    service_account_json_str = service_account_json_str.replace('\\n', '\\n')
    service_account_info = json.loads(service_account_json_str)
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=SCOPES
    )
    service = build('drive', 'v3', credentials=credentials)
except Exception as e:
    st.error(f"Google Drive authentication failed. Check that your JSON in secrets is valid: {e}")
    st.stop()

# Input folder ID
FOLDER_ID = st.text_input("Enter Google Drive Folder ID:")

if FOLDER_ID:
    try:
        query = f"'{FOLDER_ID}' in parents and (mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document' or mimeType='text/plain')"
        results = service.files().list(q=query, pageSize=100, fields="files(id, name, mimeType)").execute()
        files = results.get('files', [])

        if files:
            if 'library_chunks' not in st.session_state:
                st.session_state['library_chunks'] = []

            for file in files:
                request = service.files().get_media(fileId=file['id'])
                fh = io.BytesIO()
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                fh.seek(0)

                if file['mimeType'] == 'text/plain':
                    text = fh.read().decode('utf-8')
                elif file['mimeType'] == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                    doc = docx.Document(fh)
                    text = "\n".join([p.text for p in doc.paragraphs])
                else:
                    text = ""

                # Break text into chunks for AI
                chunk_size = 150
                overlap = 50
                words = text.split()
                i = 0
                while i < len(words):
                    chunk = " ".join(words[i:i+chunk_size])
                    st.session_state['library_chunks'].append({"source": file['name'], "text": chunk})
                    i += chunk_size - overlap

            st.success(f"Added {len(files)} file(s) from Google Drive to the knowledge library.")
        else:
            st.warning("No documents found in this folder.")
    except Exception as e:
        st.error(f"Error loading files from Google Drive: {e}")

# ------------------------------
# AI FUNCTION AND USER UI
# ------------------------------

def answer_question_or_generate_article(question: str) -> str:
    '''Answer questions using uploaded documents and prior articles.''' 
    st.write("Debug: AI function called")
    article_context = "\n\n".join([str(a) for a in st.session_state.get('articles', {}).values()])
    results = st.session_state.get('library_chunks', [])
    if len(results) == 0:
        st.warning("No documents uploaded. Please upload files to generate answers.")
        return ""
    # Corrected f-string with proper quotes and bracket
    library_context = "\n\n".join([f"[From {r['source']}]\n{r['text']}" for r in results])

    prompt = f'''
You are an AI Grokpedia assistant.
Answer ONLY using the material provided below.
If a clear source is not present in the context, say that you don't have enough information.
Prefer accuracy over speculation.

Always search for both English and Yiddish content and use translations where needed.

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
    try:
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.15,
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"OpenAI API error: {e}")
        return ""

question = st.text_input("Type your question here:")
if question:
    answer = answer_question_or_generate_article(question)
    st.subheader("Answer")
    st.write(answer)
