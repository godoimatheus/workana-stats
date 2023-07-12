import json
import re
from datetime import datetime, timedelta
import random
import os
import pymongo
from bs4 import BeautifulSoup
import requests
from pymongo.errors import PyMongoError
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}

# conectar mongo
# documentação oficial mongodb
uri = os.environ.get("MONGODB_URI", "mongodb://localhost:27017")
client = MongoClient(uri, server_api=ServerApi("1"))
try:
    client.admin.command("ping")
    print("Conectando ao banco de dados")
except Exception as e:
    print(e)
db = client["workana"]
collection = db["vagas"]

# indice para aceitar somente titulos e datas únicos
db["vagas"].create_index(
    [("titulo", pymongo.ASCENDING), ("data_vaga", pymongo.ASCENDING)], unique=True
)

# navegar somente até a data da última pesquisas
search_filter = {}
sort = list({"consulta": -1}.items())

result = client["workana"]["vagas"].find_one(filter=search_filter, sort=sort)
# número de documentos
documents_numbers = collection.count_documents({})
print(f"Vagas atuais: {documents_numbers}")

# skills unicas no bd
skills_names = collection.distinct("skills")
payment_type = ["", "fixed", "hourly"]
customize = int(input("Personalizar consulta: \n1 - SIM \n2 - NÃO \nOpção: "))
while customize not in (1, 2):
    customize = int(input("Opção: "))
AGREEMENT = ""
skills_names2 = []
if customize == 1 or len(skills_names) == 0:
    SEARCH = str(input("Nome da vaga: ")).strip()
    FMT_SEARCH = SEARCH.replace(" ", "+")
    payment = int(
        input(
            "Escolha a forma de pagamento:"
            "\n0 - Todas as formas"
            "\n1 - Pagamento fixo"
            "\n2 - Pagamento por hora"
            "\nSua opção: "
        )
    )

    if payment == 0:
        AGREEMENT = payment_type[0]
    elif payment == 1:
        AGREEMENT = payment_type[1]
    elif payment == 2:
        AGREEMENT = payment_type[2]
    else:
        print("Opção inválida")
        while payment < 0 or payment > 2:
            payment = int(input("Opção: "))
    # query = fmt_search
    skills_names2.append(SEARCH)
elif customize == 2:
    AGREEMENT = payment_type[0]
    skills_names2 = skills_names.copy()
    random.shuffle(skills_names2)

# pesquisa por skills
COUNT = 0
NEW_JOBS = 0
for NAMES in skills_names2:
    COUNT += 1
    for i in range(1, 51):
        if NAMES == "Sem skills":
            NAMES = ""
        if NAMES == "C#":
            NAMES = "c-1"
        if NAMES == "C++":
            NAMES = "c-2"
        print(f"Página {i} - {NAMES} - {COUNT}/{len(skills_names2)}")
        # skills url
        url_page = f"https://www.workana.com/en/jobs?agreement={AGREEMENT}&language=xx&query={NAMES}&page={i}"
        site = requests.get(url_page, headers=headers, timeout=10)
        soup = BeautifulSoup(site.content, "html.parser")
        jobs = soup.find_all("div", class_="project-item")
        if len(jobs) == 0:
            print("Sem resultados encontrados")
            break
        DATE = ""
        for job in jobs:
            title = job.find("span").get("title").replace('"', "'")
            print(title)
            value_text = job.find(class_="values").get_text().replace(",", "")
            values = re.findall(r"\d+(?:\.\d+)?", value_text)
            print(value_text)
            if "hour" in value_text:
                PAYMENT_METHOD = "Hourly"
            else:
                PAYMENT_METHOD = "Fixed"
            if len(values) == 0:
                VAL_MIN = 0
                VAL_MAX = 0
            else:
                val_min = values[0]
                if len(values) > 1:
                    VAL_MAX = values[1]
                else:
                    VAL_MAX = values[0]
            tag_date = job.find(class_="date").get("title")
            DATE = datetime.strptime(tag_date, "%B %d, %Y %H:%M")
            print(DATE)
            skills_list = []
            tag_label = job.find_all("label-expander")
            if len(tag_label) > 0:
                expand = tag_label[0][":to-expand"]
                skills = json.loads(expand)
                for skill in skills:
                    anchor_text = skill["anchorText"]
                    skills_list.append(anchor_text)
                SKILL_TEXT = ", ".join(skills_list)
                print(skills_list)
            else:
                SKILL_TEXT = "Sem skills"
                skills_list.append(SKILL_TEXT)
            country = job.find(class_="country-name").get_text().strip()
            print(country)
            utc_time = datetime.utcnow()
            try:
                db["vagas"].insert_one(
                    {
                        "titulo": title,
                        "valor_min": int(val_min),
                        "valor_max": int(VAL_MAX),
                        "forma_pag": PAYMENT_METHOD,
                        "data_vaga": DATE,
                        "skills": skills_list,
                        "pais": country,
                        "consulta": utc_time,
                    }
                )
                NEW_JOBS += 1
            except PyMongoError as erro:
                print(erro)
            print()
        if documents_numbers > 0:
            if DATE < result["consulta"] - timedelta(days=2):
                break
print(f"Novas vagas: {NEW_JOBS}")
