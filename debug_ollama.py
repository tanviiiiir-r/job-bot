from ollama import Client
import re

client = Client(host='http://localhost:11434')

prompt = """
You are a helpful assistant. Rate how well this job matches the user's skills on a scale from 0 to 10.

Rules:
- 0 = totally unrelated
- 10 = perfect match
- Return ONLY a single number. No explanation.

##
MY SKILLS:
Python, Cybersecurity, Helpdesk, GPT, FastAPI, API Automation, AI tools

##
JOB DESCRIPTION:
We are looking for a cybersecurity engineer with knowledge of Python and cloud automation.

"""

try:
    response = client.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )
    content = response['message']['content'].strip()
    print("📨 Ollama raw reply:", repr(content))

    match = re.search(r"\b(10|[0-9])\b", content)
    if match:
        score = int(match.group(0))
        print(f"🎯 Extracted score:", score)
    else:
        print("⚠️ No valid number found in response.")

except Exception as e:
    print("❌ Ollama call failed:", e)
