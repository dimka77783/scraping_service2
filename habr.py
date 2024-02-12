import requests
import codecs
from bs4 import BeautifulSoup as BS
from random import randint


headers = [
            {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0',
           'Accept': 'application/font-woff2;q=1.0,application/font-woff;q=0.9,*/*;q=0.8'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
           'Accept': 'application/font-woff2;q=1.0,application/font-woff;q=0.9,*/*;q=0.8'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
           'Accept': 'application/font-woff2;q=1.0,application/font-woff;q=0.9,*/*;q=0.8'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
           'Accept': 'application/font-woff2;q=1.0,application/font-woff;q=0.9,*/*;q=0.8'},
            {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
           'Accept': 'application/font-woff2;q=1.0,application/font-woff;q=0.9,*/*;q=0.8'}
           ]

jobs = []
errors = []
domain = 'https://career.habr.com'
url = 'https://career.habr.com/vacancies?q=python&l=1&type=all'
if url:
    resp = requests.get(url, headers=headers[randint(0, 4)])
    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        table = soup.find('div', attrs={'class': 'section-group section-group--gap-medium'})
        if table:
            div_list = table.find_all('div', attrs={'class': 'vacancy-card'})
            for div in div_list:
                titles = div.find_all('div', attrs={'class': 'vacancy-card__title'})
                for title in titles:
                    title = title.text
                href = div.a['href']
                content2 = 'No price'
                contents = div.find_all('div', attrs={'class': 'basic-salary'})
                for content2 in contents:
                    content2 = content2.text
                if content2:
                    content2 = content2
                companys = div.find_all('div', attrs={'class': 'vacancy-card__company-title'})
                for company in companys:
                    company = company.text

                jobs.append({'title': title, 'url': domain + href, 'description': content2, 'company': company})
        else:
            errors.append({'url': url, 'title': 'Table does not exists'})
    else:
        errors.append({'url': url, 'title': 'Page do not response'})


h = codecs.open('../work3.txt', 'w', 'utf-8')
h.write(str(jobs))
h.close()
