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
dic_vagas = {'titulo': [], 'valorMin': [], 'valorMax': [], 'formaPag': [], 'data': [], 'skill': [], 'pais': []}
bd = sqlite3.connect(f'{search}_{data_fmt}.db')
cursor = bd.cursor()
cursor.execute(f"CREATE TABLE vagas (titulo text, valor_min real, valor_max real, forma_Pag text, data text, skills text, pais text)")
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
    url_pag = f'https://www.workana.com/jobs?{agreement}&language=xx&query={fmt_search}&page={i}'
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
        # print(valor)
        valor_sem_ponto = valor.replace('.', '')
        valores = re.findall(r'\d+(?:\.\d+)?', valor_sem_ponto)
        print(valor_sem_ponto)
        if 'hora' in valor_sem_ponto:
            print('hora')
            forma_de_pagamento = 'Hora'
        else:
            print('fixo')
            forma_de_pagamento = 'Fixo'
        if len(valores) == 0:
            val_min = valor_sem_ponto
            val_max = valor_sem_ponto  # ou valor sem ponto
        else:
            val_min = valores[0]
            if len(valores) > 1:
                val_max = valores[1]
            else:
                val_max = valores[0]
        # print(val_min)
        # print(val_max)
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
            skills = ', '.join(lista_skill)
            print(lista_skill)
        else:
            skills = 'Sem skills'
            lista_skill.append(skills)
        pais = vaga.find(class_='country-name').get_text().strip()
        print(pais)
        dic_vagas['titulo'].append(titulo)
        dic_vagas['valorMin'].append(val_min)
        dic_vagas['valorMax'].append(val_max)
        dic_vagas['formaPag'].append(forma_de_pagamento)
        dic_vagas['data'].append(data)
        dic_vagas['skill'].append(lista_skill)
        dic_vagas['pais'].append(pais)
        print()
        cursor.execute(f"INSERT INTO vagas (titulo, valor_min, valor_max, forma_Pag, data, skills, pais) VALUES("
                       f"'{titulo}', '{val_min}', '{val_max}', '{forma_de_pagamento}', '{data}', '{skills}', '{pais}')")
        bd.commit()
df = pd.DataFrame(dic_vagas)
df.to_csv(f'{search}_{data_fmt}.csv', encoding='utf-8', sep=';', index=False)
