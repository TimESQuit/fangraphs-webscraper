import pandas as pd
from sqlalchemy import create_engine

# Combines all batter csvs into one batter dataframe
batter_dfs = []
year = 2020
while year > 1870:
    file = f"~/Downloads/Data/Batting/{year}.csv"
    df = pd.read_csv(file)
    df.insert(2, "Year", year)
    batter_dfs.append(df)
    year -= 1
batters = pd.concat(batter_dfs, axis=0, ignore_index=0)

# This is a helper function to convert 'xx%' values to '.xx'


def percentage_to_decimal(num):
    if pd.isnull(num):
        return num
    else:
        num = num[:-1]
        return float(num)/100


for field in ['BB%', 'K%']:
    batters[field] = list(
        map(percentage_to_decimal, batters[field].values))

# for field in ['RBI', 'wRC+']:
#     batters[field] = list(
#         map(lambda x: int(x) if not pd.isnull(x) else x, batters[field].values))

pitcher_dfs = []
year = 2020
while year > 1870:
    file = f"~/Downloads/Data/Pitching/{year}.csv"
    df = pd.read_csv(file)
    df.insert(2, "Year", year)
    pitcher_dfs.append(df)
    year -= 1
pitchers = pd.concat(pitcher_dfs, axis=0, ignore_index=0)

for field in ['LOB%', 'GB%', 'HR/FB']:
    pitchers[field] = list(
        map(percentage_to_decimal, pitchers[field].values))

# pitchers.to_csv("~/Downloads/Pitchers.csv", index=False)

batter_player_info = batters[['Name', 'playerid']]

pitcher_player_info = pitchers[['Name', 'playerid']]

players = [batter_player_info, pitcher_player_info]
players = pd.concat(players, axis=0, ignore_index=0)

players_unique = players.drop_duplicates()

players_unique.to_csv("~/Downloads/player_info.csv", index=False)

# batters.to_csv("~/Downloads/Batters.csv", index=False)

# engine = create_engine('sqlite:///site.db', echo=False)

# batters.to_sql('Batters', con=engine)
