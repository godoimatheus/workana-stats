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
<<<<<<< HEAD
skills_jobs = df_skills.groupby('skills')['_id'].count().sort_values(ascending=False)
skills_jobs10 = skills_jobs.head(10)
print('Quantidade de vagas skills:')
print(skills_jobs10)

plt.figure(figsize=(10, 6))
plt.bar(skills_jobs10.index, skills_jobs10)
=======
tecnologias_vagas = df_skills.groupby('skills')['_id'].count().sort_values(ascending=False)
tecnologias_vagas10 = tecnologias_vagas.head(10)
print('Quantidade de vagas skills:')
print(tecnologias_vagas10)

plt.figure(figsize=(10, 6))
plt.bar(tecnologias_vagas10.index, tecnologias_vagas10)
>>>>>>> 96018fbdacbec213c3a8e80a32c2ae21f3abe5b5
plt.title('SKILLS COM MAIS VAGAS')
plt.xticks(rotation=90)
plt.subplots_adjust(bottom=0.4)
plt.savefig('fig1')
plt.show()
print()

# skills mais bem pagas geral
<<<<<<< HEAD
higher_paid_skills = df_skills.groupby('skills')['media'].mean().sort_values(ascending=False)
print('Média de skills mais bem pagas')
print(higher_paid_skills.head(10))
plt.figure(figsize=(10, 6))
plt.bar(higher_paid_skills.head(10).index, higher_paid_skills.head(10))
=======
tecnologias_pagas = df_skills.groupby('skills')['media'].mean().sort_values(ascending=False)
print('Média de skills mais bem pagas')
print(tecnologias_pagas.head(10))
plt.figure(figsize=(10, 6))
plt.bar(tecnologias_pagas.head(10).index, tecnologias_pagas.head(10))
>>>>>>> 96018fbdacbec213c3a8e80a32c2ae21f3abe5b5
plt.title('SKILLS COM MAIORES MÉDIAS DE PAGAMENTOS')
plt.xticks(rotation=90)
plt.subplots_adjust(bottom=0.4)
plt.ylabel('U$')
plt.savefig('fig2')
plt.show()
print()

# quantas vagas por pais
<<<<<<< HEAD
country_jobs = df.groupby('pais')['_id'].count().sort_values(ascending=False)
country_jobs10 = country_jobs.head(10)
print('Quantidade de vagas por país')
print(country_jobs10)
plt.figure(figsize=(10, 7))
plt.bar(country_jobs10.index, country_jobs10)
=======
paises_vagas = df.groupby('pais')['_id'].count().sort_values(ascending=False)
paises_vagas10 = paises_vagas.head(10)
print('Quantidade de vagas por país')
print(paises_vagas10)
plt.figure(figsize=(10, 7))
plt.bar(paises_vagas10.index, paises_vagas10)
>>>>>>> 96018fbdacbec213c3a8e80a32c2ae21f3abe5b5
plt.title('QUANTIDADE DE VAGAS POR PAÍS')
plt.xticks(rotation=90)
plt.subplots_adjust(bottom=0.4)
plt.savefig('fig3')
plt.show()
print()

# valor geral medio por pais
<<<<<<< HEAD
higher_paid_countries = df.groupby('pais')['media'].mean().sort_values(ascending=False)
higher_paid_countries10 = higher_paid_countries.head(10)
print('Média de pagamentos por país geral:')
print(higher_paid_countries10)
plt.figure(figsize=(10, 8))
plt.bar(higher_paid_countries10.index, higher_paid_countries10)
=======
paises_maiores_sal = df.groupby('pais')['media'].mean().sort_values(ascending=False)
paises_maiores_sal10 = paises_maiores_sal.head(10)
print('Média de pagamentos por país geral:')
print(paises_maiores_sal10)
plt.figure(figsize=(10, 8))
plt.bar(paises_maiores_sal10.index, paises_maiores_sal10)
>>>>>>> 96018fbdacbec213c3a8e80a32c2ae21f3abe5b5
plt.title('MÉDIA DE PAGAMENTOS POR PAÍS')
plt.xticks(rotation=90)
plt.subplots_adjust(bottom=0.4)
plt.ylabel('U$')
plt.savefig('fig4')
plt.show()
print()

