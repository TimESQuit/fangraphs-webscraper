import pandas as pd
import numpy as np

from helper_functions import ip_fraction_handler, percentage_to_decimal

batter_dfs = []
pitcher_dfs = []

year = 2020

# This combines all years' data into one list of dfs for each Batting and Pitching.
while year > 1870:
    kinds = ['Batting', 'Pitching']
    for kind in kinds:
        file = f"~/Downloads/Data/{kind}/{year}.csv"
        df = pd.read_csv(file)
        df.insert(2, "Year", year)

        if kind == "Batting":
            batter_dfs.append(df)
        else:
            pitcher_dfs.append(df)

    year -= 1

# These create one dataframe each for all batting and pitching data
batters = pd.concat(batter_dfs, axis=0, ignore_index=0)
pitchers = pd.concat(pitcher_dfs, axis=0, ignore_index=0)


for field in ['BB%', 'K%']:
    batters[field] = list(
        map(percentage_to_decimal, batters[field].values))

for field in ['LOB%', 'GB%', 'HR/FB']:
    pitchers[field] = list(
        map(percentage_to_decimal, pitchers[field].values))

for field in ['RBI', 'SB', 'wRC+']:
    batters[field] = batters[field].astype(pd.Int64Dtype())


# This extracts player names and ids from all data, to later be put into its own table.
batter_player_info = batters[['Name', 'playerid']]
pitcher_player_info = pitchers[['Name', 'playerid']]
players = [batter_player_info, pitcher_player_info]
players = pd.concat(players, axis=0, ignore_index=0)
players = players.drop_duplicates()


def war_per_600(row):
    if row['PA'] > 0:
        return round((row['WAR'] / row['PA'] * 600), 1)
    else:
        return np.nan


batters['WAR/600'] = batters.apply(war_per_600, axis=1)


def war_per_200(row):
    ip = row['IP']
    if ip > 0:
        thirds = 0
        if "." in str(ip):
            thirds = int(str(ip).split(".")[1])
        else:
            thirds = 0
        ip = ip + thirds / 3
        return round((row['WAR'] / ip * 200), 1)
    else:
        return 0


pitchers['WAR/200'] = pitchers.apply(war_per_200, axis=1)

# pitchers.to_csv("~/Downloads/Pitchers.csv", index=False)
# batters.to_csv("~/Downloads/Batters.csv", index=False)
# players.to_csv("~/Downloads/Player_info.csv", index=False)
