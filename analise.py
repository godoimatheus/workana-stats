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

print()
nomes_quantidade = {}
nomes_unicos = collection.distinct('skills')
for nome in nomes_unicos:
    quantidade = collection.count_documents({'skills': nome})
    nomes_quantidade[nome] = quantidade
    # print(f'{nome}: {quantidade}')
print(nomes_quantidade)


'''dicionario_ordenado = dict(sorted(nomes_quantidade.items(), key=lambda item: item[1], reverse=True))
plt.bar(dicionario_ordenado.keys(), dicionario_ordenado.values())
plt.show()


# ordene o dicionário pelos valores em ordem decrescente
nomes_quantidade_ordenado = dict(sorted(nomes_quantidade.items(), key=lambda item: item[1], reverse=True))

# pegue as 10 primeiras chaves e valores
top_10 = dict(list(nomes_quantidade_ordenado.items())[:10])

# plote um gráfico de barras das 10 principais habilidades
plt.bar(top_10.keys(), top_10.values())
plt.xlabel('Habilidade')
plt.ylabel('Quantidade')
plt.title('10 principais habilidades')
plt.show()'''