# media por pagamento fixo por pais
<<<<<<< HEAD
fixed_payment_skills = df[['pais', 'media']].loc[df['forma_pag'] == 'Fixed']
average_fixed_countries = fixed_payment_skills.groupby('pais')['media'].mean().sort_values(ascending=False)
average_fixed_countries10 = average_fixed_countries.head(10)
print('Maiores médias de pagamentos fixo por país')
print(average_fixed_countries10)
plt.figure(figsize=(10, 7))
plt.bar(average_fixed_countries10.index, average_fixed_countries10)
=======
pais_fixo = df[['pais', 'media']].loc[df['forma_pag'] == 'Fixed']
media_pais_fixo = pais_fixo.groupby('pais')['media'].mean().sort_values(ascending=False)
media_pais_fixo10 = media_pais_fixo.head(10)
print('Maiores médias de pagamentos fixo por país')
print(media_pais_fixo10)
plt.figure(figsize=(10, 7))
plt.bar(media_pais_fixo10.index, media_pais_fixo10)
>>>>>>> 96018fbdacbec213c3a8e80a32c2ae21f3abe5b5
plt.title('PAÍSES COM MAIORES MÉDIAS DE PAGAMENTOS (FIXO)')
plt.ylabel('U$')
plt.xticks(rotation=90)
plt.subplots_adjust(bottom=0.4)
plt.savefig('fig5')
plt.show()
print()

# media por pagamento hora de cada pais
<<<<<<< HEAD
hourly_country = df[['pais', 'media']].loc[df['forma_pag'] == 'Hourly']
average_hourly_countries = hourly_country.groupby('pais')['media'].mean().sort_values(ascending=False)
average_hourly_countries10 = average_hourly_countries.head(10)
print('Maiores médias de pagamentos por hora por país:')
print(average_hourly_countries10)
plt.figure(figsize=(10, 7))
plt.bar(average_hourly_countries10.index, average_hourly_countries10)
=======
pais_hora = df[['pais', 'media']].loc[df['forma_pag'] == 'Hourly']
media_pais_hora = pais_hora.groupby('pais')['media'].mean().sort_values(ascending=False)
media_pais_hora10 = media_pais_hora.head(10)
print('Maiores médias de pagamentos por hora por país:')
print(media_pais_hora10)
plt.figure(figsize=(10, 7))
plt.bar(media_pais_hora10.index, media_pais_hora10)
>>>>>>> 96018fbdacbec213c3a8e80a32c2ae21f3abe5b5
plt.title('PAÍSES COM MAIORES MÉDIAS DE PAGAMENTOS (HORA)')
plt.xticks(rotation=90)
plt.subplots_adjust(bottom=0.4)
plt.ylabel('U$')
plt.savefig('fig6')
plt.show()
print()

# media por pagamento fixo por skills
<<<<<<< HEAD
fixed_skills = df_skills[['skills', 'media']].loc[df_skills['forma_pag'] == 'Fixed']
average_fixed_skills = fixed_skills.groupby('skills')['media'].mean().sort_values(ascending=False)
average_fixed_skills10 = average_fixed_skills.head(10)
print('Maiores médias de pagamentos fixo por skills:')
print(average_fixed_skills10)
plt.figure(figsize=(10, 7))
plt.bar(average_fixed_skills10.index, average_fixed_skills10)
=======
skills_fixo = df_skills[['skills', 'media']].loc[df_skills['forma_pag'] == 'Fixed']
media_skills_fixo = skills_fixo.groupby('skills')['media'].mean().sort_values(ascending=False)
media_skills_fixo10 = media_skills_fixo.head(10)
print('Maiores médias de pagamentos fixo por skills:')
print(media_skills_fixo10)
plt.figure(figsize=(10, 7))
plt.bar(media_skills_fixo10.index, media_skills_fixo10)
>>>>>>> 96018fbdacbec213c3a8e80a32c2ae21f3abe5b5
plt.title('SKILLS COM MAIORES MÉDIAS DE PAGAMENTO (FIXO)')
plt.xticks(rotation=90)
plt.subplots_adjust(bottom=0.4)
plt.ylabel('U$')
plt.savefig('fig7')
plt.show()
print()

