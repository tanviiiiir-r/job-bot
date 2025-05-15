import os
import sqlite3
import json
import re
from dotenv import load_dotenv
from ollama import Client

# 🧠 Load environment variables
load_dotenv()
client = Client(host='http://localhost:11434')

# 🧠 Your skillset (customize this as needed)
YOUR_SKILLS = """
Python, Cybersecurity, Helpdesk, GPT, FastAPI, API Automation, AI tools
"""

# 🧠 Ollama-based job scoring
def score_job_text(description):
    prompt = f"""
You are a helpful assistant. Rate how well this job matches the user's skills on a scale from 0 to 10.

Rules:
- 0 = totally unrelated
- 10 = perfect match
- Return ONLY a single number. No explanation.

##
MY SKILLS:
{YOUR_SKILLS}

##
JOB DESCRIPTION:
{description}
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
            print(f"🎯 Extracted score: {score}")
            return score
        else:
            print("⚠️ No valid number found in response.")
            return None

    except Exception as e:
        print("❌ Ollama scoring error:", e)
        return None

# 🧠 Score only TE-palvelut jobs that are unscored
def score_te_only():
    con = sqlite3.connect("data/jobs.db")
    cur = con.cursor()
    cur.execute("SELECT id, raw FROM jobs WHERE score IS NULL AND source = 'te'")
    rows = cur.fetchall()

    print(f"\n🔍 Found {len(rows)} unscored TE-palvelut jobs.\n")

    for job_id, raw_json in rows:
        try:
            print(f"🔄 Scoring job ID {job_id}")
            job = json.loads(raw_json)
            desc = job.get("description", "")
            score = score_job_text(desc)
            if score is not None:
                cur.execute("UPDATE jobs SET score = ? WHERE id = ?", (score, job_id))
                print(f"💾 Saved score {score} for job ID {job_id} ({job.get('title')[:50]})")
            else:
                print(f"⚠️ Skipped job {job_id} due to invalid score.")
        except Exception as e:
            print(f"❌ Error scoring job {job_id}:", e)

    con.commit()
    con.close()
    print("\n✅ Done scoring TE-palvelut jobs.\n")

# ✅ Trigger scoring when script is run
if __name__ == "__main__":
    score_te_only()
