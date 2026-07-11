import json
from pathlib import Path

import requests

LEAGUE_ID = "1326711861197938688"
BASE_URL = "https://api.sleeper.app/v1"

DATA = Path("data")
DATA.mkdir(exist_ok=True)


def fetch(endpoint):
    url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()


all_transactions = {}

print("Downloading league transactions...")

# Download every fantasy week
for week in range(1, 19):
    tx = fetch(f"league/{LEAGUE_ID}/transactions/{week}")

    if tx:
        print(f"Week {week}: {len(tx)} transactions")
        all_transactions[str(week)] = tx

with open(DATA / "transactions.json", "w") as f:
    json.dump(all_transactions, f, indent=2)

print(f"Downloaded transactions for {len(all_transactions)} weeks.")