# media por pagamento hora por skills
<<<<<<< HEAD
hourly_skills = df_skills[['skills', 'media']].loc[df_skills['forma_pag'] == 'Hourly']
average_hourly_skills = hourly_skills.groupby('skills')['media'].mean().sort_values(ascending=False)
average_hourly_skills10 = average_hourly_skills.head(10)
print('Maiores médias de pagamentos por hora por skills:')
print(average_hourly_skills10)
plt.figure(figsize=(10, 9))
plt.bar(average_hourly_skills10.index, average_hourly_skills10)
=======
skills_hora = df_skills[['skills', 'media']].loc[df_skills['forma_pag'] == 'Hourly']
media_skills_hora = skills_hora.groupby('skills')['media'].mean().sort_values(ascending=False)
media_skills_hora10 = media_skills_hora.head(10)
print('Maiores médias de pagamentos por hora por skills:')
print(media_skills_hora10)
plt.figure(figsize=(10, 9))
plt.bar(media_skills_hora10.index, media_skills_hora10)
>>>>>>> 96018fbdacbec213c3a8e80a32c2ae21f3abe5b5
plt.title('SKILLS COM MAIORES MÉDIAS DE PAGAMENTOS (HORA)')
plt.xticks(rotation=90)
plt.subplots_adjust(bottom=0.4)
plt.ylabel('U$')
plt.savefig('fig8')
plt.show()
print()

# anos com mais vagas
<<<<<<< HEAD
year_jobs = df.groupby(df['data_vaga'].dt.strftime('%Y'))['_id'].count().sort_values(ascending=False)
year_jobs10 = year_jobs.head(10)
print('Anos com mais vagas')
print(year_jobs10)
plt.figure(figsize=(11, 7))
plt.bar(year_jobs10.index, year_jobs10)
=======
vagas_ano = df.groupby(df['data_vaga'].dt.strftime('%Y'))['_id'].count().sort_values(ascending=False)
vagas_ano10 = vagas_ano.head(10)
print('Anos com mais vagas')
print(vagas_ano10)
plt.figure(figsize=(11, 7))
plt.bar(vagas_ano10.index, vagas_ano10)
>>>>>>> 96018fbdacbec213c3a8e80a32c2ae21f3abe5b5
plt.title('ANOS COM MAIS VAGAS')
plt.savefig('fig9')
plt.show()
print()

# meses com mais vagas
<<<<<<< HEAD
month_jobs = df.groupby(df['data_vaga'].dt.strftime('%Y-%m'))['_id'].count().sort_values(ascending=False)
month_jobs10 = month_jobs.head(10)
print('Meses com mais vagas')
print(month_jobs10)
plt.figure(figsize=(11, 7))
plt.bar(month_jobs10.index, month_jobs10)
=======
vagas_mes = df.groupby(df['data_vaga'].dt.strftime('%Y-%m'))['_id'].count().sort_values(ascending=False)
vagas_mes10 = vagas_mes.head(10)
print('Meses com mais vagas')
print(vagas_mes10)
plt.figure(figsize=(11, 7))
plt.bar(vagas_mes10.index, vagas_mes10)
>>>>>>> 96018fbdacbec213c3a8e80a32c2ae21f3abe5b5
plt.title('MESES COM MAIS VAGAS')
plt.savefig('fig10')
plt.show()
print()

# vagas dia
<<<<<<< HEAD
day_jobs = df.groupby(df['data_vaga'].dt.strftime('%Y-%m-%d'))['_id'].count().sort_values(ascending=False)
day_jobs10 = day_jobs.head(10)
print('Dias com mais vagas')
print(day_jobs10)
plt.figure(figsize=(12, 7))
plt.bar(day_jobs10.index, day_jobs10)
=======
vagas_dia = df.groupby(df['data_vaga'].dt.strftime('%Y-%m-%d'))['_id'].count().sort_values(ascending=False)
vagas_dia10 = vagas_dia.head(10)
print('Dias com mais vagas')
print(vagas_dia10)
plt.figure(figsize=(12, 7))
plt.bar(vagas_dia10.index, vagas_dia10)
>>>>>>> 96018fbdacbec213c3a8e80a32c2ae21f3abe5b5
plt.title('DIAS COM MAIS VAGAS')
plt.savefig('fig11')
plt.show()
print()

