from utils import load_json, save_json

players = load_json("enriched_players.json")

POSITION_BASE = {
    "QB": 95,   # Superflex premium
    "RB": 80,
    "WR": 85,
    "TE": 70
}

def calculate_score(player):
    if not player["active"]:
        return 0

    position = player.get("position")
    if position not in POSITION_BASE:
        return 0

    score = POSITION_BASE[position]

    age = player.get("age")
    if isinstance(age, int):
        if position == "QB":
            if age <= 26:
                score += 5
            elif age >= 34:
                score -= 15
        elif position == "RB":
            if age <= 23:
                score += 10
            elif age >= 28:
                score -= 15
        elif position == "WR":
            if age <= 25:
                score += 8
            elif age >= 30:
                score -= 12
        elif position == "TE":
            if age <= 24:
                score += 5
            elif age >= 31:
                score -= 8

    if not player["rostered"]:
        score -= 20

    return max(0, min(100, score))

values = []

for player in players.values():
    score = calculate_score(player)

    if score == 0:
        continue

    values.append({
        **player,
        "gm_score": score
    })

values.sort(key=lambda p: p["gm_score"], reverse=True)

save_json("player_values.json", values)

print(f"Scored {len(values)} players.")
