from pymongo import MongoClient
from unidecode import unidecode
import re

# conectar ao mongo
client = MongoClient('localhost', 27017)
db = client['workana']
collection = db['vagas']
countries_names = collection.distinct('pais')
skills_names = collection.distinct('skills')
countries_names_fmt = []
skills_names_fmt = []

for country in countries_names:
    country = unidecode(country)
    country = re.sub(r'[^\w\s-]', '', country)
    country = re.sub(r'\s', '-', country)
    country = country.lower()
    countries_names_fmt.append(country)
dict_countries = dict(zip(countries_names_fmt, countries_names))

for skill in skills_names:
    skill = unidecode(skill)
    skill = re.sub(r'[^\w\s-]', '', skill)
    skill = re.sub(r'\s', '-', skill)
    skill = skill.lower()
    skills_names_fmt.append(skill)
dict_skills = dict(zip(skills_names_fmt, skills_names))