# top de vagas por pais
<<<<<<< HEAD
top_country_skill = df_skills.groupby(['skills', 'pais'])['_id'].count().sort_values(ascending=False)
country_name = collection.distinct('pais')

pay_skill_country = None
# input usuario escolher pais
print('Input do usuário país')
user_country = input('País: ').strip()
for country in country_name:
    if user_country.lower() == country.lower():
        print(country)
        user_country = country
        print(f'Quantidade de vagas: {country_jobs[user_country]}')
        try:
            print(f'Média fixo: {average_fixed_countries[user_country]}')
=======
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
>>>>>>> 96018fbdacbec213c3a8e80a32c2ae21f3abe5b5
        except Exception as e:
            print(f'Não foi possível encontrar {e}')
            pass
        try:
<<<<<<< HEAD
            print(f'Média por hora: {average_hourly_countries[user_country]}')
=======
            print(f'Média por hora: {media_pais_hora[usuario_pais]}')
>>>>>>> 96018fbdacbec213c3a8e80a32c2ae21f3abe5b5
        except Exception as e:
            print(f'Não foi possível encontrar {e}')
        print()

        # top de vagas por pais
<<<<<<< HEAD
        top_country_skill = df_skills.groupby(['skills', 'pais'])['_id'].count().sort_values(ascending=False)
        top10_country = top_country_skill.loc(axis=0)[:, user_country].head(10)
        print(f'Top 10 de skills do {user_country}')
        print(top10_country)
        skills = top10_country.index.get_level_values(0).tolist()
        values = top10_country.values
        plt.figure(figsize=(10, 7))
        plt.bar(skills, values)
        plt.title(f'{user_country} skills com mais vagas')
=======
        top_skills_pais = df_skills.groupby(['skills', 'pais'])['_id'].count().sort_values(ascending=False)
        top10_pais = top_skills_pais.loc(axis=0)[:, usuario_pais].head(10)
        print(f'Top 10 de skills do {usuario_pais}')
        print(top10_pais)
        skills = top10_pais.index.get_level_values(0).tolist()
        values = top10_pais.values
        plt.figure(figsize=(10, 7))
        plt.bar(skills, values)
        plt.title(f'{usuario_pais} skills com mais vagas')
>>>>>>> 96018fbdacbec213c3a8e80a32c2ae21f3abe5b5
        plt.xticks(rotation=90)
        plt.subplots_adjust(bottom=0.4)
        plt.savefig('fig12')
        plt.show()
        print()

        # skills mais bem pagas por pais
<<<<<<< HEAD
        pay_skill_country = df_skills.groupby(['skills', 'pais'])['media'].mean().sort_values(ascending=False)
        top10_skills_pais = pay_skill_country.loc(axis=0)[:, user_country].head(10)
        print(f'Top 10 de skills mais bem pagas do {user_country}')
        print(top10_skills_pais)
        skills = top10_skills_pais.index.get_level_values(0).tolist()
        values = top10_skills_pais.values
        plt.figure(figsize=(10, 7))
        plt.bar(skills, values)
        plt.title(f'{user_country} skills mais bem pagas')
=======
        pag_skills_pais = df_skills.groupby(['skills', 'pais'])['media'].mean().sort_values(ascending=False)
        top10_sk_pais = pag_skills_pais.loc(axis=0)[:, usuario_pais].head(10)
        print(f'Top 10 de skills mais bem pagas do {usuario_pais}')
        print(top10_sk_pais)
        skills = top10_sk_pais.index.get_level_values(0).tolist()
        values = top10_sk_pais.values
        plt.figure(figsize=(10, 7))
        plt.bar(skills, values)
        plt.title(f'{usuario_pais} skills mais bem pagas')
>>>>>>> 96018fbdacbec213c3a8e80a32c2ae21f3abe5b5
        plt.xticks(rotation=90)
        plt.ylabel('U$')
        plt.subplots_adjust(bottom=0.4)
        plt.savefig('fig13')
        plt.show()
        print()
        break
else:
    print('Não encontrado')

