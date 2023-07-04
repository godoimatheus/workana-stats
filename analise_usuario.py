from analise import *

# criar pasta para armazenar graficos
print()
print('Verificando se a pasta /graficos_usuario existe')
if not os.path.exists('graficos_usuario'):
    os.makedirs('graficos_usuario')
    print('Pasta criada')
else:
    print('A pasta já existe')

# top de vagas por pais
top_country_skill = df_skills.groupby(['skills', 'pais'])['_id'].count().sort_values(ascending=False)
country_name = collection.distinct('pais')
pay_skill_country = None

# input usuario escolher pais
print()
print('INFORME UM PAÍS')
print()
user_country = input('País: ').strip()
for country in country_name:
    if user_country.lower() == country.lower():
        print(f'O país escolhido foi {country}')
        user_country = country
        print(f'Quantidade de vagas: {country_jobs[user_country]}')
        try:
            print(f'Média fixo: {average_fixed_countries[user_country]:.2f}')
        except Exception as e:
            print(f'Não foi possível encontrar {e}')
            pass
        try:
            print(f'Média por hora: {average_hourly_countries[user_country]:.2f}')
        except Exception as e:
            print(f'Não foi possível encontrar {e}')
        print()

        # top de vagas por pais
        top_country_skill = df_skills.groupby(['skills', 'pais'])['_id'].count().sort_values(ascending=False)
        pay_skill_country = df_skills.groupby(['skills', 'pais'])['media'].mean().sort_values(ascending=False)
        top10_country = top_country_skill.loc(axis=0)[:, user_country].head(10)
        print(f'Top 10 de skills do {user_country}')
        print(top10_country)
        skills = top10_country.index.get_level_values(0).tolist()
        values = top10_country.values
        plt.figure(figsize=(10, 7))
        plt.bar(skills, values)
        plt.suptitle(user_country)
        plt.title('SKILLS COM MAIS VAGAS E SUAS MÉDIAS DE PAGAMENTOS')
        plt.xticks(rotation=90)
        plt.subplots_adjust(bottom=0.4)

        top10_country_name = []
        top10_country_average = []
        for skill in top10_country.index:
            top10_country_name.append(skill[0])
        print()
        print('Valores de pagamentos médios dos países com mais vagas')
        for average in top10_country_name:
            print(f'{average} : {pay_skill_country[average][user_country]:.2f}')
            top10_country_average.append(pay_skill_country[average][user_country])
        for i, val in enumerate(top10_country_average):
            plt.text(i, values[i] + 1, str(f'{val:.2f}'), ha='center')
        plt.savefig(f'graficos_usuario/{user_country}_skills')
        plt.show()
        print()

        # skills mais bem pagas por pais
        top10_skills_pais = pay_skill_country.loc(axis=0)[:, user_country].head(10)
        print(f'Top 10 de skills mais bem pagas do {user_country}')
        print(top10_skills_pais)
        skills = top10_skills_pais.index.get_level_values(0).tolist()
        values = top10_skills_pais.values
        plt.figure(figsize=(10, 7))
        plt.bar(skills, values)
        plt.suptitle(user_country)
        plt.title(f'SKILLS MAIS BEM PAGAS')
        plt.xticks(rotation=90)
        plt.ylabel('U$')
        plt.subplots_adjust(bottom=0.4)
        plt.savefig(f'graficos_usuario/{user_country}_skills_paid')
        plt.show()
        print()
        break
else:
    print('Não encontrado')

# pesquisa por skills
skills_names = collection.distinct('skills')
print()
print('INFORME UMA SKILL')
print()
user_skill = input('Skill: ').strip()
for skill in skills_names:
    if user_skill.lower() == skill.lower():
        print(skill)
        user_skill = skill
        print(f'Quantidade de vagas: {skills_jobs[user_skill]}')
        print(f'Média de pagamento: {higher_paid_skills[user_skill]:.2f}')
        print()
        print(f'Top 10 de países com mais vagas de {user_skill}')
        print(top_country_skill[user_skill].head(10))
        plt.figure(figsize=(10, 7))
        plt.bar(top_country_skill[user_skill].head(10).index, top_country_skill[user_skill].head(10))
        plt.suptitle(user_skill)
        plt.title(f'PAÍSES COM MAIS VAGAS')
        plt.xticks(rotation=90)
        plt.subplots_adjust(bottom=0.4)
        plt.savefig(f'graficos_usuario/{user_skill}_countries')
        plt.show()
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
        plt.suptitle(user_skill)
        plt.title(f'SKILLS RELACIONADAS')
        plt.xticks(rotation=90)
        plt.subplots_adjust(bottom=0.4)
        plt.savefig(f'graficos_usuario/{user_skill}_related')
        plt.show()
        break
else:
    print('Não encontrado')

# devolve a quantidade vagas e media do input do usuario
try:
    # quantidade de vagas da skill no pais
    print()
    print(f'Vagas de {user_skill} - {user_country}: {top_country_skill[user_skill][user_country]}')
    # media de pagamentos da skill no pais
    print(f'Média de pagamentos de {user_skill} - {user_country}: {pay_skill_country[user_skill][user_country]:.2f}')
    print()
except Exception as e:
    print(f'Não encontradas vagas de {user_skill} - {e}')

print('Gráficos gerados com sucesso, para consuntá-los verifique a pasta /graficos_usuario')
