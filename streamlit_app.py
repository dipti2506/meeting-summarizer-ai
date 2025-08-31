import streamlit as st

st.title("🚀 Meeting Summarizer AI")
st.write("If you see this, Streamlit is working fine!")



import os
from groq import Groq
from dotenv import load_dotenv

# Load API key
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def summarize_transcript(transcript_text):
    prompt = f"""
    Here is a meeting transcript:
    {transcript_text}

    Summarize key decisions and action items with owners.
    """
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=300,
    )
    return response.choices[0].message["content"]

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

st.write("✅ Git change test")
print("Debug: change detected")
