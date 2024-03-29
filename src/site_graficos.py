import os
from flask import Flask, render_template
import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from converter import countries_names_fmt, skills_names_fmt

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


@app.route("/")
def album():
    imagens = os.listdir("../static")
    return render_template("index.html", imagens=imagens)


@app.route("/stats")
def stats():
    return f"<p>Total de vagas: {collection.count_documents({})}</p>\
        <p>Total de países: {len(countries_names)}<p>\
        <p>Total de skills: {len(skills_names)}<p>\
        <p>Ultima consulta: {result['consulta']}<p>"


@app.route("/countries")
def countries():
    return countries_names_fmt


@app.route("/skills")
def skills():
    return skills_names_fmt


if __name__ == "__main__":
    app.run(debug=True)
