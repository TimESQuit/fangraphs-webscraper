### Fangraphs-webscraping-to-database

This code scrapes [Fangraphs'](https://www.fangraphs.com/) batting and pitching data for each season using **Selenium**, transforms and aggregates it using **Pandas**, and imports it into a **Postgresql** database.

###

This code's order of operations is:
* download-data.py
* data_wrangling.py
* data_wrangling_part2.py
* SQL/tables_creation.sql
* SQL/add_fks.sql

data_wrangling.py & data_wrangling_part2.py use helper_functions.py
