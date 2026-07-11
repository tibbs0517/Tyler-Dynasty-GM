import json
from pathlib import Path
from collections import Counter
from datetime import datetime

DATA = Path("data")
REPORTS = Path("reports")
CONFIG_FILE = Path("config.json")

REPORTS.mkdir(exist_ok=True)


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


config = load_json(CONFIG_FILE)

league = load_json(DATA / "league.json")
transactions = load_json(DATA / "transactions.json")
waiver_board = load_json(DATA / "waiver_board.json")
rosters = load_json(DATA / "rosters.json")
users = load_json(DATA / "users.json")
players = load_json(DATA / "players.json")

# ----------------------------------------------------
# Configuration
# ----------------------------------------------------

MY_ROSTER_ID = config["roster_id"]
MY_USERNAME = config["username"]
REPORT_NAME = config["report_name"]

# ----------------------------------------------------
# Player Lookup
# ----------------------------------------------------

player_lookup = {}

for pid, player in players.items():

    name = player.get("full_name")

    if not name:
        name = (
            player.get("first_name", "")
            + " "
            + player.get("last_name", "")
        ).strip()

    if not name:
        name = pid

    player_lookup[pid] = name

# ----------------------------------------------------
# Owner Lookup
# ----------------------------------------------------

owner_lookup = {}

for roster in rosters:

    owner = str(roster["roster_id"])

    for user in users:
        if user["user_id"] == roster["owner_id"]:
            owner = user["display_name"]
            break

    owner_lookup[roster["roster_id"]] = owner

# ----------------------------------------------------
# Collect statistics
# ----------------------------------------------------

activity = Counter()

trade_count = 0
waiver_count = 0
free_agent_count = 0

recent_trades = []
recent_waivers = []
recent_drops = []

latest_week = max(transactions.keys(), key=int)

for transaction in transactions[latest_week]:

    ttype = transaction["type"]

    if ttype == "trade":

        trade_count += 1

        teams = [
            owner_lookup.get(r, str(r))
            for r in transaction.get("roster_ids", [])
        ]

        recent_trades.append(" ↔ ".join(teams))

    elif ttype == "waiver":

        waiver_count += 1

        if transaction.get("adds"):

            for pid, roster in transaction["adds"].items():

                recent_waivers.append(
                    (
                        player_lookup.get(pid, pid),
                        owner_lookup.get(roster, roster)
                    )
                )

    elif ttype == "free_agent":

        free_agent_count += 1

    for roster in transaction.get("roster_ids", []):

        activity[owner_lookup.get(roster, roster)] += 1

    if transaction.get("drops"):

        for pid in transaction["drops"]:

            recent_drops.append(player_lookup.get(pid, pid))

# ----------------------------------------------------
# Find My Team
# ----------------------------------------------------

my_roster = None

for roster in rosters:

    if roster["roster_id"] == MY_ROSTER_ID:

        my_roster = roster
        break

# ----------------------------------------------------
# Build Report
# ----------------------------------------------------

report = []

report.append(f"# {REPORT_NAME}")
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
report.append("## My Front Office")
report.append("")
report.append(f"Username: {MY_USERNAME}")
report.append(f"Roster ID: {MY_ROSTER_ID}")

if my_roster:
    report.append(f"Players on Roster: {len(my_roster['players'])}")

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

seen = set()

for player, owner in recent_waivers:

    key = (player, owner)

    if key in seen:
        continue

    seen.add(key)

    report.append(f"- {player} → {owner}")

report.append("")
report.append("---")
report.append("")
report.append("## Recently Dropped Players")
report.append("")

for player in recent_drops[:15]:
    report.append(f"- {player}")

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