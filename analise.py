import re
from pymongo import MongoClient
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from collections import Counter

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
print('Quantidade de vagas skills:')
print(tecnologias_vagas.head(10))
print()

# skills mais bem pagas geral
tecnologias_pagas = df_skills.groupby('skills')['media'].mean().sort_values(ascending=False)
print('Média de skills mais bem pagas')
print(tecnologias_pagas.head(10))
print()

# quantas vagas por pais
paises_vagas = df.groupby('pais')['_id'].count().sort_values(ascending=False)
print('Quantidade de vagas por país:')
print(paises_vagas.head(10))
print()

# valor geral medio por pais
paises_maiores_sal = df.groupby('pais')['media'].mean().sort_values(ascending=False)
print('Média de pagamentos por país geral:')
print(paises_maiores_sal.head(10))
print()

# media por pagamento fixo por pais
pais_fixo = df[['pais', 'media']].loc[df['forma_pag'] == 'Fixed']
media_pais_fixo = pais_fixo.groupby('pais')['media'].mean().sort_values(ascending=False)
print('Maiores médias de pagamentos fixo por país')
print(media_pais_fixo.head(10))
print()

# media por pagamento hora de cada pais
pais_hora = df[['pais', 'media']].loc[df['forma_pag'] == 'Hourly']
media_pais_hora = pais_hora.groupby('pais')['media'].mean().sort_values(ascending=False)
print('Maiores médias de pagamentos por hora por país:')
print(media_pais_hora.head(10))
print()

# media por pagamento fixo por skills
skills_fixo = df_skills[['skills', 'media']].loc[df_skills['forma_pag'] == 'Fixed']
media_skills_fixo = skills_fixo.groupby('skills')['media'].mean().sort_values(ascending=False)
print('Maiores médias de pagamentos fixo por skills:')
print(media_skills_fixo.head(10))
print()

# media por pagamento hora por skills
skills_hora = df_skills[['skills', 'media']].loc[df_skills['forma_pag'] == 'Hourly']
media_skills_hora = skills_hora.groupby('skills')['media'].mean().sort_values(ascending=False)
print('Maiores médias de pagamentos por hora por skills:')
print(media_skills_hora.head(10))
print()

# anos com mais vagas
vagas_ano = df.groupby(df['data_vaga'].dt.strftime('%Y'))['_id'].count().sort_values(ascending=False)
print('Anos com mais vagas')
print(vagas_ano.head(10))
print()

# meses com mais vagas
vagas_mes = df.groupby(df['data_vaga'].dt.strftime('%Y-%m'))['_id'].count().sort_values(ascending=False)
print('Meses com mais vagas')
print(vagas_mes.head(10))
print()

# vagas dia
vagas_dia = df.groupby(df['data_vaga'].dt.strftime('%Y-%m-%d'))['_id'].count().sort_values(ascending=False)
print('Dias com mais vagas')
print(vagas_dia.head(10))
print()

# input usuario escolher pais
paises_nomes = collection.distinct('pais')
print('Input do usuário país')
usuario_pais = input('País: ').strip()
for pais in paises_nomes:
    if usuario_pais.lower() == pais.lower():
        print(pais)
        usuario_pais = pais

        print(f'Quantidade de vagas: {paises_vagas[usuario_pais]}')
        print(f'Média fixo: {media_pais_fixo[usuario_pais]}')
        print(f'Média por hora: {media_pais_hora[usuario_pais]}')
        print()

        # top de vagas por pais
        top_skills_pais = df_skills.groupby(['skills', 'pais'])['_id'].count().sort_values(ascending=False)
        top10_pais = top_skills_pais.loc(axis=0)[:, usuario_pais]
        print(f'Top 10 de skills do {usuario_pais}')
        print(top10_pais.head(10))
        print()

        # skills mais bem pagas por pais
        pag_skills_pais = df_skills.groupby(['skills', 'pais'])['media'].mean().sort_values(ascending=False)
        top10_sk_pais = pag_skills_pais.loc(axis=0)[:, usuario_pais]
        print(f'Top 10 de skills mais bem pagas do {usuario_pais}')
        print(top10_sk_pais.head(10))
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
        print()

        # skills relacionadas
        print(f'Skills relacionadas a {usuario_skill}')
        skills_relacionadas = df[df['skills'].apply(lambda x: usuario_skill in x)]
        counter = Counter()
        for skills in skills_relacionadas['skills']:
            counter.update(skills)
        counter.pop(usuario_skill)
        for k, v in counter.most_common()[:11]:
            print(f'{k}: {v}')

        break
else:
    print('Não encontrado')

# gráfico definido por quantidade de skills
media_pais_fixo = pais_fixo.groupby('pais')['media'].agg(['mean', 'count'])
media_pais_fixo = media_pais_fixo.loc[media_pais_fixo['count'] >= 100].sort_values(by='mean', ascending=False).head(10)
sns.set()
plt.bar(media_pais_fixo.index, media_pais_fixo['mean'])
plt.xticks(rotation=45)
plt.show()