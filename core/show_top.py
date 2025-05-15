import sqlite3
from rich.console import Console
from rich.table import Table

console = Console()

con = sqlite3.connect("data/jobs.db")
cur = con.cursor()

rows = cur.execute("""
    SELECT title, score 
    FROM jobs 
    WHERE score IS NOT NULL AND source = 'te' 
    ORDER BY score DESC 
    LIMIT 10
""").fetchall()
con.close()

if not rows:
    console.print("[yellow]⚠️ No scored jobs found.[/yellow]")
else:
    table = Table(title="⭐ Top 10 Job Matches (TE-palvelut Only)", show_lines=True)
    table.add_column("Rank", justify="center", style="cyan")
    table.add_column("Job Title", style="green")
    table.add_column("Score", justify="center", style="bold yellow")

    for i, (title, score) in enumerate(rows, 1):
        table.add_row(str(i), title, f"{score}/10")

    console.print(table)
