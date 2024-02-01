
import codecs
import os, sys
from django.db import DatabaseError

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

import django
django.setup()



from scraping.parsers import *

from scraping.models import Vacancy, City, Language, Error

parsers = (
    (work_hh, 'https://belgorod.hh.ru/search/vacancy?search_field=name&search_field=company_name&search_field=description&enable_snippets=false&area=17&text=python&L_save_area=true&customDomain=1'),
    (work_habr, 'https://career.habr.com/vacancies?q=python&l=1&type=all')
)



city = City.objects.filter(slug='belgorod').first()
language = Language.objects.filter(slug='python').first()

jobs, errors = [], []

for func, url in parsers:
    j, e = func(url)
    jobs += j
    errors += e

for job in jobs:
    v = Vacancy(**job, city=city, language=language)
    try:
        v.save()
    except DatabaseError:
        pass
if errors:
    er = Error(data=errors).save()


#h = codecs.open('../work2.txt', 'w', 'utf-8')
#h.write(str(jobs))
#h.close()
