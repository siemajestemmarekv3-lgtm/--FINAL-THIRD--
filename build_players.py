import pandas as pd
import zipfile
import json

ZIP_PATH = "archive.zip"
TOP_LEAGUES = ["GB1", "ES1", "IT1", "L1", "FR1"]

LEAGUE_NAME_MAP = {
    "GB1": "Premier League",
    "ES1": "La Liga",
    "IT1": "Serie A",
    "L1": "Bundesliga",
    "FR1": "Ligue 1"
}

POSITION_MAP = {
    "Attack": "Forward",
    "Midfield": "Midfielder",
    "Defender": "Defender",
    "Goalkeeper": "Goalkeeper"
}

CLUB_NAME_MAP = {
    "Manchester City Football Club": "Manchester City",
    "Liverpool Football Club": "Liverpool",
    "Brighton and Hove Albion Football Club": "Brighton",
    "Borussia Dortmund": "Borussia Dortmund",
    "1. Fußball- und Sportverein Mainz 05": "Mainz 05",
    "Borussia Verein für Leibesübungen 1900 Mönchengladbach": "Borussia Mönchengladbach",
    "Bayer 04 Leverkusen Fußball": "Bayer Leverkusen",
    "Angers Sporting Club de l'Ouest": "Angers",
    "Manchester United Football Club": "Manchester United",
    "FC Bayern München": "Bayern Munich",
    "Girona Fútbol Club S. A. D.": "Girona",
    "Football Club Internazionale Milano S.p.A.": "Inter Milan",
    "Aston Villa Football Club": "Aston Villa",
    "Everton Football Club": "Everton",
    "Real Madrid Club de Fútbol": "Real Madrid",
    "Società Sportiva Calcio Napoli": "Napoli",
    "Arsenal Football Club": "Arsenal",
    "Villarreal Club de Fútbol, S.A.D.": "Villarreal",
    "Sevilla Fútbol Club S.A.D.": "Sevilla",
    "Olympique Gymnaste Club Nice Côte d'Azur": "Nice",
    "Olympique de Marseille": "Marseille",
    "Crystal Palace Football Club": "Crystal Palace",
    "Sporting Gijón": "Sporting Gijón",
    "CD Leganés": "Leganés",
    "Real Club Deportivo Mallorca, S.A.D.": "Mallorca",
    "Udinese Calcio": "Udinese",
    "Torino Calcio": "Torino",
    "Association Sportive de Monaco Football Club": "Monaco",
    "Paris Saint-Germain Football Club": "PSG",
    "Chelsea Football Club": "Chelsea",
    "Tottenham Hotspur Football Club": "Tottenham",
    "West Ham United Football Club": "West Ham",
    "Leicester City": "Leicester City",
    "Wolverhampton Wanderers Football Club": "Wolves",
    "Newcastle United Football Club": "Newcastle United",
    "Association de la Jeunesse Auxerroise": "Auxerre",
    "Olympique Lyonnais": "Lyon",
    "Football Club de Nantes": "Nantes",
    "Lille Olympique Sporting Club Lille Métropole": "Lille",
    "Stade Rennais Football Club 1901": "Rennes",
    "Bologna Football Club 1909": "Bologna",
    "Associazione Calcio Milan": "AC Milan",
    "Juventus Football Club": "Juventus",
    "Associazione Sportiva Roma": "Roma",
    "Società Sportiva Lazio": "Lazio",
    "Atalanta Bergamasca Calcio": "Atalanta",
    "ACF Fiorentina": "Fiorentina",
    "Bayer 04 Leverkusen": "Bayer Leverkusen",
    "Fußball-Club Augsburg 1907": "Augsburg",
    "RasenBallsport Leipzig": "RB Leipzig",
    "VfB Stuttgart 1893": "Stuttgart",
    "Verein für Bewegungsspiele Stuttgart 1893": "Stuttgart",
    "Eintracht Frankfurt": "Eintracht Frankfurt",
    "Verein für Bewegungsspiele Wolfsburg": "Wolfsburg",
    "Club Atlético de Madrid S.A.D.": "Atlético Madrid",
    "Futbol Club Barcelona": "Barcelona",
    "FC Barcelona": "Barcelona",
    "Valencia Club de Fútbol, S.A.D.": "Valencia",
    "Real Betis Balompié S.A.D.": "Real Betis",
    "Real Sociedad de Fútbol S.A.D.": "Real Sociedad",
    "Athletic Club": "Athletic Club"
}

with zipfile.ZipFile(ZIP_PATH) as z:
    players = pd.read_csv(z.open("players.csv"))
    appearances = pd.read_csv(z.open("appearances.csv"))
    clubs = pd.read_csv(z.open("clubs.csv"))

active_players = players[players["last_season"] >= 2024].copy()

active_top5_players = active_players[
    active_players["current_club_domestic_competition_id"].isin(TOP_LEAGUES)
].copy()

top5_player_ids = set(active_top5_players["player_id"])

top5_appearances = appearances[
    (appearances["player_id"].isin(top5_player_ids)) &
    (appearances["competition_id"].isin(TOP_LEAGUES))
].copy()

club_map = clubs.set_index("club_id")["name"].to_dict()
top5_appearances["club_name"] = top5_appearances["player_club_id"].map(club_map)

def normalize_club_name(name):
    if pd.isna(name):
        return None
    name = str(name).strip()
    return CLUB_NAME_MAP.get(name, name)

def unique_non_null(series):
    values = []
    for x in series.dropna():
        x = str(x).strip()
        if x and x not in values:
            values.append(x)
    return values

def map_leagues(ids):
    result = []
    for league_id in ids:
        if league_id in LEAGUE_NAME_MAP:
            result.append(LEAGUE_NAME_MAP[league_id])
    return result

top5_appearances["club_name"] = top5_appearances["club_name"].apply(normalize_club_name)

player_history = top5_appearances.groupby("player_id").agg({
    "club_name": unique_non_null,
    "competition_id": unique_non_null
}).reset_index()

appearance_counts = top5_appearances.groupby("player_id").size().reset_index(name="appearance_count")

merged = active_top5_players[[
    "player_id",
    "name",
    "country_of_citizenship",
    "position",
    "sub_position",
    "current_club_name"
]].merge(player_history, on="player_id", how="inner")

merged = merged.merge(appearance_counts, on="player_id", how="left")

merged["leagues"] = merged["competition_id"].apply(map_leagues)
merged["primary_position"] = merged["position"].map(POSITION_MAP)

merged = merged[
    (merged["appearance_count"] >= 5) &
    (merged["country_of_citizenship"].notna()) &
    (merged["primary_position"].notna())
].copy()

result = []

for _, row in merged.iterrows():
    clubs_list = row["club_name"] if isinstance(row["club_name"], list) else []
    leagues_list = row["leagues"] if isinstance(row["leagues"], list) else []

    if not clubs_list or not leagues_list:
        continue

    result.append({
        "name": row["name"],
        "nationality": row["country_of_citizenship"],
        "positions": [row["primary_position"]],
        "clubs": clubs_list,
        "leagues": leagues_list,
        "achievements": []
    })

with open("players.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("FINAL merged rows:", len(merged))
print("FINAL json players:", len(result))
print(result[:5])
print("Saved to players.json")