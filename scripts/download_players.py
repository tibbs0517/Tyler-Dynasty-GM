import json
import requests
from pathlib import Path

BASE_URL = "https://api.sleeper.app/v1"

print("Downloading Sleeper player database...")

response = requests.get(f"{BASE_URL}/players/nfl", timeout=120)
response.raise_for_status()

players = response.json()

data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

with open(data_dir / "players.json", "w") as f:
    json.dump(players, f)

print(f"Downloaded {len(players)} players.")
