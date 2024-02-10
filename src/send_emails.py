import os, sys
import django
import datetime
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model


proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"


django.setup()

from scraping.models import Vacancy, Error, Url
from scraping_service.settings import EMAIL_HOST_USER
ADMIN_USER = EMAIL_HOST_USER
today = datetime.date.today()
subject =f'Рассылка вакансий за {today}'
text_content = f'Рассылка вакансий за {today}'
from_email = EMAIL_HOST_USER
empty = '<h2> к сожалению на сегодня по Вашим предпочтениям данных нет</h2>'
today = datetime.date.today()

User = get_user_model()
qs = User.objects.filter(send_email=True).values('city', 'language', 'email')
users_dict = {}
for i in qs:
    users_dict.setdefault((i['city'], i['language']), [])
    users_dict[(i['city'], i['language'])].append(i['email'])
if users_dict:
    params = {'city_id__in': [], 'language_id__in': []}
    for pair in users_dict.keys():
        params['city_id__in'].append(pair[0])
        params['language_id__in'].append(pair[1])
    qs = Vacancy.objects.filter(**params, timestamp=today).values()
    vacancies = {}
    #for i in qs:
    #    vacancies.setdefault((i['city_id'], i['language_id']), [])
    #    vacancies[(i['city_id'], i['language_id'])].append(i)
    #for keys, emails in users_dict.items():
    #    rows = vacancies.get(keys, [])
    #    html = ''
    #    for row in rows:
    #        html += f'<h5><a href="{row["url"] }">{ row["title"] }</a></h5>'
    #       html += f'<p>{row["description"]}</p>'
    #        html += f'<p>{row["company"]}</p><br><hr>'
    #    _html = html if html else empty
    #    for email in emails:
    #        to = email
    #        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    #        msg.attach_alternative(_html, "text/html")
    #        msg.send()
qs = Error.objects.filter(timestamp=today)
subject = ''
text_content = ''
to = ADMIN_USER
_html = ''
if qs.exists():
    error = qs.first()
    data = error.data.get('errors', [])
    for i in data:
        _html += f'<p><a href= "{ i["url"] }">Error: { i["title"] }</a></p><br>'
    subject = f"Ошибки скрапинга{today}"
    text_content = "Ошибки скрапинга"
    data = error.data.get('user_data')
    if data:
        _html += '<hr>'
        _html += '<h2>Пожелания пользователей</h2>'
        for i in data:
            _html += f'<p>Город: {i["city"]}, Специальность:{i["language"]}, Имейл:{i["email"]}</p><br>'
        subject = f"Пожелания пользователей{today}"
        text_content = "Пожелания пользователей"



qs = Url.objects.all().values('city', 'language')
urls_dict = {(i['city'], i['language']): True for i in qs}
urls_errors = ''
for keys in urls_dict.keys():
    if keys in urls_dict:
        if keys[0] and keys[1]:
            urls_errors += f'<p>Для города:{keys[0]} и ЯП: {keys[1]} отсутсвуют урлы</p><br/>'
if urls_errors:
    subject += ' Отсутсвующие урлы'
    _html += urls_errors

if subject:
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(_html, "text/html")
    msg.send()
