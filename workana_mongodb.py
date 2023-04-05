import re
import pymongo
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import PyMongoError

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                         "(KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}

client = MongoClient('localhost', 27017)
db = client['workana']
collection = db['vagas']
db['vagas'].create_index([("titulo", pymongo.ASCENDING)], unique=True)

nomes_unicos = collection.distinct('skills')
print(nomes_unicos)
paises = ['AD', 'AE', 'AF', 'AG', 'AI', 'AL', 'AM', 'AO', 'AQ', 'AR', 'AS',
          'AT', 'AU', 'AW', 'AX', 'AZ', 'BA', 'BB', 'BD', 'BE', 'BF', 'BG',
          'BH', 'BI', 'BJ', 'BL', 'BM', 'BN', 'BO', 'BQ', 'BR', 'BS', 'BT',
          'BV', 'BW', 'BY', 'BZ', 'CA', 'CC', 'CD', 'CF', 'CG', 'CH', 'CI',
          'CK', 'CL', 'CM', 'CN', 'CO', 'CR', 'CU', 'CV', 'CW', 'CX', 'CY',
          'CZ', 'DE', 'DJ', 'DK', 'DM', 'DO', 'DZ', 'EC', 'EE', 'EG', 'EH',
          'ER', 'ES', 'ET', 'EU', 'FI', 'FJ', 'FK', 'FM', 'FO', 'FR', 'GA',
          'GB', 'GD', 'GE', 'GF', 'GG', 'GH', 'GI', 'GL', 'GM', 'GN', 'GP',
          'GQ', 'GR', 'GS', 'GT', 'GU', 'GW', 'GY', 'HK', 'HM', 'HN', 'HR',
          'HT', 'HU', 'ID', 'IE', 'IL', 'IM', 'IN', 'IO', 'IQ', 'IR', 'IS',
          'IT', 'JE', 'JM', 'JO', 'JP', 'KE', 'KG', 'KH', 'KI', 'KM', 'KN',
          'KP', 'KR', 'KW', 'KY', 'KZ', 'LA', 'LB', 'LC', 'LI', 'LK', 'LR',
          'LS', 'LT', 'LU', 'LV', 'LY', 'MA', 'MC', 'MD', 'ME', 'MF', 'MG',
          'MH', 'MK', 'ML', 'MM', 'MN', 'MO', 'MP', 'MQ', 'MR', 'MS', 'MT',
          'MU', 'MV', 'MW', 'MX', 'MY', 'MZ', 'NA', 'NC', 'NE', 'NF', 'NG',
          'NI', 'NL', 'NO', 'NP', 'NR', 'NU', 'NZ', 'OM', 'PA', 'PE', 'PF',
          'PG', 'PH', 'PK', 'PL', 'PM', 'PN', 'PR', 'PS', 'PT', 'PW', 'PY',
          'QA', 'RE', 'RO', 'RS', 'RU', 'RW', 'SA', 'SB', 'SC', 'SD', 'SE',
          'SG', 'SH', 'SI', 'SJ', 'SK', 'SL', 'SM', 'SN', 'SO', 'SR', 'SS',
          'ST', 'SV', 'SX', 'SY', 'SZ', 'TC', 'TD', 'TF', 'TG', 'TH', 'TJ',
          'TK', 'TL', 'TM', 'TN', 'TO', 'TR', 'TT', 'TV', 'TW', 'TZ', 'UA',
          'UG', 'UM', 'US', 'UY', 'UZ', 'VA', 'VC', 'VE', 'VG', 'VI', 'VN',
          'VU', 'WF', 'WS', 'YE', 'YT', 'ZA', 'ZM', 'ZW']
search = str(input('Nome da vaga: ')).strip()
fmt_search = search.replace(' ', '+')
full_date = datetime.now()
# fmt_date = full_date.strftime("%Y-%m-%d %H:%M")
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
# paises
# for pais in paises:
# url_pag = f'https://www.workana.com/en/jobs?country={pais}&page={i}'

# pesquisa por skills
for nomes in nomes_unicos:
    for i in range(1, 51):
        print(f'Página {i}')
        url_pag = f'https://www.workana.com/en/jobs?&language=xx&query={nomes}&page={i}'
        # pesquisas
        # url_pag = f'https://www.workana.com/en/jobs?{agreement}&language=xx&query={fmt_search}&page={i}'
        site = requests.get(url_pag, headers=headers)
        soup = BeautifulSoup(site.content, 'html.parser')
        jobs = soup.find_all('div', class_='project-item')
        if len(jobs) == 0:
            print('Sem resultados encontrados')
            break
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
                val_min = 0  # value_text
                val_max = 0  # value_text
            else:
                val_min = values[0]
                if len(values) > 1:
                    val_max = values[1]
                else:
                    val_max = values[0]
            tag_date = job.find(class_='date').get('title')
            date = datetime.strptime(tag_date, "%B %d, %Y %H:%M")
            print(date)
            # date_bd = date.strftime("%Y-%m-%d %H:%M")
            # print(date_bd)
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
                        'consulta': full_date
                    }
                )
            except PyMongoError as erro:
                print(erro)
            print()
