import json
from pathlib import Path

DATA = Path("data")

with open(DATA / "transactions.json") as f:
    transactions = json.load(f)

with open(DATA / "players.json") as f:
    players = json.load(f)

with open(DATA / "users.json") as f:
    users = json.load(f)

with open(DATA / "rosters.json") as f:
    rosters = json.load(f)

# ------------------------------------------
# Build lookup dictionaries
# ------------------------------------------

player_lookup = {}

for pid, player in players.items():
    name = player.get("full_name")

    if not name:
        first = player.get("first_name", "")
        last = player.get("last_name", "")
        name = (first + " " + last).strip()

    if not name:
        name = pid

    player_lookup[pid] = name

owner_lookup = {}

for roster in rosters:
    owner_id = roster["owner_id"]
    roster_id = roster["roster_id"]

    username = owner_id

    for user in users:
        if user["user_id"] == owner_id:
            username = user["display_name"]
            break

    owner_lookup[roster_id] = username

# ------------------------------------------
# Print Transactions
# ------------------------------------------

for week in sorted(transactions.keys(), key=int):

    print(f"\n===================")
    print(f"Week {week}")
    print("===================\n")

    for t in transactions[week]:

        print(t["type"].upper())

        if t.get("adds"):
            for pid, roster in t["adds"].items():
                print(
                    f"ADD  : {player_lookup.get(pid,pid)} -> {owner_lookup.get(roster,roster)}"
                )

        if t.get("drops"):
            for pid, roster in t["drops"].items():
                print(
                    f"DROP : {player_lookup.get(pid,pid)} <- {owner_lookup.get(roster,roster)}"
                )

        if t.get("draft_picks"):

            print("PICKS")

            for p in t["draft_picks"]:

                print(
                    f"{p['season']} Round {p['round']} "
                    f"Roster {p['previous_owner_id']} -> "
                    f"Roster {p['owner_id']}"
                )

        print()
