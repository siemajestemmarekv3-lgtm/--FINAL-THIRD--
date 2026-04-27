import json

with open("players.json", "r", encoding="utf-8") as f:
    players = json.load(f)

ROWS = [
    {"type": "club", "value": "Manchester United"},
    {"type": "club", "value": "Juventus"},
    {"type": "club", "value": "Arsenal"},
]

COLS = [
    {"type": "nationality", "value": "Brazil"},
    {"type": "position", "value": "Midfielder"},
    {"type": "nationality", "value": "France"},
]

used_players = set()

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
        check_player_condition(player, condition_1)
        and check_player_condition(player, condition_2)
    )

def find_player_by_name(name):
    name = name.strip().lower()
    for player in players:
        if player["name"].strip().lower() == name:
            return player
    return None

def validate_cell_answer(player_name, row_index, col_index, used_players):
    player = find_player_by_name(player_name)

    if player is None:
        return False, "Player not found."

    if player["name"] in used_players:
        return False, "Player already used in this grid."

    row_condition = ROWS[row_index]
    col_condition = COLS[col_index]

    if not check_two_conditions(player, row_condition, col_condition):
        return False, "Player does not match both conditions."

    return True, f"Correct: {player['name']}"

test_answers = [
    ("Casemiro", 0, 0),          # Manchester United + Brazil
    ("Paul Pogba", 0, 2),        # Manchester United + France
    ("Paul Pogba", 1, 1),        # Juventus + Midfielder -> should fail because already used
    ("William Saliba", 2, 2),    # Arsenal + France
    ("David Raya", 2, 0),        # Arsenal + Brazil -> should fail
]

for player_name, row_index, col_index in test_answers:
    is_valid, message = validate_cell_answer(player_name, row_index, col_index, used_players)
    print(f"{player_name} -> {message}")
    if is_valid:
        used_players.add(player_name)