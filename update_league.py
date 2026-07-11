import json
import requests

LEAGUE_ID = "1326711861197938688"
BASE_URL = "https://api.sleeper.app/v1"

def fetch(endpoint):
    url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()

print("Downloading league information...")

league = fetch(f"league/{LEAGUE_ID}")
users = fetch(f"league/{LEAGUE_ID}/users")
rosters = fetch(f"league/{LEAGUE_ID}/rosters")

snapshot = {
    "league": league,
    "users": users,
    "rosters": rosters
}

with open("league_snapshot.json", "w") as f:
    json.dump(snapshot, f, indent=2)

print("League snapshot created successfully.")