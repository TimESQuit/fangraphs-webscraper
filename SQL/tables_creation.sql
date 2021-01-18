/* Run these queries to create tables and import data */

CREATE TABLE player_info (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    Name VARCHAR,
    Fplayerid INTEGER
);


COPY player_info(Name, Fplayerid)
FROM '/home/tim/Downloads/Player_info.csv'
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
    Fplayerid INTEGER
);


COPY batters(Name,Team,Year,G,PA,HR,R,RBI,SB,BB_rate,k_rate,ISO,BABIP,AVG,OBP,SLG,wOBA,wrc_plus,EV,BsR,Off,Def,WAR,Fplayerid)
FROM '/home/tim/Downloads/Batters.csv'
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
    Fplayerid INTEGER
);

COPY pitchers(Name, Team, Year, W, L, SV, G, GS, IP, K_per_9, BB_per_9, HR_per_9, BABIP, LOB_rate, GB_rate, HR_per_FB, EV, ERA, FIP, xFIP, WAR, Fplayerid)
FROM '/home/tim/Downloads/Pitchers.csv'
DELIMITER ','
CSV HEADER;


CREATE TABLE career_stats (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    Fplayerid INTEGER,
    bat_career REAL,
    bat_peak REAL,
    bat_avg REAL,
    bat_rate_career REAL,
    bat_rate_peak REAL,
    bat_rate_avg REAL,
    pit_career REAL,
    pit_peak REAL,
    pit_avg REAL,
    pit_rate_career REAL,
    pit_rate_peak REAL,
    pit_rate_avg REAL
)

