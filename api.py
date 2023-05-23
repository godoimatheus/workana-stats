import os

from pymongo import MongoClient
import pandas as pd
from flask import Flask
from converter import *

# conectar ao mongo
# client = MongoClient(os.environ['MONGODB_URI'])
client = MongoClient('localhost', 27017)
db = client['workana']
collection = db['vagas']

# converter para dataframe
cursor = collection.find()
df = pd.DataFrame(list(cursor))

filter = {}
sort = list({
                'consulta': -1
            }.items())

result = client['workana']['vagas'].find_one(
    filter=filter,
    sort=sort
)

df['_id'] = df['_id'].apply(lambda x: str(x))

app = Flask(__name__)


@app.route('/', methods=['GET'])
def homepage():
    stats = {
        'Total de vagas': collection.count_documents({}),
        f'Total de países': len(countries_names),
        f'Total de skills': len(skills_names),
        f'Ultima atualização': result['consulta']
    }
    return stats


@app.route('/all')
def all_jobs():
    df_all_jobs = df.to_dict(orient='records')
    return df_all_jobs


@app.route('/recents')
def recents():
    recent = df.tail(1000).to_dict(orient='records')
    return recent


@app.route('/countries')
def country():
    return countries_names_fmt


@app.route('/countries/<pais>')
def country_jobs(pais):
    if pais in dict_countries:
        pais = dict_countries[pais]
        jobs = df.loc[df['pais'] == pais]
    else:
        return 'Not found', 404
    return jobs.to_dict(orient='records')


@app.route('/skills')
def skills():
    return skills_names_fmt


@app.route('/skills/<skill>')
def skills_vagas(skill):
    if skill in skills_names_fmt:
        skill = dict_skills[skill]
    else:
        return 'Not found', 404
    cursor_skill = collection.find({'skills': skill})
    df_skill = pd.DataFrame(list(cursor_skill))
    df_skill['_id'] = df_skill['_id'].apply(lambda x: str(x))
    return df_skill.to_dict(orient='records')


@app.route('/fixed')
def fixed():
    jobs = df.loc[df['forma_pag'] == 'Fixed']
    return jobs.to_dict(orient='records')


@app.route('/hourly')
def hourly():
    jobs = df.loc[df['forma_pag'] == 'Hourly']
    return jobs.to_dict(orient='records')


if __name__ == '__main__':
    app.run(debug=True)
