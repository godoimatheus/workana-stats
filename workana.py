import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import math
import json
from datetime import datetime

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                         "(KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}

search = str(input('Nome da vaga: ')).strip()
fmt_search = search.replace(' ', '+')
data_completa = datetime.now()
data_fmt = data_completa.strftime("%d-%m-%Y_%H-%M-%S")
print(data_fmt)
dic_vagas = {'titulo': [], 'valor': [], 'data': [], 'skill': [], 'pais': []}
for i in range(1, 51):
    url_pag = f'https://www.workana.com/jobs?language=pt&query={fmt_search}&page={i}'
    print(f'Página {i}')
    site = requests.get(url_pag, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')
    vagas = soup.find_all('div', class_='project-item')
    if len(vagas) == 0:
        break
    for vaga in vagas:
        titulo = vaga.find('span').get('title')
        print(titulo)
        valor = vaga.find(class_='values').get_text()
        print(valor)
        data = vaga.find(class_='date').get('title')
        print(data)
        lista_skill = []
        try:
            skill = vaga.find('label-expander')
            expand = skill[":to-expand"]
            print(skill)
            print(expand)
            sk = json.loads(expand)
            # lista_skill = []
            for s in sk:
                anchor_text = s['anchorText']
                print(anchor_text)
                lista_skill.append(anchor_text)
            print(lista_skill)
        except:
            print('Vaga sem skills')
        pais = vaga.find(class_='country-name').get_text().strip()
        print(pais)
        dic_vagas['titulo'].append(titulo)
        dic_vagas['valor'].append(valor)
        dic_vagas['data'].append(data)
        dic_vagas['skill'].append(lista_skill)
        dic_vagas['pais'].append(pais)
        print()

df = pd.DataFrame(dic_vagas)
df.to_csv(f'C:/Users/mathe/PycharmProjects/workana/{search}_{data_fmt}.csv', encoding='utf-8', sep=';')