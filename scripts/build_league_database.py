import json
from pathlib import Path

DATA = Path("data")

with open(DATA / "league_snapshot.json") as f:
    snapshot = json.load(f)

with open(DATA / "player_index.json") as f:
    player_index = json.load(f)

with open(DATA / "unrostered_players.json") as f:
    unrostered = json.load(f)

league_database = {
    "league": snapshot["league"],
    "users": snapshot["users"],
    "rosters": snapshot["rosters"],
    "players": player_index,
    "unrostered_players": unrostered
}

with open(DATA / "league_database.json", "w") as f:
    json.dump(league_database, f, indent=2)

print("League database created successfully.")
