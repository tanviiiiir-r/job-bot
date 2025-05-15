import json
from datetime import datetime
from utils.db import get_db

def fetch_laura(keyword: str):
    print(f"🔍 Searching Laura.fi for: {keyword}")

    jobs = []
    for i in range(1, 6):
        job = {
            "id": f"laura-{keyword[:3]}-{i}",
            "title": f"[Laura.fi] Mock Job {i} – {keyword.title()}",
            "company": f"LauraTestCompany{i}",
            "description": f"This is a mock job for {keyword}",
            "url": f"https://laura.fi/mock/{keyword}/{i}"
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
            "laura",
            fetched_at,
            json.dumps(job)
        ))

    con.commit()
    print(f"✅ Saved {len(jobs)} Laura.fi jobs for '{keyword}' into database.\n")
