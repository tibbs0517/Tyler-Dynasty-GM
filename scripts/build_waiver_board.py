from utils import load_json, save_json

players = load_json("enriched_players.json")

available = []

for player in players.values():

    if player["rostered"]:
        continue

    if not player["active"]:
        continue

    if player["position"] not in ["QB","RB","WR","TE"]:
        continue

    available.append(player)

available.sort(key=lambda p: (
    p["position"],
    p["name"] or ""
))

save_json("waiver_board.json", available)

print(f"{len(available)} waiver players written.")
