from pymongo import MongoClient
import pandas as pd
from flask import Flask

# conectar ao mongo
client = MongoClient('localhost', 27017)
db = client['workana']
collection = db['vagas']

# converter para dataframe
cursor = collection.find()
df = pd.DataFrame(list(cursor))
df['_id'] = df['_id'].apply(lambda x: str(x))
app = Flask(__name__)


@app.route('/', methods=['GET'])
def dataframe():
    return '/all - todas as vagas' \
           '\n/recents - ultimas 1000 vagas' \
           '\n/country - lista de países' \
           '\n/country/country_name - vagas do país' \
           '\n/skill - lista de skills' \
           '\n/skill/skill_name - vagas da skill' \
           '\n/fixed - vagas de pagamentos fixo' \
           '\n/hourly - vagas de pagamento por hora'


country_names = collection.distinct('pais')


@app.route('/all')
def all_jobs():
    df_all_jobs = df.to_dict(orient='records')
    return df_all_jobs


@app.route('/recents')
def recents():
    recent = df.tail(1000).to_dict(orient='records')
    return recent


@app.route('/country')
def country():
    country_names = collection.distinct('pais')
    return country_names


@app.route('/country/<pais>')
def country_jobs(pais):
    jobs = df.loc[df['pais'] == pais]
    if len(jobs) == 0:
        return 'Not found', 404
    return jobs.to_dict(orient='records')


@app.route('/skill')
def skills():
    skills_names = collection.distinct('skills')
    return skills_names


@app.route('/skill/<skill>')
def skills_vagas(skill):
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
