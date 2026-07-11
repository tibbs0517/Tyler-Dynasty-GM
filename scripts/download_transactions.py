import json
import requests
from pathlib import Path

LEAGUE_ID = "1326711861197938688"
BASE_URL = "https://api.sleeper.app/v1"

DATA = Path("data")
DATA.mkdir(exist_ok=True)

def fetch(endpoint):
    url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()

# Get NFL state to determine current week
state = fetch("state/nfl")
current_week = state.get("week", 1)

all_transactions = {}

print(f"Downloading transactions through Week {current_week}...")

for week in range(1, current_week + 1):
    try:
        tx = fetch(f"league/{LEAGUE_ID}/transactions/{week}")
        all_transactions[str(week)] = tx
        print(f"Week {week}: {len(tx)} transactions")
    except Exception as e:
        print(f"Week {week}: skipped ({e})")

with open(DATA / "transactions.json", "w") as f:
    json.dump(all_transactions, f, indent=2)

print("transactions.json created.")
