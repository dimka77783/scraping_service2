
import codecs
import os, sys

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

import django

django.setup()

from scraping.parsers import *

from scraping.models import Vacancy, City, Language



parsers = (
    (work_hh, 'https://stary-oskol.hh.ru/search/vacancy?search_field=name&search'
              '_field=company_name&search_field=description&enable_snippets=false&text=python'),
    (work_habr, 'https://career.habr.com/vacancies?q=python&l=1&type=all')
)
city = City.objects.filter(slug='belgorod')
jobs, errors = [], []

for func, url in parsers:
    j, e = func(url)
    jobs += j
    errors += e
h = codecs.open('../work2.txt', 'w', 'utf-8')
h.write(str(jobs))
h.close()
