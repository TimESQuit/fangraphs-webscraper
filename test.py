from urllib.request import urlopen
import time
import os
import shutil

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

chrome_options = Options()
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--user-data-dir=/home/tim/snap/chromium/common/chromium/Profile 1')


driver_path = "/home/tim/Code/WebScraping/chromedriver"

driver = Chrome(driver_path, options=chrome_options)

# test_url = "https://www.fangraphs.com/players/mike-trout/10155/stats?position=OF"
# test_page = urlopen(test_url)
# test_html = test_page.read().decode("utf-8")
# soup = BeautifulSoup(test_html, "html.parser")

driver.get('https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=8&season=2020&month=0&season1=2020&ind=0')


data = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.LINK_TEXT, 'Export Data'))
)

print(data.get_attribute('text'))


data.send_keys('\n')

source = "/home/tim/Downloads/FanGraphs Leaderboard.csv"
dest = "/home/tim/Downloads/Data/Batting/2020.csv"

time.sleep(1)

if os.path.exists(source):
    shutil.move(source, dest)

time.sleep(5)

driver.quit()
