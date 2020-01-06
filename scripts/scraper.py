import sqlite3, requests, time
from bs4 import BeautifulSoup

def scrape_homes(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    homes = soup.find_all(".result-info")
    all_homes = []
    for home in homes:
        home_data = (get_price(home), get_loc(home), get_size(home))
        all_homes.append(home_data)
        time.sleep(10)
    save_loc(all_homes)

def save_loc(all_homes):
    conn = sqlite3.connect('homes.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE homes 
            (location TEXT, price INTEGER, size TEXT, date TEXT)''')
    c.executemany("INSERT INTO homes VALUES (?,?,?,?)", all_homes)
    conn.commit()
    conn.close()

def get_loc(home):
    return home.select(".result-meta")[0].select(".result-hood")[0].get_text()

def get_price(home):
    price = home.select(".result-meta")[0].select(".result-price").get_text()
    return int(price.replace("$", "").replace("Â", ""))

def get_size(home):
    return home.select(".result-meta")[0].select(".housing").get_text()

scrape_homes("https://newjersey.craigslist.org/d/apts-housing-for-rent/search/apa")