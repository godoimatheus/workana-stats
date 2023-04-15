import re
from pymongo import MongoClient
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from collections import Counter

# set seaborn
sns.set_theme()

# conectar ao mongo
client = MongoClient('localhost', 27017)
db = client['workana']
collection = db['vagas']

# converter para dataframe
cursor = collection.find()
df = pd.DataFrame(list(cursor))

# calculo da media e criar nova coluna
df['media'] = (df['valor_min'] + df['valor_max']) / 2

# quantidade de vagas por skill
df_skills = df.copy()
df_skills = df_skills.drop(['valor_min', 'valor_max'], axis=1)
df_skills = df_skills.explode('skills')
tecnologias_vagas = df_skills.groupby('skills')['_id'].count().sort_values(ascending=False)
tecnologias_vagas10 = tecnologias_vagas.head(10)
print('Quantidade de vagas skills:')
print(tecnologias_vagas10)

plt.figure(figsize=(10, 6))
plt.bar(tecnologias_vagas10.index, tecnologias_vagas10)
plt.title('SKILLS COM MAIS VAGAS')
plt.xticks(rotation=90)
plt.subplots_adjust(bottom=0.4)
plt.show()
print()

# skills mais bem pagas geral
tecnologias_pagas = df_skills.groupby('skills')['media'].mean().sort_values(ascending=False)
print('Média de skills mais bem pagas')
print(tecnologias_pagas.head(10))
plt.figure(figsize=(10, 6))
plt.bar(tecnologias_pagas.head(10).index, tecnologias_pagas.head(10))
plt.title('SKILLS COM MAIORES MÉDIAS DE PAGAMENTOS')
plt.xticks(rotation=90)
plt.subplots_adjust(bottom=0.4)
plt.ylabel('U$')
plt.show()
print()

# quantas vagas por pais
paises_vagas = df.groupby('pais')['_id'].count().sort_values(ascending=False)
paises_vagas10 = paises_vagas.head(10)
print('Quantidade de vagas por país')
print(paises_vagas10)
plt.figure(figsize=(10, 7))
plt.bar(paises_vagas10.index, paises_vagas10)
plt.title('QUANTIDADE DE VAGAS POR PAÍS')
plt.xticks(rotation=90)
plt.subplots_adjust(bottom=0.4)
plt.show()
print()

# valor geral medio por pais
paises_maiores_sal = df.groupby('pais')['media'].mean().sort_values(ascending=False)
paises_maiores_sal10 = paises_maiores_sal.head(10)
print('Média de pagamentos por país geral:')
print(paises_maiores_sal10)
plt.figure(figsize=(10, 8))
plt.bar(paises_maiores_sal10.index, paises_maiores_sal10)
plt.title('MÉDIA DE PAGAMENTOS POR PAÍS')
plt.xticks(rotation=90)
plt.subplots_adjust(bottom=0.4)
plt.ylabel('U$')
plt.show()
print()

# media por pagamento fixo por pais
pais_fixo = df[['pais', 'media']].loc[df['forma_pag'] == 'Fixed']
media_pais_fixo = pais_fixo.groupby('pais')['media'].mean().sort_values(ascending=False)
media_pais_fixo10 = media_pais_fixo.head(10)
print('Maiores médias de pagamentos fixo por país')
print(media_pais_fixo10)
plt.figure(figsize=(10, 7))
plt.bar(media_pais_fixo10.index, media_pais_fixo10)
plt.title('PAÍSES COM MAIORES MÉDIAS DE PAGAMENTOS (FIXO)')
plt.ylabel('U$')
plt.xticks(rotation=90)
plt.subplots_adjust(bottom=0.4)
plt.show()
print()

# media por pagamento hora de cada pais
pais_hora = df[['pais', 'media']].loc[df['forma_pag'] == 'Hourly']
media_pais_hora = pais_hora.groupby('pais')['media'].mean().sort_values(ascending=False)
media_pais_hora10 = media_pais_hora.head(10)
print('Maiores médias de pagamentos por hora por país:')
print(media_pais_hora10)
plt.figure(figsize=(10, 7))
plt.bar(media_pais_hora10.index, media_pais_hora10)
plt.title('PAÍSES COM MAIORES MÉDIAS DE PAGAMENTOS (HORA)')
plt.xticks(rotation=90)
plt.subplots_adjust(bottom=0.4)
plt.ylabel('U$')
plt.show()
print()

