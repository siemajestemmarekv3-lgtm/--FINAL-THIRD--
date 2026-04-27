import json
from conditions import BETA_CONDITIONS

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
    return check_player_condition(player, condition_1) and check_player_condition(player, condition_2)

def count_matches(players, condition_1, condition_2):
    count = 0
    for player in players:
        if check_two_conditions(player, condition_1, condition_2):
            count += 1
    return count

rows = [
    {"type": "club", "value": "Arsenal"},
    {"type": "club", "value": "Manchester United"},
    {"type": "club", "value": "Real Madrid"},
]

cols = [
    {"type": "nationality", "value": "England"},
    {"type": "position", "value": "Goalkeeper"},
    {"type": "club", "value": "Chelsea"},
]

print("GRID TEST\n")

for row in rows:
    for col in cols:
        count = count_matches(players, row, col)
        print(f"{row['value']} + {col['value']} -> {count}")