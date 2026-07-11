import json
from pathlib import Path

DATA = Path("data")
REPORTS = Path("reports")

REPORTS.mkdir(exist_ok=True)


def load_json(filename):
    with open(DATA / filename, "r") as f:
        return json.load(f)


league = load_json("league.json")
transactions = load_json("transactions.json")
waiver_board = load_json("waiver_board.json")
rosters = load_json("rosters.json")
users = load_json("users.json")

report = []

report.append("# Tyler Dynasty GM Report")
report.append("")
report.append(f"League: {league['name']}")
report.append("")
report.append(f"Season: {league['season']}")
report.append("")
report.append(f"Teams: {league['total_rosters']}")
report.append("")
report.append("---")
report.append("")
report.append("## League Summary")
report.append("")
report.append(f"- Managers: {len(users)}")
report.append(f"- Rosters: {len(rosters)}")
report.append(f"- Transaction Weeks: {len(transactions)}")
report.append(f"- Available Players: {len(waiver_board)}")
report.append("")
report.append("---")
report.append("")
report.append("## Recent Activity")
report.append("")

latest_week = max(transactions.keys(), key=int)

for t in transactions[latest_week][:10]:
    report.append(f"- {t['type'].title()} ({t['status']})")

report.append("")
report.append("---")
report.append("")
report.append("GM Report generated successfully.")

with open(REPORTS / "daily_gm_report.md", "w") as f:
    f.write("\n".join(report))

print("Created reports/daily_gm_report.md")
