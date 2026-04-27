import json

with open("players.json", "r", encoding="utf-8") as f:
    players = json.load(f)

def check_player_condition(player, condition):
    condition_type = condition["type"]
    condition_value = condition["value"]

    if condition_type == "club":
        return condition_value in player["clubs"]

    if condition_type == "nationality":
        return condition_value == player["nationality"]

    if condition_type == "league":
        return condition_value in player["leagues"]

    if condition_type == "position":
        return condition_value in player["positions"]

    return False

def check_two_conditions(player, condition_1, condition_2):
    return (
        check_player_condition(player, condition_1) and
        check_player_condition(player, condition_2)
    )

def find_players_for_cell(players, condition_1, condition_2, limit=10):
    matches = []

    for player in players:
        if check_two_conditions(player, condition_1, condition_2):
            matches.append(player["name"])

    return matches[:limit]

rows = [
    {"type": "club", "value": "Arsenal"},
    {"type": "club", "value": "Manchester United"},
    {"type": "league", "value": "Premier League"},
]

cols = [
    {"type": "nationality", "value": "England"},
    {"type": "position", "value": "Goalkeeper"},
    {"type": "club", "value": "Chelsea"},
]

for row in rows:
    print(f"\nROW: {row}")

    for col in cols:
        matches = find_players_for_cell(players, row, col, limit=10)
        print(f"  CELL {row['value']} + {col['value']}: {len(matches)} matches")
        print(f"    {matches}")