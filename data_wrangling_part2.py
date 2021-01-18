import time

import pandas as pd

from helper_functions import ip_fraction_handler

batters = pd.read_csv("~/Documents/baseball-data/Batters.csv")
pitchers = pd.read_csv("~/Documents/baseball-data/Pitchers.csv")
players = pd.read_csv("~/Documents/baseball-data/Player_info.csv")

batters = batters.sort_values(
    ['playerid', 'WAR', 'WAR/600'], ascending=[True, False, False])
pitchers = pitchers.sort_values(
    ['playerid', 'WAR', 'WAR/200'], ascending=[True, False, False])


def aggregate_career_stats():
    cols = [
        "playerid",
        "bat_career", "bat_peak", "bat_avg", "bat_rate_career", "bat_rate_peak", "bat_rate_avg",
        "pit_career", "pit_peak", "pit_avg", "pit_rate_career", "pit_rate_peak", "pit_rate_avg"
    ]
    df = pd.DataFrame(columns=cols)
    ids = players['playerid']

    tick = time.perf_counter()

    for i, id in enumerate(ids):
        bat_regular = bat_reg_cruncher(id)
        bat_rates = bat_rate_cruncher(id)
        pit_regular = pit_reg_cruncher(id)
        pit_rates = pit_rate_cruncher(id)
        df.loc[i] = [
            id,
            bat_regular[0], bat_regular[1], bat_regular[2], bat_rates[0], bat_rates[1], bat_rates[2],
            pit_regular[0], pit_regular[1], pit_regular[2], pit_rates[0], pit_rates[1], pit_rates[2]
        ]

    tock = time.perf_counter()
    print(
        f'Aggregating all careers stats into a df took {tock - tick:04f} seconds.')

    return df


def bat_reg_cruncher(id):
    career = round(batters[batters['playerid'] == id].sum()['WAR'], 1)
    peak = round(batters[batters['playerid'] == id].nlargest(
        7, 'WAR').sum()['WAR'], 1)
    avg = round(((career + peak) / 2), 1)
    return [career, peak, avg]


def bat_rate_cruncher(id):
    career_pas = batters[batters['playerid'] == id].sum()['PA']
    career_war = round(batters[batters['playerid'] == id].sum()['WAR'], 1)
    if not career_pas > 0:
        return [0, 0, 0]
    else:
        career_rate = round((career_war / career_pas * 600), 2)
        peak_pas = batters[batters['playerid'] == id].nlargest(
            7, ['WAR', 'WAR/600']).sum()['PA']
        peak_war = batters[batters['playerid'] == id].nlargest(
            7, ['WAR', 'WAR/600']).sum()['WAR']
        peak_rate = round((peak_war / peak_pas * 600), 2)
        avg_rate = round(((career_rate + peak_rate) / 2), 2)
        return [career_rate, peak_rate, avg_rate]


def pit_reg_cruncher(id):
    career = round(pitchers[pitchers['playerid'] == id].sum()['WAR'], 1)
    peak = round(pitchers[pitchers['playerid'] == id].nlargest(
        7, 'WAR').sum()['WAR'], 1)
    avg = round(((career + peak) / 2), 1)
    return [career, peak, avg]


def pit_rate_cruncher(id):
    career_years = pitchers[pitchers['playerid'] == id]
    career_years_ip = career_years['IP']
    career_ip = ip_fraction_handler(career_years_ip)
    career_war = round(pitchers[pitchers['playerid'] == id].sum()['WAR'], 1)
    if not career_ip > 0:
        return [0, 0, 0]
    else:
        career_rate = round((career_war / career_ip * 200), 2)
        peak_years = pitchers[pitchers['playerid']
                              == id].nlargest(7, ['WAR', 'WAR/200'])
        peak_years_ip = peak_years['IP']
        peak_ip = ip_fraction_handler(peak_years_ip)
        peak_war = pitchers[pitchers['playerid'] == id].nlargest(
            7, ['WAR', 'WAR/200']).sum()['WAR']
        peak_rate = round((peak_war / peak_ip * 200), 2)
        avg_rate = round(((career_rate + peak_rate) / 2), 2)
        return [career_rate, peak_rate, avg_rate]


aggregate_career_stats().to_csv(
    "~/Documents/baseball-data/Career_stats.csv", index=False)