# media por pagamento fixo por skills
skills_fixo = df_skills[['skills', 'media']].loc[df_skills['forma_pag'] == 'Fixed']
media_skills_fixo = skills_fixo.groupby('skills')['media'].mean().sort_values(ascending=False)
media_skills_fixo10 = media_skills_fixo.head(10)
print('Maiores médias de pagamentos fixo por skills:')
print(media_skills_fixo10)
plt.figure(figsize=(10, 7))
plt.bar(media_skills_fixo10.index, media_skills_fixo10)
plt.title('SKILLS COM MAIORES MÉDIAS DE PAGAMENTO (FIXO)')
plt.xticks(rotation=90)
plt.subplots_adjust(bottom=0.4)
plt.ylabel('U$')
plt.show()
print()

# media por pagamento hora por skills
skills_hora = df_skills[['skills', 'media']].loc[df_skills['forma_pag'] == 'Hourly']
media_skills_hora = skills_hora.groupby('skills')['media'].mean().sort_values(ascending=False)
media_skills_hora10 = media_skills_hora.head(10)
print('Maiores médias de pagamentos por hora por skills:')
print(media_skills_hora10)
plt.figure(figsize=(10, 9))
plt.bar(media_skills_hora10.index, media_skills_hora10)
plt.title('SKILLS COM MAIORES MÉDIAS DE PAGAMENTOS (HORA)')
plt.xticks(rotation=90)
plt.subplots_adjust(bottom=0.4)
plt.ylabel('U$')
plt.show()
print()

# anos com mais vagas
vagas_ano = df.groupby(df['data_vaga'].dt.strftime('%Y'))['_id'].count().sort_values(ascending=False)
vagas_ano10 = vagas_ano.head(10)
print('Anos com mais vagas')
print(vagas_ano10)
plt.figure(figsize=(11, 7))
plt.bar(vagas_ano10.index, vagas_ano10)
plt.title('ANOS COM MAIS VAGAS')
plt.show()
print()

# meses com mais vagas
vagas_mes = df.groupby(df['data_vaga'].dt.strftime('%Y-%m'))['_id'].count().sort_values(ascending=False)
vagas_mes10 = vagas_mes.head(10)
print('Meses com mais vagas')
print(vagas_mes10)
plt.figure(figsize=(11, 7))
plt.bar(vagas_mes10.index, vagas_mes10)
plt.title('MESES COM MAIS VAGAS')
plt.show()
print()

# vagas dia
vagas_dia = df.groupby(df['data_vaga'].dt.strftime('%Y-%m-%d'))['_id'].count().sort_values(ascending=False)
vagas_dia10 = vagas_dia.head(10)
print('Dias com mais vagas')
print(vagas_dia10)
plt.figure(figsize=(12, 7))
plt.bar(vagas_dia10.index, vagas_dia10)
plt.title('DIAS COM MAIS VAGAS')
plt.show()
print()

# top de vagas por pais
top_skills_pais = df_skills.groupby(['skills', 'pais'])['_id'].count().sort_values(ascending=False)
paises_nomes = collection.distinct('pais')