# pesquisa por skills
<<<<<<< HEAD
skills_names = collection.distinct('skills')
print('Input do usuário skill')
user_skill = input('Skill: ').strip()
for skill in skills_names:
    if user_skill.lower() == skill.lower():
        print(skill)
        user_skill = skill
        print(f'Quantidade de vagas: {skills_jobs[user_skill]}')
        print(f'Média de pagamento: {higher_paid_skills[user_skill]}')
        print()
        print(f'Top 10 de países com mais vagas de {user_skill}')
        print(top_country_skill[user_skill].head(10))
        plt.figure(figsize=(10, 7))
        plt.bar(top_country_skill[user_skill].head(10).index, top_country_skill[user_skill].head(10))
        plt.title(f'PAÍSES COM MAIS VAGAS DE {user_skill}')
=======
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
>>>>>>> 96018fbdacbec213c3a8e80a32c2ae21f3abe5b5
        plt.xticks(rotation=90)
        plt.subplots_adjust(bottom=0.4)
        plt.savefig('fig14')
        plt.show()
        print()

        # skills relacionadas
<<<<<<< HEAD
        print(f'Skills relacionadas a {user_skill}')
        related_skills = df[df['skills'].apply(lambda x: user_skill in x)]
        counter = Counter()
        for skills in related_skills['skills']:
            counter.update(skills)
        counter.pop(user_skill)
=======
        print(f'Skills relacionadas a {usuario_skill}')
        skills_relacionadas = df[df['skills'].apply(lambda x: usuario_skill in x)]
        counter = Counter()
        for skills in skills_relacionadas['skills']:
            counter.update(skills)
        counter.pop(usuario_skill)
>>>>>>> 96018fbdacbec213c3a8e80a32c2ae21f3abe5b5
        plt.figure(figsize=(10, 7))
        for k, v in counter.most_common()[:11]:
            print(f'{k}: {v}')
            plt.bar(k, v)
<<<<<<< HEAD
        plt.title(f'SKILLS QUE MAIS APARECEM JUNTOS DE {user_skill}')
=======
        plt.title(f'SKILLS QUE MAIS APARECEM JUNTOS DE {usuario_skill}')
>>>>>>> 96018fbdacbec213c3a8e80a32c2ae21f3abe5b5
        plt.xticks(rotation=90)
        plt.subplots_adjust(bottom=0.4)
        plt.savefig('fig15')
        plt.show()
        break
else:
    print('Não encontrado')

# gráfico definido por quantidade de skills
<<<<<<< HEAD
average_fixed_countries = fixed_payment_skills.groupby('pais')['media'].agg(['mean', 'count'])
average_fixed_countries = average_fixed_countries.loc[average_fixed_countries['count'] >= 100].sort_values(by='mean', ascending=False).head(10)
plt.figure(figsize=(10, 7))
plt.bar(average_fixed_countries.index, average_fixed_countries['mean'])
=======
media_pais_fixo = pais_fixo.groupby('pais')['media'].agg(['mean', 'count'])
media_pais_fixo = media_pais_fixo.loc[media_pais_fixo['count'] >= 100].sort_values(by='mean', ascending=False).head(10)
plt.figure(figsize=(10, 7))
plt.bar(media_pais_fixo.index, media_pais_fixo['mean'])
>>>>>>> 96018fbdacbec213c3a8e80a32c2ae21f3abe5b5
plt.title('PAÍSES COM MAIORES MÉDIAS COM PELO MENOS 100 VAGAS')
plt.xticks(rotation=90)
plt.subplots_adjust(bottom=0.4)
plt.savefig('fig16')
plt.show()

# devolve a quantidade vagas e media do input do usuario
try:
    # quantidade de vagas da skill no pais
<<<<<<< HEAD
    print(f'Vagas de {user_skill} no {user_country}: {top_country_skill[user_skill][user_country]}')
    # media de pagamentos da skill no pais
    print(f'Média de pagamentos de {user_skill} em {user_country}: {pay_skill_country[user_skill][user_country]}')
except Exception as e:
    print(f'Não encontradas vagas de {user_skill} em {e}')
=======
    print(f'Vagas de {usuario_skill} no {usuario_pais}: {top_skills_pais[usuario_skill][usuario_pais]}')
    # media de pagamentos da skill no pais
    print(f'Média de pagamentos de {usuario_skill} em {usuario_pais}: {pag_skills_pais[usuario_skill][usuario_pais]}')
except Exception as e:
    print(f'Não encontradas vagas de {usuario_skill} em {e}')
>>>>>>> 96018fbdacbec213c3a8e80a32c2ae21f3abe5b5
