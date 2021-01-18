/* Run these after tables_creation */

ALTER TABLE batters
ADD player_id INT;

UPDATE batters
SET player_id = player_info.id
FROM player_info
WHERE batters.fplayerid = player_info.fplayerid;

ALTER TABLE batters
ADD CONSTRAINT fk_batters_player_id
    FOREIGN KEY(player_id)
        REFERENCES player_info(id)
        ON DELETE RESTRICT;

ALTER TABLE batters
DROP COLUMN fplayerid,
DROP COLUMN name;



ALTER TABLE pitchers
ADD player_id INT;

UPDATE pitchers
SET player_id = player_info.id
FROM player_info
WHERE pitchers.fplayerid = player_info.fplayerid;

ALTER TABLE pitchers
ADD CONSTRAINT fk_pitchers_player_id
    FOREIGN KEY(player_id)
        REFERENCES player_info(id)
        ON DELETE RESTRICT;

ALTER TABLE pitchers
DROP COLUMN fplayerid,
DROP COLUMN name;




ALTER TABLE career_stats
ADD player_id INT;

UPDATE career_stats
SET player_id = player_info.id
FROM player_info
WHERE career_stats.fplayerid = player_info.fplayerid;

ALTER TABLE career_stats
ADD CONSTRAINT fk_career_stats_player_id
    FOREIGN KEY(player_id)
        REFERENCES player_info(id)
        ON DELETE RESTRICT;

ALTER TABLE career_stats
DROP COLUMN fplayerid;
