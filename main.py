import requests
from bs4 import BeautifulSoup as bs
import csv
import re

# создадим заголовки для эмуляции работы из браузера
headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
# базовый адрес
base_url = 'https://filmshd.club/page/1/'


def pars(base_url, headers):
    films = []
    urls = []
    urls.append(base_url)
    text_search = r"\S+\/page\/\d+"
    find_count = r"\d+"
    # создадим сессию
    session = requests.Session()
    # эмуляция открытия страницы в браузере
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        # получим весь контент
        soup = bs(request.content, 'lxml')
        try:
            # найти способ взять номер ласт страницы (не самый красивый способ, но рабочий)
            pages = str(soup.find('div', attrs = {'class':'navigation'}))
            last_page = re.findall(text_search, pages)[-1]
            count = int(re.findall(find_count, last_page)[0])
            for i in range(1, count + 1):
                url = f'https://filmshd.club/page/{i}/'
                if url not in urls:
                    urls.append(url)
        except:
            pass
    for url in urls:
        request = session.get(url, headers=headers)
        soup = bs(request.content, 'lxml')
        divs = soup.find_all('div', attrs={'class': 'th-item'})
        # отберем необходимое
        for div in divs:
            try:
                info = div.find('div', attrs={'class': 'th-tip'}).text
                href = div.find('a', attrs={'class': 'th-in js-tip'})['href']
                films.append({
                    'info': info,
                    'href': href
                })
            except:
                pass
        print(len(films))
    else:
        print('ERROR or Done. Status_code = ' + str(request.status_code))
    return films


def file_writer(films):
    with open('parsed_films.csv', 'w') as file:
        pen = csv.writer(file)
        pen.writerow(('Название фильма и краткое описание', 'URL'))
        for film in films:
            try:
                pen.writerow((film['info'], film['href']))
            except:
                pass


films = pars(base_url, headers)
file_writer(films)
