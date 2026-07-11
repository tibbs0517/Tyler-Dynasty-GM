import json
from pathlib import Path

DATA = Path("data")

with open(DATA / "league_snapshot.json") as f:
    snapshot = json.load(f)

with open(DATA / "players.json") as f:
    players = json.load(f)

# Build lookup of player -> roster owner
ownership = {}

for roster in snapshot["rosters"]:
    roster_id = roster["roster_id"]

    for player_id in roster.get("players") or []:
        ownership[str(player_id)] = roster_id

enriched = {}

for player_id, player in players.items():

    enriched[player_id] = {
        "id": player_id,
        "name": player.get("full_name"),
        "position": player.get("position"),
        "team": player.get("team"),
        "age": player.get("age"),
        "years_exp": player.get("years_exp"),
        "active": player.get("active"),
        "injury_status": player.get("injury_status"),
        "bye_week": player.get("bye_week"),
        "rostered": player_id in ownership,
        "roster_id": ownership.get(player_id)
    }

with open(DATA / "enriched_players.json", "w") as f:
    json.dump(enriched, f, indent=2)

print(f"Created enriched database for {len(enriched)} players.")
