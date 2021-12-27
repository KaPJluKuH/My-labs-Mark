import requests
from bs4 import BeautifulSoup as BS
import base64
import requests
import json


def save(comp):
    with open('games_parse.txt', 'a') as file:
        file.write(f"{comp['title']} -> Date:{comp['date']} -> Link:{comp['link']}\n")


def parseImgs():
    allComps = []
    i = 1
    while True:
        URL = f'https://stopgame.ru/review/new/izumitelno/p{i}'
        i += 1
        HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
        }
        response = requests.get(URL, headers=HEADERS)

        # проверка на статус ответа ссервера
        if response.status_code != 200:
            break

        soup = BS(response.content, 'html.parser')
        games = soup.findAll('div', class_='item article-summary')
        # ограничение на 1 запись со страницы for test
        # games = soup.findAll('div', class_='item article-summary')[:1]

        if len(games) < 1:
            break

        comps = []

        for game in games:
            comps.append({
                'title': game.find('div', class_='caption caption-bold').get_text(strip=True),
                'date': game.find('span', class_='info-item timestamp').get_text(strip=True),
                'link': game.find('a', href=True).get('href'),
                'src': game.find('img')['src']
            })

        for comp in comps:
            print(f"page{i - 1} {comp['title']} -> Date:{comp['date']} -> link:{comp['link']}")
            comp.update({'base64': ''})

        allComps += comps

    return allComps


requests.post("http://127.0.0.1:8080/create_table", json={"columns": [["title", "TEXT", ["NOT NULL", ]],
                                                                            ["date", "TEXT", ["NOT NULL", ]],
                                                                            ["link", "TEXT",
                                                                             ["PRIMARY KEY", "NOT NULL"]],
                                                                            ["src", "TEXT", ["NOT NULL", ]],
                                                                            ["base64", "BLOB", ["NOT NULL", ]]],
                                                                "table_name": "article_data_images"})

requests.post("http://127.0.0.1:8080/truncate", json={"table_name": "article_data_images"})

data = parseImgs()
print(f"{len(data)} read")

values = [(d['title'], d['date'], d['link'], d['src'], d['base64']) for d in data]
columns = ['title', 'date', 'link', 'src', 'base64']
# Привод данных к заполнению
for v in values:
    requests.post("http://127.0.0.1:8080/create", json={"columns": columns, "values": v},
                  params={"download":"true"})
