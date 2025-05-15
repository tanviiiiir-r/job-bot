import sqlite3
import os
import json
from dotenv import load_dotenv

load_dotenv()
cv_path = os.getenv("CV_FILE", "docs/my_cv.pdf")

def apply_to_job(job_id):
    con = sqlite3.connect("data/jobs.db")
    cur = con.cursor()
    cur.execute("SELECT title, url, raw FROM jobs WHERE id = ?", (job_id,))
    row = cur.fetchone()

    if not row:
        print(f"❌ Job ID {job_id} not found.")
        return

    title, url, raw_json = row
    print(f"\n📩 Applying to job: {title}\n🔗 URL: {url}\n📎 Attaching CV: {cv_path}")

    with open("logs/applications_sent.log", "a") as log:
        log.write(f"✅ Applied to '{title}' ({url}) with CV: {cv_path}\n")

    print("✅ Application simulated and logged.\n")
    con.close()

if __name__ == "__main__":
    job_id = input("Enter Job ID to apply: ").strip()
    apply_to_job(job_id)
