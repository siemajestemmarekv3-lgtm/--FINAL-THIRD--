MAX_ATTEMPTS = 9
attempts = 0
import json

with open("players.json", "r", encoding="utf-8") as f:
    players = json.load(f)

import json

with open("grid.json", "r", encoding="utf-8") as f:
    grid = json.load(f)

ROWS = grid["rows"]
COLS = grid["cols"]

used_players = set()
board = [[None for _ in range(3)] for _ in range(3)]

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

    # exact match
    for player in players:
        if player["name"].lower() == name:
            return player

    # partial match
    matches = []
    for player in players:
        if name in player["name"].lower():
            matches.append(player)

    if len(matches) == 1:
        return matches[0]

    if len(matches) > 1:
        print("\nMultiple matches found:")
        for i, p in enumerate(matches[:5]):
            print(f"{i}: {p['name']}")

        try:
            choice = int(input("Choose player index: "))
            return matches[choice]
        except:
            return None

    return None

def validate_cell_answer(player_name, row_index, col_index):
    player = find_player_by_name(player_name)

    if player is None:
        return False, "Player not found."

    if player["name"] in used_players:
        return False, "Player already used in this grid."

    row_condition = ROWS[row_index]
    col_condition = COLS[col_index]

    if not check_two_conditions(player, row_condition, col_condition):
        return False, "Player does not match both conditions."

    return True, player["name"]

def print_conditions():
    print("\nROWS:")
    for i, row in enumerate(ROWS):
        print(f"{i}: {row['value']} ({row['type']})")

    print("\nCOLS:")
    for i, col in enumerate(COLS):
        print(f"{i}: {col['value']} ({col['type']})")

def print_board():
    print("\nBOARD:")
    for i in range(3):
        row_display = []
        for j in range(3):
            value = board[i][j]
            row_display.append(value if value is not None else "[empty]")
        print(" | ".join(row_display))

def board_full():
    for row in board:
        for cell in row:
            if cell is None:
                return False
    return True

print("FinalThird - Terminal Beta")
print_conditions()

while not board_full() and attempts < MAX_ATTEMPTS:
    print_board()

    try:
        row_index = int(input("\nChoose row (0-2): ").strip())
        col_index = int(input("Choose col (0-2): ").strip())
    except ValueError:
        print("Invalid input. Use numbers 0, 1, 2.")
        continue

    if row_index not in [0, 1, 2] or col_index not in [0, 1, 2]:
        print("Row and col must be between 0 and 2.")
        continue

    if board[row_index][col_index] is not None:
        print("That cell is already filled.")
        continue

    player_name = input("Enter player name (or type 'exit'): ").strip()

    if player_name.lower() == "exit":
        break

    is_valid, result = validate_cell_answer(player_name, row_index, col_index)
    attempts += 1
    print(f"Attempts: {attempts}/{MAX_ATTEMPTS}")

    if is_valid:
        board[row_index][col_index] = result
        used_players.add(result)
        print(f"Correct: {result}")
    else:
        print(result)

print("\nFinal board:")
print_board()

if board_full():
    print("\nWIN")
else:
    print("\nLOSE")