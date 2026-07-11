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

league = fetch(f"league/{LEAGUE_ID}")
users = fetch(f"league/{LEAGUE_ID}/users")
rosters = fetch(f"league/{LEAGUE_ID}/rosters")
traded_picks = fetch(f"league/{LEAGUE_ID}/traded_picks")
drafts = fetch(f"league/{LEAGUE_ID}/drafts")
nfl_state = fetch("state/nfl")

snapshot = {
    "league": league,
    "users": users,
    "rosters": rosters,
    "traded_picks": traded_picks,
    "drafts": drafts,
    "nfl_state": nfl_state
}

with open(data_dir / "league_snapshot.json", "w") as f:
    json.dump(snapshot, f, indent=2)

with open(data_dir / "users.json", "w") as f:
    json.dump(users, f, indent=2)

with open(data_dir / "rosters.json", "w") as f:
    json.dump(rosters, f, indent=2)

with open(data_dir / "traded_picks.json", "w") as f:
    json.dump(traded_picks, f, indent=2)

with open(data_dir / "drafts.json", "w") as f:
    json.dump(drafts, f, indent=2)

with open(data_dir / "league.json", "w") as f:
    json.dump(league, f, indent=2)

with open(data_dir / "nfl_state.json", "w") as f:
    json.dump(nfl_state, f, indent=2)

print("League snapshot updated successfully.")
print("Saved:")
print(" - league.json")
print(" - users.json")
print(" - rosters.json")
print(" - traded_picks.json")
print(" - drafts.json")
print(" - nfl_state.json")
print(" - league_snapshot.json")