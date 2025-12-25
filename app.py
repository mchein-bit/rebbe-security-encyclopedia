import streamlit as st
import docx
from openai import OpenAI
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
import io

# ------------------------------
# OPENAI CLIENT SETUP
# ------------------------------
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

st.title("Rebbe Security Encyclopedia")
st.write("Ask any question about the Rebbe's teachings on security for Israel.")

# ------------------------------
# GOOGLE DRIVE INTEGRATION
# ------------------------------
st.subheader("Load documents from Google Drive")

# Set path to your service account credentials JSON (add to Streamlit secrets or upload)
SERVICE_ACCOUNT_FILE = 'service_account.json'
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)

# Specify your folder ID
FOLDER_ID = st.text_input("Enter Google Drive Folder ID:")

if FOLDER_ID:
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

            # Break text into chunks
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

# ------------------------------
# AI FUNCTION AND USER UI (unchanged from previous version)
# ------------------------------

def answer_question_or_generate_article(question: str) -> str:
    '''Answer questions using uploaded documents and prior articles, with debug messages.''' 
    try:
        st.write("Debug: AI function called")
        article_context = "\n\n".join([str(a) for a in st.session_state.get('articles', {}).values()])
        results = st.session_state.get('library_chunks', [])
        if len(results) == 0:
            st.warning("No documents uploaded. Please upload files to generate answers.")
            return ""
        library_context = "\n\n".join(["[From {}]\n{}".format(r['source'], r['text']) for r in results])
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
    except Exception as e:
        st.error(f"Error in generating answer: {e}")
        return ""

question = st.text_input("Type your question here:")
if question:
    answer = answer_question_or_generate_article(question)
    st.subheader("Answer")
    st.write(answer)
