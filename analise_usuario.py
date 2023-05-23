from analise import *

# criar pasta para armazenar graficos
new_directory('graficos_usuarios')

# top de vagas por pais
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
        except Exception as e:
            print(f'Não foi possível encontrar {e}')
            pass
        try:
            print(f'Média por hora: {average_hourly_countries[user_country]}')
        except Exception as e:
            print(f'Não foi possível encontrar {e}')
        print()

        # top de vagas por pais
        top_country_skill = df_skills.groupby(['skills', 'pais'])['_id'].count().sort_values(ascending=False)
        top10_country = top_country_skill.loc(axis=0)[:, user_country].head(10)
        print(f'Top 10 de skills do {user_country}')
        print(top10_country)
        skills = top10_country.index.get_level_values(0).tolist()
        values = top10_country.values
        plt.figure(figsize=(10, 7))
        plt.bar(skills, values)
        plt.title(f'{user_country} skills com mais vagas')
        plt.xticks(rotation=90)
        plt.subplots_adjust(bottom=0.4)
        plt.savefig(f'graficos_usuarios/{user_country}_skills')
        # plt.show()
        print()

        # skills mais bem pagas por pais
        pay_skill_country = df_skills.groupby(['skills', 'pais'])['media'].mean().sort_values(ascending=False)
        top10_skills_pais = pay_skill_country.loc(axis=0)[:, user_country].head(10)
        print(f'Top 10 de skills mais bem pagas do {user_country}')
        print(top10_skills_pais)
        skills = top10_skills_pais.index.get_level_values(0).tolist()
        values = top10_skills_pais.values
        plt.figure(figsize=(10, 7))
        plt.bar(skills, values)
        plt.title(f'{user_country} skills mais bem pagas')
        plt.xticks(rotation=90)
        plt.ylabel('U$')
        plt.subplots_adjust(bottom=0.4)
        plt.savefig(f'graficos_usuarios/{user_country}skills_paid')
        # plt.show()
        print()
        break
else:
    print('Não encontrado')

# pesquisa por skills
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
        plt.xticks(rotation=90)
        plt.subplots_adjust(bottom=0.4)
        plt.savefig(f'graficos_usuarios/{user_skill}_countries')
        # plt.show()
        print()

        # skills relacionadas
        print(f'Skills relacionadas a {user_skill}')
        related_skills = df[df['skills'].apply(lambda x: user_skill in x)]
        counter = Counter()
        for skills in related_skills['skills']:
            counter.update(skills)
        counter.pop(user_skill)
        plt.figure(figsize=(10, 7))
        for k, v in counter.most_common()[:11]:
            print(f'{k}: {v}')
            plt.bar(k, v)
        plt.title(f'SKILLS QUE MAIS APARECEM JUNTOS DE {user_skill}')
        plt.xticks(rotation=90)
        plt.subplots_adjust(bottom=0.4)
        plt.savefig(f'graficos_usuarios/{user_skill}_paid_countries')
        # plt.show()
        break
else:
    print('Não encontrado')

# devolve a quantidade vagas e media do input do usuario
try:
    # quantidade de vagas da skill no pais
    print(f'Vagas de {user_skill} no {user_country}: {top_country_skill[user_skill][user_country]}')
    # media de pagamentos da skill no pais
    print(f'Média de pagamentos de {user_skill} em {user_country}: {pay_skill_country[user_skill][user_country]}')
except Exception as e:
    print(f'Não encontradas vagas de {user_skill} em {e}')
