from pymongo import MongoClient
import pandas as pd
from flask import Flask
<<<<<<< HEAD
from converter import *
=======
>>>>>>> 96018fbdacbec213c3a8e80a32c2ae21f3abe5b5

# conectar ao mongo
client = MongoClient('localhost', 27017)
db = client['workana']
collection = db['vagas']

# converter para dataframe
cursor = collection.find()
<<<<<<< HEAD
df = pd.DataFrame(list(cursor))
df['_id'] = df['_id'].apply(lambda x: str(x))
=======

df = pd.DataFrame(list(cursor))

df['_id'] = df['_id'].apply(lambda x: str(x))
# df.pop('_id')
>>>>>>> 96018fbdacbec213c3a8e80a32c2ae21f3abe5b5

app = Flask(__name__)


<<<<<<< HEAD
@app.route('/', methods=['GET'])
def dataframe():
    return '/all - todas as vagas' \
           '\n/recents - ultimas 1000 vagas' \
           '\n/countries - lista de países' \
           '\n/countries/country_name - vagas do país' \
=======
@app.route('/')
def dataframe():
    ultimas_vagas = df.tail(10).to_dict(orient='records')
    return '/country - lista de países' \
           '\n/country/country_name - vagas do país' \
>>>>>>> 96018fbdacbec213c3a8e80a32c2ae21f3abe5b5
           '\n/skills - lista de skills' \
           '\n/skills/skill_name - vagas da skill' \
           '\n/fixed - vagas de pagamentos fixo' \
           '\n/hourly - vagas de pagamento por hora'


<<<<<<< HEAD
country_names = collection.distinct('pais')


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
=======
paises_unicos = collection.distinct('pais')


@app.route('/country')
def country():
    country_names = collection.distinct('pais')
    return country_names


@app.route('/country/<pais>')
def paises_vagas(pais):
    vagas = df.loc[df['pais'] == pais]
    if len(vagas) == 0:
        return 'Not found', 404
    return vagas.to_dict(orient='records')


@app.route('/skill')
def skills():
    skills_names = collection.distinct('skills')
    return skills_names


@app.route('/skill/<skill>')
def skills_vagas(skill):
>>>>>>> 96018fbdacbec213c3a8e80a32c2ae21f3abe5b5
    cursor_skill = collection.find({'skills': skill})
    df_skill = pd.DataFrame(list(cursor_skill))
    df_skill['_id'] = df_skill['_id'].apply(lambda x: str(x))
    return df_skill.to_dict(orient='records')


@app.route('/fixed')
def fixed():
<<<<<<< HEAD
    jobs = df.loc[df['forma_pag'] == 'Fixed']
    return jobs.to_dict(orient='records')
=======
    vagas = df.loc[df['forma_pag'] == 'Fixed']
    return vagas.to_dict(orient='records')
>>>>>>> 96018fbdacbec213c3a8e80a32c2ae21f3abe5b5


@app.route('/hourly')
def hourly():
<<<<<<< HEAD
    jobs = df.loc[df['forma_pag'] == 'Hourly']
    return jobs.to_dict(orient='records')

=======
    vagas = df.loc[df['forma_pag'] == 'Hourly']
    return vagas.to_dict(orient='records')
    
>>>>>>> 96018fbdacbec213c3a8e80a32c2ae21f3abe5b5

if __name__ == '__main__':
    app.run(debug=True)
