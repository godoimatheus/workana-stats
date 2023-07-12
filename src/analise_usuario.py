import os
from collections import Counter
import matplotlib.pyplot as plt
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd

# documentação oficial mongodb
uri = os.environ.get("MONGODB_URI", "mongodb://localhost:27017")
client = MongoClient(uri, 27017, server_api=ServerApi("1"))
try:
    client.admin.command("ping")
    print("Conectando ao banco de dados")
except Exception as e:
    print(e)

# conectar ao mongo
db = client["workana"]
collection = db["vagas"]

# converter para dataframe
cursor = collection.find()
df = pd.DataFrame(list(cursor))

# criar pasta para armazenar graficos
print()
print("Verificando se a pasta /graficos_usuario existe")
if not os.path.exists("../graficos_usuario"):
    os.makedirs("../graficos_usuario")
    print("Pasta criada")
else:
    print("A pasta já existe")

# calculo da media e criar nova coluna
df["media"] = (df["valor_min"] + df["valor_max"]) / 2

# quantidade de vagas por skill
DF_SKILLS = df.copy()
DF_SKILLS = DF_SKILLS.drop(["valor_min", "valor_max"], axis=1)
DF_SKILLS = DF_SKILLS.explode("skills")
skills_jobs = DF_SKILLS.groupby("skills")["_id"].count().sort_values(ascending=False)

# top de vagas por pais
top_country_skill = (
    DF_SKILLS.groupby(["skills", "pais"])["_id"].count().sort_values(ascending=False)
)
country_name = collection.distinct("pais")
PAY_SKILL_COUNTRY = None

# quantas vagas por pais
country_jobs = df.groupby("pais")["_id"].count().sort_values(ascending=False)

# media por pagamento fixo por pais
fixed_payment_skills = df[["pais", "media"]].loc[df["forma_pag"] == "Fixed"]
average_fixed_countries = (
    fixed_payment_skills.groupby("pais")["media"].mean().sort_values(ascending=False)
)

# media por pagamento hora de cada pais
hourly_country = df[["pais", "media"]].loc[df["forma_pag"] == "Hourly"]
average_hourly_countries = (
    hourly_country.groupby("pais")["media"].mean().sort_values(ascending=False)
)

# skills mais bem pagas geral
higher_paid_skills = (
    DF_SKILLS.groupby("skills")["media"].mean().sort_values(ascending=False)
)

# input usuario escolher pais
print()
print("INFORME UM PAÍS")
print()
user_country = input("País: ").strip()
for country in country_name:
    if user_country.lower() == country.lower():
        print(f"O país escolhido foi {country}")
        user_country = country
        print(f"Quantidade de vagas: {country_jobs[user_country]}")
        try:
            print(f"Média fixo: {average_fixed_countries[user_country]:.2f}")
        except Exception as e:
            print(f"Não foi possível encontrar {e}")
        try:
            print(f"Média por hora: {average_hourly_countries[user_country]:.2f}")
        except Exception as e:
            print(f"Não foi possível encontrar {e}")
        print()

        # top de vagas por pais
        top_country_skill = (
            DF_SKILLS.groupby(["skills", "pais"])["_id"]
            .count()
            .sort_values(ascending=False)
        )
        PAY_SKILL_COUNTRY = (
            DF_SKILLS.groupby(["skills", "pais"])["media"]
            .mean()
            .sort_values(ascending=False)
        )
        top10_country = top_country_skill.loc(axis=0)[:, user_country].head(10)
        print(f"Top 10 de skills do {user_country}")
        print(top10_country)
        skills = top10_country.index.get_level_values(0).tolist()
        values = top10_country.values
        plt.figure(figsize=(10, 7))
        plt.bar(skills, values)
        plt.suptitle(user_country)
        plt.title("SKILLS COM MAIS VAGAS E SUAS MÉDIAS DE PAGAMENTOS")
        plt.xticks(rotation=90)
        plt.subplots_adjust(bottom=0.4)

        top10_country_name = []
        top10_country_average = []
        for skill in top10_country.index:
            top10_country_name.append(skill[0])
        print()
        print("Valores de pagamentos médios dos países com mais vagas")
        for average in top10_country_name:
            print(f"{average}: {PAY_SKILL_COUNTRY[average][user_country]:.2f}")
            top10_country_average.append(PAY_SKILL_COUNTRY[average][user_country])
        for i, val in enumerate(top10_country_average):
            plt.text(i, values[i] + 1, str(f"{val:.2f}"), ha="center")
        plt.savefig(f"../graficos_usuario/{user_country}_skills")
        # plt.show()
        print()

        # skills mais bem pagas por pais
        top10_skills_pais = PAY_SKILL_COUNTRY.loc(axis=0)[:, user_country].head(10)
        print(f"Top 10 de skills mais bem pagas do {user_country}")
        print(top10_skills_pais)
        skills = top10_skills_pais.index.get_level_values(0).tolist()
        values = top10_skills_pais.values
        plt.figure(figsize=(10, 7))
        plt.bar(skills, values)
        plt.suptitle(user_country)
        plt.title("SKILLS MAIS BEM PAGAS E QUANTIDADE DE VAGAS")
        plt.xticks(rotation=90)
        plt.ylabel("U$")
        plt.subplots_adjust(bottom=0.4)

        # lista com nomes dos paises do top10
        countries_names = []
        for country_name in top10_skills_pais.index:
            countries_names.append(country_name[0])
        # lista das quantidades de vagas
        number_of_jobs = []
        for name in countries_names:
            print(f"{name}: {top_country_skill[name][user_country]}")
            number_of_jobs.append(top_country_skill[name][user_country])
        for i, val in enumerate(number_of_jobs):
            plt.text(i, values[i] + 1, val, ha="center")

        plt.savefig(f"../graficos_usuario/{user_country}_skills_paid")
        # plt.show()
        print()
        break
