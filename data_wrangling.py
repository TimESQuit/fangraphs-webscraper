import pandas as pd
import numpy as np

from helper_functions import ip_fraction_handler, percentage_to_decimal

batter_dfs = []
pitcher_dfs = []

year = 2020

# This combines all years' data into one list of dfs for each Batting and Pitching.
while year > 1870:
    kinds = ["Batting", "Pitching"]
    for kind in kinds:
        file = f"~/Documents/baseball-data/Data/{kind}/{year}.csv"
        df = pd.read_csv(file)
        df.insert(2, "Year", year)

        if kind == "Batting":
            batter_dfs.append(df)
        else:
            pitcher_dfs.append(df)

    year -= 1

# Create one dataframe each for all batting and pitching data
batters = pd.concat(batter_dfs, axis=0, ignore_index=0)
pitchers = pd.concat(pitcher_dfs, axis=0, ignore_index=0)


for field in ["BB%", "K%"]:
    batters[field] = list(map(percentage_to_decimal, batters[field].values))

for field in ["LOB%", "GB%", "HR/FB"]:
    pitchers[field] = list(map(percentage_to_decimal, pitchers[field].values))

for field in ["RBI", "SB", "wRC+"]:
    batters[field] = batters[field].astype(pd.Int64Dtype())


# This extracts player names and ids from all data, to later be put into its own table.
batter_player_info = batters[["Name", "playerid"]]
pitcher_player_info = pitchers[["Name", "playerid"]]
players = [batter_player_info, pitcher_player_info]
players = pd.concat(players, axis=0, ignore_index=0)
players = players.drop_duplicates()


def war_per_600(row):
    if row["PA"] > 0:
        return round((row["WAR"] / row["PA"] * 600), 1)
    else:
        return np.nan


batters["WAR/600"] = batters.apply(war_per_600, axis=1)


def war_per_200(row):
    ip = row["IP"]
    if ip > 0:
        thirds = 0
        if "." in str(ip):
            thirds = int(str(ip).split(".")[1])
        else:
            thirds = 0
        ip = ip + thirds / 3
        return round((row["WAR"] / ip * 200), 1)
    else:
        return 0


pitchers["WAR/200"] = pitchers.apply(war_per_200, axis=1)


def get_player_info():
    # Combines player info into new df
    cols = ["Name", "playerid", "first_year", "last_year"]
    df = pd.DataFrame(columns=cols)
    ids = players["playerid"]
    errors = 0
    for i, id in enumerate(ids):
        name = players[players["playerid"] == id]["Name"].values[0]
        years = get_year_ends(id)
        first_year = years[0]
        last_year = years[1]
        df.loc[i] = [name, id, first_year, last_year]

        errors += years[2]
    print(f"There were {errors} errors calculating years")

    df = df.astype({"playerid": "int64", "first_year": "int64", "last_year": "int64"})

    return df


def get_year_ends(id):
    # Finds First and Last year for a player
    batter = batters[batters["playerid"] == id]["Year"].values
    pitcher = pitchers[pitchers["playerid"] == id]["Year"].values
    first_year = 3000
    last_year = 0
    first_errors = 0
    last_errors = 0

    first_bat, first_pit = 3001, 3001
    last_bat, last_pit = 1, 1

    try:
        first_bat = batter.min()
    except:
        first_errors += 1

    try:
        first_pit = pitcher.min()
    except:
        first_errors += 1

    try:
        last_bat = batter.max()
    except:
        last_errors += 1

    try:
        last_pit = pitcher.max()
    except:
        last_errors += 1

    first_year = min(first_bat, first_pit)
    last_year = max(last_bat, last_pit)

    errors = int(first_errors // 2 + last_errors // 2)

    return [first_year, last_year, errors]


players = get_player_info()

pitchers.to_csv("~/Documents/baseball-data/Pitchers.csv", index=False)
batters.to_csv("~/Documents/baseball-data/Batters.csv", index=False)
players.to_csv("~/Documents/baseball-data/Player_info.csv", index=False)
