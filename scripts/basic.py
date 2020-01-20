import sqlite3
import requests
from time import sleep
from bs4 import BeautifulSoup

response = requests.get("https://newjersey.craigslist.org/d/apts-housing-for-rent/search/apa")
soup = BeautifulSoup(response.text, "html.parser")
homes = soup.find_all("p", class_="result-info")
hoods = []
for home in homes[:7]:
    hoods.append(home.select(".result-date")[0].get_text())
    sleep(10)

print(hoods)