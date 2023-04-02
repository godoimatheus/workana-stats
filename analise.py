import re

from pymongo import MongoClient
import pandas as pd
from matplotlib import pyplot as plt

client = MongoClient('localhost', 27017)
db = client['workana']
collection = db['vagas']
cursor = collection.find()
df = pd.DataFrame(list(cursor))
print(df.columns)
print(df)