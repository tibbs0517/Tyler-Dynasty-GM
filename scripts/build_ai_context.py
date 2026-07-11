import json
from pathlib import Path
from datetime import datetime

DATA = Path("data")

def load(name):
    with open(DATA / name, "r") as f:
        return json.load(f)

league = load("league.json")
users = load("users.json")
rosters = load("rosters.json")
transactions = load("transactions.json")
waiver_board = load("waiver_board.json")
players = load("players.json")
league_database = load("league_database.json")

# Find your user
my_user = next(
    u for u in users
    if u["display_name"].lower() == "tylergratz"
)

my_roster = next(
    r for r in rosters
    if r["owner_id"] == my_user["user_id"]
)

ai_context = {
    "generated": datetime.now().isoformat(),

    "league": {
        "name": league["name"],
        "season": league["season"],
        "teams": league["total_rosters"],
        "scoring": league["scoring_settings"]
    },

    "me": {
        "username": my_user["display_name"],
        "user_id": my_user["user_id"],
        "roster_id": my_roster["roster_id"],
        "players": my_roster["players"],
        "starters": my_roster["starters"]
    },

    "users": users,
    "rosters": rosters,

    "transactions": transactions,

    "waiver_board": waiver_board,

    "league_database": league_database,

    "players": players
}

with open(DATA / "ai_context.json", "w") as f:
    json.dump(ai_context, f, indent=2)

print("Created data/ai_context.json")
