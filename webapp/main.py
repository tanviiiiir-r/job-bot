from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'jobs.db')

def get_jobs():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT title, score, url FROM jobs WHERE score IS NOT NULL ORDER BY score DESC LIMIT 10")
    rows = cur.fetchall()
    con.close()
    return rows

@app.route("/")
def index():
    jobs = get_jobs()
    return render_template("index.html", jobs=jobs)

if __name__ == "__main__":
    app.run(debug=True)
