import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def summarize_transcript(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        transcript = f.read()

    prompt = f"""
    Here is a meeting transcript:
    {transcript}

    Please summarize the meeting into:
    1. Key decisions
    2. Action items with owners
    3. Deadlines if mentioned
    """

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a professional meeting assistant."},
            {"role": "user", "content": prompt}
        ],
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    result = summarize_transcript("sample_transcript.txt")
    print("\n--- Meeting Summary ---\n")
    print(result)

