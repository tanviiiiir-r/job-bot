import sqlite3

print("⭐ Top 10 Job Matches (TE-palvelut only):\n")

con = sqlite3.connect("data/jobs.db")
cur = con.cursor()

rows = cur.execute("""
    SELECT title, score 
    FROM jobs 
    WHERE score IS NOT NULL AND source = 'te' 
    ORDER BY score DESC 
    LIMIT 10
""").fetchall()

for title, score in rows:
    print(f"⭐ {score}/10 — {title}")

con.close()
