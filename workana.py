import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from datetime import datetime
import sqlite3

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                         "(KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}

search = str(input('Nome da vaga: ')).strip()
fmt_search = search.replace(' ', '+')
full_date = datetime.now()
fmt_date = full_date.strftime("%d-%m-%Y_%H-%M-%S")
dict_jobs = {'titulo': [], 'valorMin': [], 'valorMax': [], 'formaPag': [],
             'data': [], 'skill': [], 'pais': []}
# bd = sqlite3.connect(f'{search}_{fmt_date}.db')
db = sqlite3.connect('sqlite.db')
cursor = db.cursor()
cursor.execute(f"CREATE TABLE IF NOT EXISTS vagas ("
               f"titulo text UNIQUE, valor_min real, valor_max real, "
               f"forma_pag text, data text, skills text, pais text)")
payment = int(input('Escolha a forma de pagamento:'
                    '\n1 - Todas as formas'
                    '\n2 - Pagamento fixo'
                    '\n3 - Pagamento por hora'
                    '\nSua opção: '))
if payment == 1:
    agreement = f'agreement='
elif payment == 2:
    agreement = f'agreement=fixed'
elif payment == 3:
    agreement = f'agreement=hourly'
else:
    print('Opção inválida')
for i in range(1, 51):
    print(f'Página {i}')
    url_pag = f'https://www.workana.com/jobs?{agreement}&language=xx&query={fmt_search}&page={i}'
    site = requests.get(url_pag, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')
    jobs = soup.find_all('div', class_='project-item')
    if len(jobs) == 0:
        print('Sem resultados encontrados')
        break
    for job in jobs:
        title = job.find('span').get('title').replace('"', "'")
        print(title)
        value_text = job.find(class_='values').get_text().replace('.', '')
        # value_text = value_text.replace('.', '')
        values = re.findall(r'\d+(?:\.\d+)?', value_text)
        print(value_text)
        if 'hora' in value_text:
            payment_method = 'Hora'
        else:
            payment_method = 'Fixo'
        if len(values) == 0:
            val_min = value_text
            val_max = value_text  # ou valor sem ponto
        else:
            val_min = values[0]
            if len(values) > 1:
                val_max = values[1]
            else:
                val_max = values[0]
        date = job.find(class_='date').get('title')
        print(date)
        skills_list = []
        tag_label = job.find_all('label-expander')
        if len(tag_label) > 0:
            expand = tag_label[0][":to-expand"]
            skills = json.loads(expand)
            for skill in skills:
                anchor_text = skill['anchorText']
                skills_list.append(anchor_text)
            skill_text = ', '.join(skills_list)
            print(skills_list)
        else:
            skill_text = 'Sem skills'
            skills_list.append(skill_text)
        country = job.find(class_='country-name').get_text().strip()
        print(country)
        dict_jobs['titulo'].append(title)
        dict_jobs['valorMin'].append(val_min)
        dict_jobs['valorMax'].append(val_max)
        dict_jobs['formaPag'].append(payment_method)
        dict_jobs['data'].append(date)
        dict_jobs['skill'].append(skills_list)
        dict_jobs['pais'].append(country)
        print()
        cursor.execute(f'INSERT OR IGNORE INTO vagas ('
                       f'titulo, valor_min, valor_max, forma_Pag, data, skills, pais) '
                       f'VALUES('
                       f'"{title}", "{val_min}", "{val_max}", "{payment_method}", '
                       f'"{date}", "{skill_text}", "{country}")')
        db.commit()
# df = pd.DataFrame(dict_jobs)
# df.to_csv(f'{search}_{fmt_date}.csv', encoding='utf-8', sep=';', index=False)
