import os
import pandas as pd
from flask import Flask
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from converter import countries_names_fmt, skills_names_fmt
from converter import dict_countries, dict_skills

# documentação oficial mongodb
uri = os.environ.get("MONGODB_URI", "mongodb://localhost:27017")
client = MongoClient(uri, 27017, server_api=ServerApi("1"))
try:
    client.admin.command("ping")
    print("Conectando ao banco de dados")
except Exception as e:
    print(e)

db = client["workana"]
collection = db["vagas"]
countries_names = collection.distinct("pais")
skills_names = collection.distinct("skills")

# converter para dataframe
cursor = collection.find()
df = pd.DataFrame(list(cursor))

search_filter = {}
sort = list({"consulta": -1}.items())

result = client["workana"]["vagas"].find_one(filter=search_filter, sort=sort)
df["_id"] = df["_id"].apply(str)

app = Flask(__name__)


@app.route("/", methods=["GET"])
def homepage():
    stats = {
        "Total de vagas": collection.count_documents({}),
        "Total de países": len(countries_names),
        "Total de skills": len(skills_names),
        "Ultima atualização": result["consulta"],
    }
    return stats


@app.route("/all")
def all_jobs():
    df_all_jobs = df.to_dict(orient="records")
    return df_all_jobs


@app.route("/recents")
def recents():
    recent = df.tail(1000).to_dict(orient="records")
    return recent


@app.route("/countries")
def country():
    return countries_names_fmt


@app.route("/countries/<pais>")
def country_jobs(pais):
    if pais in dict_countries:
        pais = dict_countries[pais]
        jobs = df.loc[df["pais"] == pais]
    else:
        return "Not found", 404
    return jobs.to_dict(orient="records")


@app.route("/skills")
def skills():
    return skills_names_fmt


@app.route("/skills/<skill>")
def skills_vagas(skill):
    if skill in skills_names_fmt:
        skill = dict_skills[skill]
    else:
        return "Not found", 404
    cursor_skill = collection.find({"skills": skill})
    df_skill = pd.DataFrame(list(cursor_skill))
    df_skill["_id"] = df_skill["_id"].apply(str)
    return df_skill.to_dict(orient="records")


@app.route("/fixed")
def fixed():
    jobs = df.loc[df["forma_pag"] == "Fixed"]
    return jobs.to_dict(orient="records")


@app.route("/hourly")
def hourly():
    jobs = df.loc[df["forma_pag"] == "Hourly"]
    return jobs.to_dict(orient="records")


if __name__ == "__main__":
    app.run()
