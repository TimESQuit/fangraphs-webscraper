import time

import pandas as pd

from helper_functions import ip_fraction_handler

# Import the 3 csv files created in data_wrangling
batters = pd.read_csv("~/Documents/baseball-data/Batters.csv")
pitchers = pd.read_csv("~/Documents/baseball-data/Pitchers.csv")
players = pd.read_csv("~/Documents/baseball-data/Player_info.csv")


# This file's main function
def aggregate_career_stats():
    """
    This function creates 15 columns and inputs data that is aggregated from the three csv files,
    using other calculation functions. It returns a pandas DataFrame. 'playerid' here refers to Fangraphs' playerid;
    "career_pas" and "career_ip" are exactly as expected, with career_ip in real-number format (see the
    ip helper function for more detail); all other columns represent the appropriate total WAR or WAR rate, with
    peak WAR including the top 7 seasons. 
    """
    cols = [
        "playerid",
        "bat_career", "bat_peak", "bat_avg",
        "career_pas", "bat_rate_career", "bat_rate_peak", "bat_rate_avg",
        "pit_career", "pit_peak", "pit_avg",
        "career_ip", "pit_rate_career", "pit_rate_peak", "pit_rate_avg"
    ]
    # Creates an empty DataFrame with column names.
    df = pd.DataFrame(columns=cols)
    ids = players['playerid']

    tick = time.perf_counter()  # Setup timing the next operations

    # This loops over each playerid (unique values), calculates 14 different stats, and fills them into the DataFrame.
    for i, id in enumerate(ids):
        bat_regular = bat_reg_cruncher(id)
        bat_rates = bat_rate_cruncher(id)
        pit_regular = pit_reg_cruncher(id)
        pit_rates = pit_rate_cruncher(id)
        df.loc[i] = [
            id,
            bat_regular[0], bat_regular[1], bat_regular[2],
            bat_rates[0], bat_rates[1], bat_rates[2], bat_rates[3],
            pit_regular[0], pit_regular[1], pit_regular[2],
            pit_rates[0], pit_rates[1], pit_rates[2], pit_rates[3]
        ]

    df = df.astype({'playerid': 'int64', 'career_pas': 'int64'})

    # Stop timing after the operations have finished.
    tock = time.perf_counter()
    print(
        f'Aggregating all careers stats into a DataFrame took {tock - tick:04f} seconds.')

    return df


def bat_reg_cruncher(id):
    # This function returns a batter's career WAR, 7-year-peak WAR and the average of the two.
    player = batters[batters['playerid'] == id]
    career = round(player.sum()['WAR'], 1)
    peak = round(player.nlargest(7, 'WAR').sum()['WAR'], 1)
    avg = round(((career + peak) / 2), 1)
    return [career, peak, avg]


def bat_rate_cruncher(id):
    # This function calculates a batter's career rate of WAR/600 PAs, and a batter's WAR/600
    # over the batter's 7 highest WAR seasons. It also takes the average of the two numbers.
    player = batters[batters['playerid'] == id]
    career_pas = (player.sum()['PA'])
    career_war = round(player.sum()['WAR'], 1)
    if not career_pas > 0:
        return [0, 0, 0, 0]
    else:
        career_rate = round((career_war / career_pas * 600), 2)
        peak_pas = player.nlargest(7, ['WAR', 'WAR/600']).sum()['PA']
        peak_war = player.nlargest(7, ['WAR', 'WAR/600']).sum()['WAR']
        peak_rate = round((peak_war / peak_pas * 600), 2)
        avg_rate = round(((career_rate + peak_rate) / 2), 2)
        return [career_pas, career_rate, peak_rate, avg_rate]


def pit_reg_cruncher(id):
    # This function returns a pitcher's career pitching WAR, 7-year-peak WAR and the average of the tw
    player = pitchers[pitchers['playerid'] == id]
    career = round(player.sum()['WAR'], 1)
    peak = round(player.nlargest(7, 'WAR').sum()['WAR'], 1)
    avg = round(((career + peak) / 2), 1)
    return [career, peak, avg]


def pit_rate_cruncher(id):
    # This function calculates a pitcher's career rate of WAR/200 PAs, and a pitcher's WAR/200
    # over the pitcher's 7 highest WAR seasons. It also takes the average of the two numbers.
    player = pitchers[pitchers['playerid'] == id]
    career_years_ip = player['IP']
    career_ip = ip_fraction_handler(career_years_ip)
    career_war = round(player.sum()['WAR'], 1)
    if not career_ip > 0:
        return [0, 0, 0, 0]
    else:
        career_rate = round((career_war / career_ip * 200), 2)
        peak_years = player.nlargest(7, ['WAR', 'WAR/200'])
        peak_years_ip = peak_years['IP']
        peak_ip = ip_fraction_handler(peak_years_ip)
        peak_war = player.nlargest(
            7, ['WAR', 'WAR/200']).sum()['WAR']
        peak_rate = round((peak_war / peak_ip * 200), 2)
        avg_rate = round(((career_rate + peak_rate) / 2), 2)
        return [career_ip, career_rate, peak_rate, avg_rate]


# Runs the main function and converts the returned DataFrame into a CSV.
aggregate_career_stats().to_csv(
    "~/Documents/baseball-data/Career_stats.csv", index=False)
