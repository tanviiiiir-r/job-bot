from connectors.te_palvelut import fetch_te
# from connectors.duunitori import fetch_duunitori
# from connectors.laura import fetch_laura

keywords = ["cybersecurity", "python"]

print("🚀 Starting job fetch (TE-palvelut only)...\n")

for kw in keywords:
    print(f"🔎 Searching for keyword: {kw}\n")
    
    # Future sources:
    # fetch_duunitori(kw)
    fetch_te(kw)
    # fetch_laura(kw)

    print("-" * 40 + "\n")

print("✅ Fetching complete! Check data/jobs.db for results.")
