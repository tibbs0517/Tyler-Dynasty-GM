import json
from pathlib import Path
from collections import Counter
from datetime import datetime

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
players = load_json("players.json")


# ------------------------------------------
# Build lookup dictionaries
# ------------------------------------------

player_lookup = {}

for pid, player in players.items():
    name = player.get("full_name")

    if not name:
        first = player.get("first_name", "")
        last = player.get("last_name", "")
        name = (first + " " + last).strip()

    if not name:
        name = pid

    player_lookup[pid] = name


owner_lookup = {}

for roster in rosters:

    owner_id = roster["owner_id"]
    roster_id = roster["roster_id"]

    display_name = str(roster_id)

    for user in users:
        if user["user_id"] == owner_id:
            display_name = user["display_name"]
            break

    owner_lookup[roster_id] = display_name


# ------------------------------------------
# Collect statistics
# ------------------------------------------

activity = Counter()

trade_count = 0
waiver_count = 0
free_agent_count = 0

recent_trades = []
recent_waivers = []
recent_drops = []

latest_week = max(transactions.keys(), key=int)

for t in transactions[latest_week]:

    ttype = t["type"]

    if ttype == "trade":
        trade_count += 1

        teams = [
            owner_lookup.get(r, str(r))
            for r in t.get("roster_ids", [])
        ]

        recent_trades.append(
            " ↔ ".join(teams)
        )

    elif ttype == "waiver":
        waiver_count += 1

        if t.get("adds"):
            for pid, roster in t["adds"].items():
                recent_waivers.append(
                    (
                        player_lookup.get(pid, pid),
                        owner_lookup.get(roster, roster)
                    )
                )

    elif ttype == "free_agent":
        free_agent_count += 1

    for roster in t.get("roster_ids", []):
        activity[owner_lookup.get(roster, roster)] += 1

    if t.get("drops"):
        for pid in t["drops"]:
            recent_drops.append(
                player_lookup.get(pid, pid)
            )


# ------------------------------------------
# Build report
# ------------------------------------------

report = []

report.append("# Tyler Dynasty GM Report")
report.append("")
report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
report.append("")
report.append("---")
report.append("")
report.append("## League Overview")
report.append("")
report.append(f"League: {league['name']}")
report.append(f"Season: {league['season']}")
report.append(f"Teams: {league['total_rosters']}")
report.append(f"Available Players: {len(waiver_board)}")
report.append("")
report.append("---")
report.append("")
report.append("## League Activity")
report.append("")
report.append(f"Trades: {trade_count}")
report.append(f"Waiver Claims: {waiver_count}")
report.append(f"Free Agent Moves: {free_agent_count}")
report.append("")
report.append("---")
report.append("")
report.append("## Recent Trades")
report.append("")

if recent_trades:
    for trade in recent_trades:
        report.append(f"- {trade}")
else:
    report.append("No trades.")

report.append("")
report.append("---")
report.append("")
report.append("## Top Waiver Claims")
report.append("")

if recent_waivers:
    for player, owner in recent_waivers[:10]:
        report.append(f"- {player} → {owner}")
else:
    report.append("No waiver claims.")

report.append("")
report.append("---")
report.append("")
report.append("## Recently Dropped Players")
report.append("")

if recent_drops:
    for player in recent_drops[:15]:
        report.append(f"- {player}")
else:
    report.append("No recent drops.")

report.append("")
report.append("---")
report.append("")
report.append("## Most Active Managers")
report.append("")

for owner, moves in activity.most_common():
    report.append(f"- {owner}: {moves} moves")

report.append("")
report.append("---")
report.append("")
report.append("End of Report")

with open(REPORTS / "daily_gm_report.md", "w") as f:
    f.write("\n".join(report))

print("Created reports/daily_gm_report.md")