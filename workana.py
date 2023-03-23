import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import math
import json
from datetime import datetime
import sqlite3

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                         "(KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}

search = str(input('Nome da vaga: ')).strip()
fmt_search = search.replace(' ', '+')
data_completa = datetime.now()
data_fmt = data_completa.strftime("%d-%m-%Y_%H-%M-%S")
dic_vagas = {'titulo': [], 'valor': [], 'data': [], 'skill': [], 'pais': []}
# bd = sqlite3.connect(f'{search}_{data_fmt}.db')
# cursor = bd.cursor()
# cursor.execute(f"CREATE TABLE vagas (titulo text, valores text, data text, pais text)")
forma_pag = int(input('Escolha a forma de pagamento:'
                      '\n1 - Todas as formas'
                      '\n2 - Pagamento fixo'
                      '\n3 - Pagamento por hora'
                      '\nSua opção: '))
if forma_pag == 1:
    agreement = f'agreement='
elif forma_pag == 2:
    agreement = f'agreement=fixed'
elif forma_pag == 3:
    agreement = f'agreement=hourly'
else:
    print('Opção inválida')
for i in range(1, 51):
    print(f'Página {i}')
    url_pag = f'https://www.workana.com/jobs?{agreement}&language=pt&query={fmt_search}&page={i}'
    site = requests.get(url_pag, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')
    vagas = soup.find_all('div', class_='project-item')
    if len(vagas) == 0:
        print('Sem resultados encontrados')
        break
    for vaga in vagas:
        titulo = vaga.find('span').get('title')
        print(titulo)
        valor = vaga.find(class_='values').get_text()
        print(valor)
        data = vaga.find(class_='date').get('title')
        print(data)
        lista_skill = []
        skill = vaga.find_all('label-expander')
        if len(skill) > 0:
            expand = skill[0][":to-expand"]
            sk = json.loads(expand)
            for s in sk:
                anchor_text = s['anchorText']
                lista_skill.append(anchor_text)
            print(lista_skill)
        else:
            lista_skill.append('Sem skills')
        pais = vaga.find(class_='country-name').get_text().strip()
        print(pais)
        dic_vagas['titulo'].append(titulo)
        dic_vagas['valor'].append(valor)
        dic_vagas['data'].append(data)
        dic_vagas['skill'].append(lista_skill)
        dic_vagas['pais'].append(pais)
        print()
        # cursor.execute(f"INSERT INTO vagas VALUES('{titulo}', '{valor}', '{data}', '{pais}')")
        # bd.commit()
df = pd.DataFrame(dic_vagas)
df.to_csv(f'{search}_{data_fmt}.csv', encoding='utf-8', sep=';')
