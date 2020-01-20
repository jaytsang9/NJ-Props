import sqlite3, requests
from time import sleep
from bs4 import BeautifulSoup

def scrape_homes():
    base = "https://newjersey.craigslist.org/d/apts-housing-for-rent"
    query = "/search/apa?s=1320"
    count = 0
    while count < 2:
        res = requests.get(f"{base}{query}")
        soup = BeautifulSoup(res.text, "html.parser")
        homes = soup.find_all("p", class_="result-info")
        all_homes = []
        for home in homes:
            home_data = (get_price(home), get_loc(home), get_size(home), get_date(home))
            all_homes.append(home_data)
            sleep(7)
        query = soup.find("a", class_="next")["href"]
        count += 1
    save_loc(all_homes)

def save_loc(all_homes):
    conn = sqlite3.connect('homes.db')
    c = conn.cursor()
    # c.execute('''CREATE TABLE homes 
    #         (id INTEGER PRIMARY KEY, price INTEGER, location TEXT, size TEXT, date TEXT)''')
    c.executemany("INSERT INTO homes (price, location, size, date) VALUES (?,?,?,?)", all_homes)
    conn.commit()
    conn.close()

def get_price(home):
    if home.select(".result-price") is not None and len(home.select(".result-price")) > 0:
        return int(home.select(".result-price")[0].get_text()[1:])
    return None

def get_loc(home):
    if home.select(".result-hood") is not None and len(home.select(".result-hood")) > 0:
        return home.select(".result-hood")[0].get_text()
    return None

def get_size(home):
    size = home.find("span", class_="housing")
    if home.find("span", class_="housing") is not None and len(home.find("span", class_="housing")) > 0:
        return home.find("span", class_="housing").get_text()
    return None

def get_date(home):
    if home.select(".result-date") is not None and len(home.select(".result-date")) > 0:
        return home.select(".result-date")[0].get_text()
    return None

scrape_homes()