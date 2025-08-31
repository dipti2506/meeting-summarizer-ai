import streamlit as st
from groq import Groq
import os

# ---- Load API Key ----
try:
    api_key = os.getenv("GROQ_API_KEY") or st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("GROQ_API_KEY not found! Add it to your environment or Streamlit secrets.")
    st.stop()

# ---- Initialize Groq Client ----
client = Groq(api_key=api_key)
MODEL_NAME = "llama3-8b-8192"
MAX_TOKENS = 300
CHUNK_SIZE = 3000  # characters per chunk, adjust if needed

# ---- Summarization Function ----
def summarize_transcript(transcript_text):
    if not transcript_text.strip():
        return "Transcript is empty."

    # Split transcript into chunks
    chunks = [transcript_text[i:i+CHUNK_SIZE] for i in range(0, len(transcript_text), CHUNK_SIZE)]
    summaries = []

    for idx, chunk in enumerate(chunks):
        prompt = f"""
        Here is a meeting transcript:
        {chunk}

        Summarize key decisions and action items with owners.
        """
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=MAX_TOKENS,
            )
            summaries.append(response.choices[0].message.content.strip())
        except Exception as e:
            st.warning(f"Chunk {idx+1} could not be summarized: {e}")
            summaries.append("[Error summarizing this part]")

    # Combine summaries
    final_summary = " ".join(summaries)
    return final_summary

# ---- Streamlit UI ----
st.title("📋 Meeting Summarizer AI")
st.write("Upload a meeting transcript and get instant summary + action items.")

uploaded_file = st.file_uploader("Upload transcript (.txt)", type="txt")

if uploaded_file is not None:
    transcript = uploaded_file.read().decode("utf-8")
    st.subheader("Transcript Preview")
    st.text(transcript[:500] + "..." if len(transcript) > 500 else transcript)

    if st.button("Summarize"):
        with st.spinner("Summarizing..."):
            summary = summarize_transcript(transcript)
            st.subheader("✅ Summary & Action Items")
            st.write(summary)
