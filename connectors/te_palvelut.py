import os
import json
from datetime import datetime
from utils.db import get_db

def fetch_te(keyword: str):
    print(f"🔍 Searching TE-palvelut for: {keyword}")
    # Mock-safe example
    jobs = []
    for i in range(1, 6):
        job = {
            "id": f"te-{keyword[:3]}-{i}",
            "title": f"[TE] Mock Job {i} – {keyword.title()}",
            "company": f"TE Services Finland",
            "description": f"Sample description for TE job about {keyword}",
            "url": f"https://te-palvelut.fi/mock/{keyword}/{i}"
        }
        print(f"📄 {job['title']} ({job['url']})")
        jobs.append(job)

    con = get_db()
    cur = con.cursor()
    fetched_at = datetime.utcnow().isoformat()

    for job in jobs:
        cur.execute("""
            INSERT OR REPLACE INTO jobs (id, title, url, source, fetched, raw)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            job["id"],
            job["title"],
            job["url"],
            "te-palvelut",
            fetched_at,
            json.dumps(job)
        ))

    con.commit()
    print(f"✅ Saved {len(jobs)} TE-palvelut jobs for '{keyword}' into database.\n")
