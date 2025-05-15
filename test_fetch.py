from connectors.te_palvelut import fetch_te
# from connectors.duunitori import fetch_duunitori
# from connectors.laura import fetch_laura

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()

keywords = ["cybersecurity", "python"]

console.print(Panel("🚀 [bold green]Starting job fetch (TE-palvelut only)...[/bold green]", expand=False))

for kw in keywords:
    console.print(f"\n🔎 [cyan]Fetching jobs for keyword:[/cyan] [bold]{kw}[/bold]")
    
    # Future sources:
    # fetch_duunitori(kw)
    fetch_te(kw)
    # fetch_laura(kw)

    console.rule(f"[green]✔ Done fetching for: {kw}")

console.print("\n✅ [bold green]Fetching complete![/bold green] Check [italic]data/jobs.db[/italic] for results.")
