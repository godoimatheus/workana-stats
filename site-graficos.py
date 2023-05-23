import os
from flask import Flask, render_template
from converter import *
import pandas as pd
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


@app.route('/')
def album():
    imagens = os.listdir('static')
    return render_template('index.html', imagens=imagens)


@app.route('/stats')
def homepage():
    return f"Total de vagas: {collection.count_documents({})},\
        Total de países: {len(countries_names)},\
        Total de skills: {len(skills_names)},\
        Ultima consulta: {result['consulta']}"


if __name__ == '__main__':
    app.run(debug=True)
