# для корректной работы надо подгузить библиотеки:
# pip install beautifulsoup4
# pip install requests
# pip install fake-useragent
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import csv
import datetime
UserAgent().chrome
page_link = 'https://hh.ru/search/vacancy?area=113&search_field=name&search_field=company_name&search_field=description&text'
response = requests.get(page_link, headers={'User-Agent': UserAgent().chrome})
html = response.content
soup = BeautifulSoup(html,'html.parser')
info1 = soup.find(lambda tag: tag.name == 'h1' and tag.get('class') == ['bloko-header-section-3']).text
vacancy = ''
numbers = ['0','1','2','3','4','5','6','7','8','9']
for i in info1:
    if i in numbers:
        vacancy += i
vacancy = int(vacancy)
## переход на поиск резюме и кол-ва кандидатов
page_link = 'https://hh.ru/search/resume?text=&logic=normal&pos=full_text&exp_period=all_time&exp_company_size=any&exp_industry=any&area=113&relocation=living_or_relocation&salary_from=&salary_to=&currency_code=RUR&age_from=&age_to=&gender=unknown&order_by=relevance&search_period=0&items_on_page=50&no_magic=false'
response = requests.get(page_link, headers={'User-Agent': UserAgent().chrome})
html = response.content
soup = BeautifulSoup(html,'html.parser')
info2 = soup.find(lambda tag: tag.name == 'div' and tag.get('class') == ['bloko-header-section-3']).text
res = info2.split()
res.remove('Найдено')
res.remove('резюме')
if 'соискателей' in res:
    res.remove('соискателей')
else:
    res.remove('соискателя')
res.remove('у')
resume = ''
candidate = ''
a = len(res)//2
for i in range(a):
    resume += res[i]
for i in range(a,len(res)):
    candidate += res[i]
resume = int(resume)
candidate= int(candidate)
## переход на поиск кол-ва компаний
page_link = 'https://hh.ru/employers_list?query=&areaId=113'
response = requests.get(page_link, headers={'User-Agent': UserAgent().chrome})
html = response.content
soup = BeautifulSoup(html,'html.parser')
info3 = soup.find(lambda tag: tag.name == 'div' and tag.get('class') == ['totals--rE1moq2jhLukW5QVcI6L']).text
company = ''
for i in info3:
    if i in numbers:
        company += i
company = int(company)
## находим дату
today = datetime.datetime.today()
date = today.strftime('%d.%m.%Y')
## подводим итог всего найденного
'''
headings = ['Дата', 'Вакансии', 'Резюме', 'Кандидаты', 'Компании']
info = [date, vacancy, resume, candidate, company]
itog = dict(zip(headings,info))
print(itog)
'''
## записываем все в файл
with open('hhparcer', 'a', encoding='utf-8-sig', newline='') as fil:
                writer = csv.writer(fil, delimiter = ";")
                writer.writerow((
                    date,
                    vacancy,
                    resume,
                    candidate,
                    company
                ))
