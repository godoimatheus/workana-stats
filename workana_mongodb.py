import requests
from bs4 import BeautifulSoup
import pymongo
import re
import json
from datetime import datetime, timedelta
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import random

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                         "(KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}

# conectar mongo
client = MongoClient('localhost', 27017)
db = client['workana']
collection = db['vagas']

# indice para aceitar somente titulos e datas únicos
db['vagas'].create_index([('titulo', pymongo.ASCENDING), ('data_vaga', pymongo.ASCENDING)], unique=True)

# navegar somente até a data da última pesquisas
filtro = {}
sort = list({
                'consulta': -1
            }.items())

result = client['workana']['vagas'].find_one(
    filter=filtro,
    sort=sort
)

# skills unicas no bd
nomes_unicos = collection.distinct('skills')
forma_de_pag = ['', 'fixed', 'hourly']
personalizar = int(input('Personalizar consulta:'
                         '\n1 - SIM'
                         '\n2 - NÃO'
                         '\nOpção: '))
agreement = ''
nomes_unicos2 = []
if personalizar == 1:
    search = str(input('Nome da vaga: ')).strip()
    fmt_search = search.replace(' ', '+')
    payment = int(input('Escolha a forma de pagamento:'
                        '\n0 - Todas as formas'
                        '\n1 - Pagamento fixo'
                        '\n2 - Pagamento por hora'
                        '\nSua opção: '))

    if payment == 0:
        agreement = forma_de_pag[0]
    elif payment == 1:
        agreement = forma_de_pag[1]
    elif payment == 2:
        agreement = forma_de_pag[2]
    else:
        print('Opção inválida')
    # query = fmt_search
    nomes_unicos2.append(search)
elif personalizar == 2:
    agreement = forma_de_pag[0]
    nomes_unicos2 = nomes_unicos.copy()
    random.shuffle(nomes_unicos2)

# pesquisa por skills
cont = 0
novas_vagas = 0
for nomes in nomes_unicos2:
    cont += 1
    for i in range(1, 51):
        if nomes == "Sem skills":
            nomes = ''
        if nomes == 'C#':
            nomes = 'c-1'
        if nomes == 'C++':
            nomes = 'c-2'
        print(f'Página {i} - {nomes} - {cont}/{len(nomes_unicos2)}')
        # skills url
        url_pag = f'https://www.workana.com/en/jobs?agreement={agreement}&language=xx&query={nomes}&page={i}'
        site = requests.get(url_pag, headers=headers)
        soup = BeautifulSoup(site.content, 'html.parser')
        jobs = soup.find_all('div', class_='project-item')
        if len(jobs) == 0:
            print('Sem resultados encontrados')
            break
        date = ''
        for job in jobs:
            title = job.find('span').get('title').replace('"', "'")
            print(title)
            value_text = job.find(class_='values').get_text().replace(',', '')
            values = re.findall(r'\d+(?:\.\d+)?', value_text)
            print(value_text)
            if 'hour' in value_text:
                payment_method = 'Hourly'
            else:
                payment_method = 'Fixed'
            if len(values) == 0:
                val_min = 0
                val_max = 0
            else:
                val_min = values[0]
                if len(values) > 1:
                    val_max = values[1]
                else:
                    val_max = values[0]
            tag_date = job.find(class_='date').get('title')
            date = datetime.strptime(tag_date, "%B %d, %Y %H:%M")
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
            utc_time = datetime.utcnow()
            try:
                db['vagas'].insert_one(
                    {
                        'titulo': title,
                        'valor_min': int(val_min),
                        'valor_max': int(val_max),
                        'forma_pag': payment_method,
                        'data_vaga': date,
                        'skills': skills_list,
                        'pais': country,
                        'consulta': utc_time
                    }
                )
                novas_vagas += 1
            except PyMongoError as erro:
                print(erro)
            print()
        if date < result['consulta'] - timedelta(days=2):
            break
print(f'Novas vagas: {novas_vagas}')