else:
    print("Não encontrado")
# pesquisa por skills
skills_names = collection.distinct("skills")
print()
print("INFORME UMA SKILL")
print()
user_skill = input("Skill: ").strip()
for skill in skills_names:
    if user_skill.lower() == skill.lower():
        print(skill)
        user_skill = skill
        print(f"Quantidade de vagas: {skills_jobs[user_skill]}")
        print(f"Média de pagamento: {higher_paid_skills[user_skill]:.2f}")
        print()
        print("Top 10 de países com mais vagas de {user_skill}")
        print(top_country_skill[user_skill].head(10))

        plt.figure(figsize=(10, 7))
        plt.bar(
            top_country_skill[user_skill].head(10).index,
            top_country_skill[user_skill].head(10),
        )
        plt.suptitle(user_skill)
        plt.title("PAÍSES COM MAIS VAGAS E SUAS MÉDIAS DE PAGAMENTOS")
        plt.xticks(rotation=90)
        plt.subplots_adjust(bottom=0.4)

        average_of_top10 = []
        for i in top_country_skill[user_skill].head(10).index:
            average_of_top10.append(PAY_SKILL_COUNTRY[user_skill][i])
        for i, val in enumerate(average_of_top10):
            plt.text(
                i,
                top_country_skill[user_skill].head(10)[i] + 1,
                str(f"{val:.2f}"),
                ha="center",
            )

        plt.savefig(f"../graficos_usuario/{user_skill}_countries")
        # plt.show()
        print()

        # maiores medias de pagamentos da skill
        plt.figure(figsize=(10, 7))
        plt.suptitle(user_skill)
        plt.title("MAIORES MÉDIAS DE PAGAMENTOS E QUANTIDADE DE VAGAS")
        x_axis = PAY_SKILL_COUNTRY[user_skill].head(10).index
        y_axis = PAY_SKILL_COUNTRY[user_skill].head(10)
        plt.bar(x_axis, y_axis)
        plt.ylabel("U$")
        plt.xticks(rotation=90)
        plt.subplots_adjust(bottom=0.4)
        skill_number_of_jobs = top_country_skill[user_skill][x_axis]
        for i, val in enumerate(skill_number_of_jobs):
            plt.text(i, y_axis[i] + 1, val, ha="center")

        plt.savefig(f"../graficos_usuario/{user_skill}_average")

        # skills relacionadas
        print(f"Skills relacionadas a {user_skill}")
        related_skills = df[df["skills"].apply(lambda x, us=user_skill: us in x)]
        counter = Counter()
        for skills in related_skills["skills"]:
            counter.update(skills)
        counter.pop(user_skill)
        plt.figure(figsize=(10, 7))
        for k, v in counter.most_common()[:11]:
            print(f"{k}: {v}")
            plt.bar(k, v)
        plt.suptitle(user_skill)
        plt.title("SKILLS RELACIONADAS")
        plt.xticks(rotation=90)
        plt.subplots_adjust(bottom=0.4)
        plt.savefig(f"../graficos_usuario/{user_skill}_related")
        # plt.show()
        break
else:
    print("Não encontrado")

# devolve a quantidade vagas e media do input do usuario
try:
    # quantidade de vagas da skill no pais
    print()
    print(
        f"Vagas de {user_skill} - {user_country}: {top_country_skill[user_skill][user_country]}"
    )
    # media de pagamentos da skill no pais
    print(
        f"Média de pagamentos de {user_skill} - {user_country}: {PAY_SKILL_COUNTRY[user_skill][user_country]:.2f}"
    )
    print()
except Exception as e:
    print(f"Não encontradas vagas de {user_skill} - {e}")

print(
    "Gráficos gerados com sucesso, para consuntá-los verifique a pasta /graficos_usuario"
)
