import os
import json
from datetime import datetime
from utils.db import get_db

def fetch_duunitori(keyword: str):
    print(f"🔍 Searching Duunitori for: {keyword}")
    # Normally this would fetch real data. Here's mock-safe version.
    jobs = []
    for i in range(1, 6):
        job = {
            "id": f"duuni-{keyword[:3]}-{i}",
            "title": f"[Duunitori] Mock Job {i} – {keyword.title()}",
            "company": f"Duunitori Oy",
            "description": f"Mock description for {keyword} job number {i}",
            "url": f"https://duunitori.fi/mock/{keyword}/{i}"
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
            "duunitori",
            fetched_at,
            json.dumps(job)
        ))

    con.commit()
    print(f"✅ Saved {len(jobs)} Duunitori jobs for '{keyword}' into database.\n")
