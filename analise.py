import re
from pymongo import MongoClient
import pandas as pd
from matplotlib import pyplot as plt

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
df_skills = df_skills.drop(['_id', 'valor_min', 'valor_max'], axis=1)
df_skills = df_skills.explode('skills')
tecnologias_vagas = df_skills.groupby('skills')['titulo'].count().sort_values(ascending=False)
print(tecnologias_vagas.head(10))

# skills mais bem pagas geral
tecnologias_pagas = df_skills.groupby('skills')['media'].mean().sort_values(ascending=False)
print(tecnologias_pagas.head(10))

# quantas vagas por pais
paises_vagas = df.groupby('pais')['titulo'].count().sort_values(ascending=False)
print(paises_vagas.head(10))

# valor geral medio por pais
paises_maiores_sal = df.groupby('pais')['media'].mean().sort_values(ascending=False)
print(paises_maiores_sal.head(10))

# media por pagamento fixo por pais
pais_fixo = df[['pais', 'media']].loc[df['forma_pag'] == 'Fixed']
media_pais_fixo = pais_fixo.groupby('pais')['media'].mean().sort_values(ascending=False)
print(media_pais_fixo.head(10))

# media por pagamento hora de cada pais
pais_hora = df[['pais', 'media']].loc[df['forma_pag'] == 'Hourly']
media_pais_hora = pais_hora.groupby('pais')['media'].mean().sort_values(ascending=False)
print(media_pais_hora.head(10))

# media por pagamento fixo por skills
skills_fixo = df_skills[['skills', 'media']].loc[df_skills['forma_pag'] == 'Fixed']
media_skills_fixo = skills_fixo.groupby('skills')['media'].mean().sort_values(ascending=False)
print(media_skills_fixo.head(10))

# media por pagamento hora por skills
skills_hora = df_skills[['skills', 'media']].loc[df_skills['forma_pag'] == 'Hourly']
media_skills_hora = skills_hora.groupby('skills')['media'].mean().sort_values(ascending=False)
print(media_skills_hora.head(10))
