import os
import sqlite3
import json
import re
from dotenv import load_dotenv
from ollama import Client
from rich.console import Console
from rich.table import Table
from rich.progress import track

# 🧠 Load environment variables
load_dotenv()
client = Client(host='http://localhost:11434')

console = Console()

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
        console.log(f"[bold blue]📨 Ollama raw reply:[/bold blue] {repr(content)}")

        match = re.search(r"\b(10|[0-9])\b", content)
        if match:
            score = int(match.group(0))
            console.log(f"[green]🎯 Extracted score: {score}[/green]")
            return score
        else:
            console.log("[yellow]⚠️ No valid number found in response.[/yellow]")
            return None

    except Exception as e:
        console.log(f"[red]❌ Ollama scoring error:[/red] {e}")
        return None

# 🧠 Score only TE-palvelut jobs that are unscored
def score_te_only():
    con = sqlite3.connect("data/jobs.db")
    cur = con.cursor()
    cur.execute("SELECT id, raw FROM jobs WHERE score IS NULL AND source = 'te'")
    rows = cur.fetchall()

    if not rows:
        console.print("[green]✅ All TE jobs are already scored.[/green]")
        return

    console.print(f"\n[bold cyan]🔍 Found {len(rows)} unscored TE-palvelut jobs[/bold cyan]\n")

    for job_id, raw_json in track(rows, description="🧠 Scoring jobs..."):
        try:
            job = json.loads(raw_json)
            desc = job.get("description", "")
            score = score_job_text(desc)
            if score is not None:
                cur.execute("UPDATE jobs SET score = ? WHERE id = ?", (score, job_id))
                console.print(f"[green]💾 Saved score {score} for job:[/green] {job.get('title', 'N/A')[:60]}")
            else:
                console.print(f"[yellow]⚠️ Skipped job {job_id} due to invalid score[/yellow]")
        except Exception as e:
            console.print(f"[red]❌ Error scoring job {job_id}:[/red] {e}")

    con.commit()
    con.close()
    console.print("\n[bold green]✅ Done scoring TE-palvelut jobs.[/bold green]")

# ✅ Trigger scoring when script is run
if __name__ == "__main__":
    score_te_only()
