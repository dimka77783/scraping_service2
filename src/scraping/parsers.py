import requests
import codecs
from bs4 import BeautifulSoup as BS
from random import randint

__all__ = ('work_hh', 'work_habr')

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


def work_hh(url,city=None, language=None):
    jobs = []
    errors = []
    domain = 'https://hh.ru'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 4)])
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', id='a11y-main-content')
            if main_div:
                div_list = main_div.find_all('div', attrs={'class': 'vacancy-serp-item__layout'})
                for div in div_list:
                    title = div.find('h3')
                    href = title.a['href']
                    content ='No price'
                    contents = div.find_all('span', class_='bloko-header-section-2')
                    for content in contents:
                        content = content.text
                    if content:
                        content = content
                    company = 'No name'
                    companies = div.find_all('a', class_='bloko-link bloko-link_kind-tertiary')
                    for company in companies:
                        company = company.text
                    if company:
                        company = company


                    jobs.append({'title': title.text, 'url': href, 'description': content, 'company': company, 'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': 'Div does not exists'})

        else:
            errors.append({'url': url, 'title': 'Page do not response'})
    return jobs, errors


def work_habr(url, city=None, language=None):
    jobs = []
    errors = []
    domain = 'https://career.habr.com'
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


                    jobs.append({'title': title, 'url': domain + href, 'description': content2, 'company': company, 'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': 'Table does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})
    return jobs, errors




if __name__ == '__main__':
    url = 'https://career.habr.com/vacancies?q=python&l=1&type=all'
    jobs, errors = work_habr(url)
    h = codecs.open('../work.txt', 'w', 'utf-8')
    h.write(str(jobs))
    h.close()
