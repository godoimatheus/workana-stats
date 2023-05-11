# Workana Scraper e API
Este código é um web scraper que busca informações sobre vagas no site Workana. Ele utiliza a biblioteca Requests para fazer requisições HTTP e a biblioteca BeautifulSoup para fazer a análise do HTML retornado. As informações coletadas são armazenadas em um banco de dados MongoDB. Usando a biblioteca Pandas para ler dados do MongoDB e realizar algumas análises. Também utiliza as bibliotecas Matplotlib e Seaborn para visualização de dados. O código inclui um servidor Flask para disponibilizar uma API que permite consultar dados de vagas de trabalho.

# Requisitos
- Python 3.x
- Bibliotecas:
  - requests
  - beautifulsoup4
  - pymongo
  - pandas
  - flask
  - matplotlib
  - seaborn
# Como usar
- Certifique-se de que as bibliotecas necessárias estão instaladas;
- Inicie o MongoDB na porta 27017;
- Execute o script.

Ao ser executado, o script realizará uma consulta personalizada, perguntando ao usuário o nome da vaga e a forma de pagamento desejada. Caso o usuário opte por não personalizar a consulta, serão buscadas vagas para todas as habilidades únicas presentes no banco de dados.

O script faz a busca por páginas até encontrar a data da última pesquisa realizada no banco de dados, garantindo que não haja coleta duplicada de informações.

# Análise

Alguns dados e gráfico que são possíveis ser gerados:
- Skills com mais vagas 
- Skills com maiores médias de pagamentos
- Quantidade de vagas por país
- Média de pagamentos por país (pagamentos fixos e por hora)
- Skills com maiores médias de pagamentos (fixo e por hora)
- Anos com mais vagas 
- Meses com mais vagas
- Dias com mais vagas

# Endpoints
A API disponibiliza os seguintes endpoints:

- /all: Retorna todas as vagas de trabalho em formato JSON.
- /recents: Retorna as últimas 1000 vagas de trabalho em formato JSON.
- /countries: Retorna uma lista de países.
- /countries/{country_name}: Retorna as vagas de trabalho de um país específico em formato JSON.
- /skills: Retorna uma lista de skills.
- /skills/{skill_name}: Retorna as vagas de trabalho para uma habilidade específica em formato JSON.
- /fixed: Retorna as vagas de trabalho que são pagas por um valor fixo em formato JSON.
- /hourly: Retorna as vagas de trabalho que são pagas por hora em formato JSON.

Os dados retornados por cada endpoint são um dicionário JSON que representa os registros correspondentes do banco de dados MongoDB.

# Notas
O site Workana pode bloquear o IP que estiver realizando muitas requisições em um curto período de tempo. É recomendável limitar o número de requisições por minuto ou hora para evitar esse tipo de bloqueio.