import json
import requests
from pathlib import Path

LEAGUE_ID = "1326711861197938688"
BASE_URL = "https://api.sleeper.app/v1"

def fetch(endpoint):
    url = f"{BASE_URL}/{endpoint}"
    print(f"Downloading {endpoint}...")
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()

data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

snapshot = {
    "league": fetch(f"league/{LEAGUE_ID}"),
    "users": fetch(f"league/{LEAGUE_ID}/users"),
    "rosters": fetch(f"league/{LEAGUE_ID}/rosters"),
    "traded_picks": fetch(f"league/{LEAGUE_ID}/traded_picks"),
    "drafts": fetch(f"league/{LEAGUE_ID}/drafts"),
    "nfl_state": fetch("state/nfl")
}

with open(data_dir / "league_snapshot.json", "w") as f:
    json.dump(snapshot, f, indent=2)

print("League snapshot updated successfully.")