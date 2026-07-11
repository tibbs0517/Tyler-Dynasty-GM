import json
from pathlib import Path

DATA_DIR = Path("data")

# Load league snapshot
with open(DATA_DIR / "league_snapshot.json", "r") as f:
    snapshot = json.load(f)

# Load player index
with open(DATA_DIR / "player_index.json", "r") as f:
    player_index = json.load(f)

# Collect every rostered player ID
rostered = set()

for roster in snapshot["rosters"]:
    for player_id in roster.get("players") or []:
        rostered.add(str(player_id))

# Find every unrostered offensive player
unrostered = []

OFFENSIVE_POSITIONS = {"QB", "RB", "WR", "TE"}

for player_id, player in player_index.items():

    if player_id in rostered:
        continue

    if not player["active"]:
        continue

    if player["position"] not in OFFENSIVE_POSITIONS:
        continue

    unrostered.append({
        "id": player_id,
        "name": player["name"],
        "position": player["position"],
        "team": player["team"],
        "status": player["status"]
    })

# Sort alphabetically
unrostered.sort(key=lambda x: x["name"] or "")

with open(DATA_DIR / "unrostered_players.json", "w") as f:
    json.dump(unrostered, f, indent=2)

print(f"Found {len(unrostered)} unrostered offensive players.")
