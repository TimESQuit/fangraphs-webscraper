/* Run these queries to create tables and import data */

CREATE TABLE player_info (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    Name VARCHAR,
    Fplayerid INTEGER,
    first_year INTEGER,
    last_year INTEGER
);


COPY player_info(Name, Fplayerid, first_year, last_year)
FROM '/home/tim/Documents/baseball-data/Player_info.csv'
DELIMITER ','
CSV HEADER;


CREATE TABLE batters (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    Name VARCHAR,
    Team VARCHAR,
    Year INTEGER,
    G INTEGER,
    PA INTEGER,
    HR INTEGER,
    R INTEGER,
    RBI INTEGER,
    SB INTEGER,
    bb_rate REAL,
    k_rate REAL,
    ISO REAL,
    BABIP REAL,
    AVG REAL,
    OBP REAL,
    SLG REAL,
    wOBA REAL,
    wrc_plus INTEGER,
    EV REAL,
    BsR REAL,
    Off REAL,
    Def REAL,
    WAR REAL,
    Fplayerid INTEGER,
    war_per_600 REAL
);


COPY batters(Name,Team,Year,G,PA,HR,R,RBI,SB,BB_rate,k_rate,ISO,BABIP,AVG,OBP,SLG,wOBA,wrc_plus,EV,BsR,Off,Def,WAR,Fplayerid,war_per_600)
FROM '/home/tim/Documents/baseball-data/Batters.csv'
DELIMITER ','
CSV HEADER;

CREATE TABLE pitchers (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR,
    team VARCHAR,
    year INTEGER,
    w INTEGER,
    L INTEGER,
    SV INTEGER,
    G INTEGER,
    GS INTEGER,
    IP REAL,
    K_per_9 REAL,
    BB_per_9 REAL,
    HR_per_9 REAL,
    BABIP REAL,
    LOB_rate REAL,
    GB_rate REAL,
    HR_per_FB REAL,
    EV REAL,
    ERA REAL,
    FIP REAL,
    xFIP REAL,
    WAR REAL,
    Fplayerid INTEGER,
    war_per_200 REAL
);

COPY pitchers(Name, Team, Year, W, L, SV, G, GS, IP, K_per_9, BB_per_9, HR_per_9, BABIP, LOB_rate, GB_rate, HR_per_FB, EV, ERA, FIP, xFIP, WAR, Fplayerid, war_per_200)
FROM '/home/tim/Documents/baseball-data/Pitchers.csv'
DELIMITER ','
CSV HEADER;


CREATE TABLE career_stats (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    Fplayerid INTEGER,
    default_batting INTEGER,
    bat_career REAL,
    bat_peak REAL,
    bat_avg REAL,
    career_pas INTEGER,
    peak_pas INTEGER,
    bat_rate_career REAL,
    bat_rate_peak REAL,
    bat_rate_avg REAL,
    pit_career REAL,
    pit_peak REAL,
    pit_avg REAL,
    career_ip REAL,
    peak_ip REAL,
    pit_rate_career REAL,
    pit_rate_peak REAL,
    pit_rate_avg REAL
);


COPY career_stats(Fplayerid, default_batting, bat_career, bat_peak, bat_avg, career_pas, peak_pas, bat_rate_career, bat_rate_peak, bat_rate_avg, pit_career, pit_peak, pit_avg, career_ip, peak_ip, pit_rate_career, pit_rate_peak, pit_rate_avg)
FROM '/home/tim/Documents/baseball-data/Career_stats.csv'
DELIMITER ','
CSV HEADER;
