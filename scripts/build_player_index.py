import json
from pathlib import Path

data_dir = Path("data")

with open(data_dir / "players.json", "r") as f:
    players = json.load(f)

player_index = {}

for player_id, player in players.items():
    player_index[player_id] = {
        "name": player.get("full_name"),
        "position": player.get("position"),
        "team": player.get("team"),
        "status": player.get("status"),
        "active": player.get("active", False)
    }

with open(data_dir / "player_index.json", "w") as f:
    json.dump(player_index, f, indent=2)

print(f"Indexed {len(player_index)} players.")
