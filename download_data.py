import os
import shutil
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument(
    "--user-data-dir=/home/tim/snap/chromium/common/chromium/Profile 1"
)

# Download chromedriver, move it to a suitable location, and record the path here.
driver_path = "/home/tim/Code/WebScraping/chromedriver"

driver = Chrome(driver_path, options=chrome_options)

# The most recent year of available stats; I chose to go in reverse chronological order.
year = 2020

# This will track the total number of errors encountered while trying to dowload the files.
errors = 0

# Fangraphs' earliest year of data is 1871, the first year of Major League Baseball.
while year > 1870:
    """
    This loop cycles through each year and retrieves fangraphs' "dashboard" csv
    showing standard stats along with a few non-standard, including WAR.
    This downloads a csv for each year, and then renames & relocates the file.
    """

    kinds = ["bat", "pit"]

    # This retrieves one year's data for batting and then pitching.
    for kind in kinds:

        driver.get(
            f"https://www.fangraphs.com/leaders.aspx?pos=all&stats={kind}&lg=all&qual=0&type=8&season={year}&month=0&season1={year}&ind=0"
        )

        # This is for cleaner message formatting and file management.
        if kind == "bat":
            kind = "Batting"
        else:
            kind = "Pitching"

        # This waits for the "Export Data" link/button to load in.
        try:
            data = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Export Data"))
            )

        except TimeoutException:
            print(f"The {year} {kind} page took too long to load.")
            errors += 1
            continue

        # .click() caused an error, so this was used instead.
        data.send_keys("\n")

        # This is the default downloads location.
        source = "/home/tim/Downloads/FanGraphs Leaderboard.csv"

        # "Batting" & "Pitching" folders were created previously.
        dest = f"/home/tim/Downloads/Data/{kind}/{year}.csv"

        # To account for the time required to download the file before renaming & moving it,
        # this loop waits up to 10 seconds for the file to appear before renaming & moving it.
        time_counter = 0
        while time_counter < 10:
            if os.path.exists(source):
                shutil.move(source, dest)
                break
            else:
                time.sleep(1)
                time_counter += 1

        if time_counter >= 10:
            print(
                f"Something went wrong with the download or file renaming for {year} {kind}"
            )
            errors += 1

        else:
            print(f"All done for {year} {kind}!")

    # After visiting both batting and pitching pages for a given year, go to the next year.
    year -= 1

print(
    f"All requested years' data download attempts are finished. There were {errors} errors."
)

driver.quit()