pag_skills_pais = None
# input usuario escolher pais
print('Input do usuário país')
usuario_pais = input('País: ').strip()
for pais in paises_nomes:
    if usuario_pais.lower() == pais.lower():
        print(pais)
        usuario_pais = pais
        print(f'Quantidade de vagas: {paises_vagas[usuario_pais]}')
        try:
            print(f'Média fixo: {media_pais_fixo[usuario_pais]}')
        except Exception as e:
            print(f'Não foi possível encontrar {e}')
            pass
        try:
            print(f'Média por hora: {media_pais_hora[usuario_pais]}')
        except Exception as e:
            print(f'Não foi possível encontrar {e}')
        print()

        # top de vagas por pais
        top_skills_pais = df_skills.groupby(['skills', 'pais'])['_id'].count().sort_values(ascending=False)
        top10_pais = top_skills_pais.loc(axis=0)[:, usuario_pais].head(10)
        print(f'Top 10 de skills do {usuario_pais}')
        print(top10_pais)
        skills = top10_pais.index.get_level_values(0).tolist()
        values = top10_pais.values
        plt.figure(figsize=(10, 7))
        plt.bar(skills, values)
        plt.title(f'{usuario_pais} skills com mais vagas')
        plt.xticks(rotation=90)
        plt.subplots_adjust(bottom=0.4)
        plt.show()
        print()

        # skills mais bem pagas por pais
        pag_skills_pais = df_skills.groupby(['skills', 'pais'])['media'].mean().sort_values(ascending=False)
        top10_sk_pais = pag_skills_pais.loc(axis=0)[:, usuario_pais].head(10)
        print(f'Top 10 de skills mais bem pagas do {usuario_pais}')
        print(top10_sk_pais)
        skills = top10_sk_pais.index.get_level_values(0).tolist()
        values = top10_sk_pais.values
        plt.figure(figsize=(10, 7))
        plt.bar(skills, values)
        plt.title(f'{usuario_pais} skills mais bem pagas')
        plt.xticks(rotation=90)
        plt.ylabel('U$')
        plt.subplots_adjust(bottom=0.4)
        plt.show()
        print()
        break
else:
    print('Não encontrado')

# pesquisa por skills
skills_nomes = collection.distinct('skills')
print('Input do usuário skill')
usuario_skill = input('Skill: ').strip()
for skill in skills_nomes:
    if usuario_skill.lower() == skill.lower():
        print(skill)
        usuario_skill = skill
        print(f'Quantidade de vagas: {tecnologias_vagas[usuario_skill]}')
        print(f'Média de pagamento: {tecnologias_pagas[usuario_skill]}')
        print()
        print(f'Top 10 de países com mais vagas de {usuario_skill}')
        print(top_skills_pais[usuario_skill].head(10))
        plt.figure(figsize=(10, 7))
        plt.bar(top_skills_pais[usuario_skill].head(10).index, top_skills_pais[usuario_skill].head(10))
        plt.title(f'PAÍSES COM MAIS VAGAS DE {usuario_skill}')
        plt.xticks(rotation=90)
        plt.subplots_adjust(bottom=0.4)
        plt.show()
        print()

        # skills relacionadas
        print(f'Skills relacionadas a {usuario_skill}')
        skills_relacionadas = df[df['skills'].apply(lambda x: usuario_skill in x)]
        counter = Counter()
        for skills in skills_relacionadas['skills']:
            counter.update(skills)
        counter.pop(usuario_skill)
        plt.figure(figsize=(10, 7))
        for k, v in counter.most_common()[:11]:
            print(f'{k}: {v}')
            plt.bar(k, v)
        plt.title(f'SKILLS QUE MAIS APARECEM JUNTOS DE {usuario_skill}')
        plt.xticks(rotation=90)
        plt.subplots_adjust(bottom=0.4)
        plt.show()
        break
else:
    print('Não encontrado')

# gráfico definido por quantidade de skills
media_pais_fixo = pais_fixo.groupby('pais')['media'].agg(['mean', 'count'])
media_pais_fixo = media_pais_fixo.loc[media_pais_fixo['count'] >= 100].sort_values(by='mean', ascending=False).head(10)
plt.figure(figsize=(10, 7))
plt.bar(media_pais_fixo.index, media_pais_fixo['mean'])
plt.title('PAÍSES COM MAIORES MÉDIAS COM PELO MENOS 100 VAGAS')
plt.xticks(rotation=90)
plt.subplots_adjust(bottom=0.4)
plt.show()

# devolve a quantidade vagas e media do input do usuario
try:
    print(top_skills_pais[usuario_skill][usuario_pais])  # quantidade de vagas da skill no pais
    print(pag_skills_pais[usuario_skill][usuario_pais])  # meidia de pagamentos da skill no pais
except Exception as e:
    print(f'Não encontradas vagas de {usuario_skill} em {e}')
