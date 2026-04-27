import json
import random

with open("players.json", "r", encoding="utf-8") as f:
    players = json.load(f)

ROW_CONDITIONS = [
    {"type": "club", "value": "Arsenal"},
    {"type": "club", "value": "Chelsea"},
    {"type": "club", "value": "Liverpool"},
    {"type": "club", "value": "Manchester United"},
    {"type": "club", "value": "Manchester City"},
    {"type": "club", "value": "Real Madrid"},
    {"type": "club", "value": "Barcelona"},
    {"type": "club", "value": "Bayern Munich"},
    {"type": "club", "value": "Juventus"},
    {"type": "league", "value": "Premier League"},
    {"type": "league", "value": "La Liga"},
    {"type": "league", "value": "Serie A"},
    {"type": "league", "value": "Bundesliga"},
    {"type": "league", "value": "Ligue 1"},
]

COL_CONDITIONS = [
    {"type": "nationality", "value": "England"},
    {"type": "nationality", "value": "Brazil"},
    {"type": "nationality", "value": "France"},
    {"type": "nationality", "value": "Argentina"},
    {"type": "nationality", "value": "Spain"},
    {"type": "nationality", "value": "Germany"},
    {"type": "nationality", "value": "Portugal"},
    {"type": "position", "value": "Forward"},
    {"type": "position", "value": "Midfielder"},
    {"type": "position", "value": "Defender"},
    {"type": "position", "value": "Goalkeeper"},
    {"type": "club", "value": "Arsenal"},
    {"type": "club", "value": "Chelsea"},
    {"type": "club", "value": "Liverpool"},
    {"type": "club", "value": "Manchester United"},
    {"type": "club", "value": "Manchester City"},
    {"type": "club", "value": "Real Madrid"},
    {"type": "club", "value": "Barcelona"},
    {"type": "club", "value": "Bayern Munich"},
    {"type": "club", "value": "Juventus"},
]

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

def find_players_for_cell(players, condition_1, condition_2):
    matches = []

    for player in players:
        if check_two_conditions(player, condition_1, condition_2):
            matches.append(player["name"])

    return matches

def find_grid_data(players, rows, cols):
    grid_data = []

    for row in rows:
        row_data = []
        for col in cols:
            matches = find_players_for_cell(players, row, col)
            row_data.append(matches)
        grid_data.append(row_data)

    return grid_data

def is_valid_grid(grid_data, min_answers_per_cell=3, max_answers_per_cell=40):
    for row in grid_data:
        for matches in row:
            count = len(matches)
            if count < min_answers_per_cell:
                return False
            if count > max_answers_per_cell:
                return False
    return True

def generate_valid_grid(players, row_conditions, col_conditions, max_attempts=5000):
    for _ in range(max_attempts):
        rows = random.sample(row_conditions, 3)
        cols = random.sample(col_conditions, 3)

        # optional: avoid same exact condition appearing in both row and col
        row_keys = {(r["type"], r["value"]) for r in rows}
        col_keys = {(c["type"], c["value"]) for c in cols}
        if row_keys & col_keys:
            continue

        grid_data = find_grid_data(players, rows, cols)

        if is_valid_grid(grid_data, min_answers_per_cell=3, max_answers_per_cell=40):
            return rows, cols, grid_data

    return None, None, None

rows, cols, grid_data = generate_valid_grid(
    players,
    ROW_CONDITIONS,
    COL_CONDITIONS,
    max_attempts=10000
)

if rows is None:
    print("No valid grid found.")
else:
    print("VALID GRID FOUND\n")

    print("ROWS:")
    for row in rows:
        print(row)

    print("\nCOLS:")
    for col in cols:
        print(col)

    print("\nGRID:")
    for i, row in enumerate(rows):
        print(f"\nROW: {row}")
        for j, col in enumerate(cols):
            matches = grid_data[i][j]
            print(f"  CELL {row['value']} + {col['value']} -> {len(matches)}")
            print(f"    {matches[:10]}")
import json

if rows is None:
    print("No valid grid found.")
else:
    grid = {
        "rows": rows,
        "cols": cols
    }

    with open("grid.json", "w", encoding="utf-8") as f:
        json.dump(grid, f, ensure_ascii=False, indent=2)

    print("Grid saved to grid.json")