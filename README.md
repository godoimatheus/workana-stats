# Workana - Scraper, Análise e API

Este projeto contém um web scraper escrito em Python que busca informações sobre vagas no site Workana. Ele utiliza a biblioteca Requests para fazer requisições HTTP e a biblioteca BeautifulSoup para fazer a análise do HTML retornado.

O script permite personalizar a consulta por habilidades e forma de pagamento, e também realiza a verificação da última pesquisa realizada para evitar coletar vagas antigas.

As informações coletadas são armazenadas em um banco de dados MongoDB. Usando a biblioteca Pandas para ler dados do MongoDB e realizar algumas análises. Também utiliza as bibliotecas Matplotlib e Seaborn para visualização de dados. O código inclui um servidor Flask para disponibilizar uma API que permite consultar dados de vagas de trabalho.

> [Workana](https://www.workana.com/) é uma plataforma de mercado para trabalho freelancer e remoto, de contratação de trabalhadores independentes. A empresa tem sua sede na Argentina e possui escritórios no Brasil, na Colômbia e no México, e a partir de 2019 expandiu-se para o Sudeste Asiático. A plataforma está disponível em espanhol, inglês e português. Disponível em <https://pt.wikipedia.org/wiki/Workana>

## Motivação

A motivação por trás deste projeto é facilitar a busca por oportunidades de trabalho no Workana, automatizando o processo de coleta e armazenamento de informações sobre as vagas disponíveis. Ao utilizar web scraping, é possível obter uma visão mais rápida e eficiente das vagas e seus detalhes, permitindo que os usuários encontrem oportunidades relevantes de forma mais fácil.

Além disso, um dos objetivos pessoais deste projeto é o meu desenvolvimento profissional e a criação de um portfólio significativo. Ao participar deste projeto, tenho a oportunidade de aprimorar minhas habilidades em web scraping, manipulação de dados e integração com bancos de dados. Essa experiência me permite aprender conceitos importantes relacionados à coleta e análise de dados, bem como fortalecer minhas habilidades técnicas.

A criação de um portfólio é crucial para destacar minhas habilidades e projetos para potenciais empregadores e clientes. Participar deste projeto me permite demonstrar minhas capacidades de programação, resolução de problemas e trabalho em equipe, o que é fundamental para o meu crescimento profissional. Através deste projeto, poderei reunir exemplos concretos do meu trabalho e mostrar meu progresso ao longo do tempo.

Em resumo, este projeto busca fornecer uma solução prática e automatizada para a busca de oportunidades de trabalho no Workana. Ao mesmo tempo, ele me oferece a oportunidade de me desenvolver profissionalmente, aprimorar minhas habilidades técnicas e criar um portfólio relevante. Estou comprometido em realizar um trabalho de qualidade, agregando valor aos usuários e alcançando meus objetivos pessoais de crescimento na área de desenvolvimento de software.

Além disso, é importante ressaltar que este projeto foi desenvolvido com a valiosa mentoria e orientação do [@ozzono](https://github.com/ozzono). Sua experiência e conhecimento foram fundamentais para o meu aprendizado e crescimento profissional durante o processo de desenvolvimento.

A mentoria do [@ozzono](https://github.com/ozzono) contribuiu significativamente para o aprimoramento das minhas habilidades técnicas, me proporcionando insights valiosos e orientações precisas ao longo do projeto. Sua orientação me ajudou a superar desafios e a encontrar soluções eficientes, permitindo que eu expandisse meu conhecimento e adquirisse uma compreensão mais profunda das melhores práticas de desenvolvimento.

A colaboração com [@ozzono](https://github.com/ozzono) foi uma oportunidade única para aprender com um profissional experiente e receber feedback especializado sobre o projeto. Sua orientação me incentivou a alcançar padrões de excelência e aprimorar constantemente meu trabalho.

Gostaria de expressar minha sincera gratidão ao [@ozzono](https://github.com/ozzono) por compartilhar seu tempo, conhecimento e experiência comigo durante todo o processo. Sua mentoria foi essencial para o sucesso deste projeto e para o meu desenvolvimento profissional.

## Desafios

Concluir este projeto foi bastante desafiador devido a vários obstáculos superados, que incluem:

- Encontrar e utilizar as bibliotecas e frameworks necessários para o projeto.
- Configurar e utilizar um banco de dados MongoDB para armazenar as vagas, evitando duplicações.
- Acessar apenas as páginas que contêm informações sobre vagas.
- Otimizar a busca por vagas, maximizando a quantidade de vagas extraídas.
- Limitar a pesquisa para incluir apenas vagas até dois dias após a data da última vaga adicionada.
- Extrair as datas e convertê-las para um formato adequado para armazenamento em banco de dados.
- Identificar e corrigir erros, como remover aspas de títulos para evitar problemas no código, tratar vagas sem informações de pagamento ou habilidades necessárias.
- Converter os dados obtidos para usar a biblioteca Pandas para análise.
- Separar as habilidades necessárias de cada vaga para tratá-las individualmente.
- Gerar gráficos sem cortar os dados ou nomes das figuras.
- Permitir que o usuário informe o país e a habilidade desejada, e realizar uma busca estatística com base nesses critérios.
- Fornecer os dados através de uma API implementada com o Flask.

## Requisitos

- Python 3.x
- Bibliotecas:
  - [requests](https://pypi.org/project/requests/)
  - [beautifulsoup4](https://beautiful-soup-4.readthedocs.io/en/latest/)
  - [pymongo](https://pymongo.readthedocs.io/en/stable/)
  - [pandas](https://pandas.pydata.org/)
  - [flask](https://flask.palletsprojects.com/)
  - [matplotlib](https://matplotlib.org/)
  - [seaborn](https://seaborn.pydata.org/)
- MongoDB
- Docker

### Python

Documentação oficial em <https://www.python.org/doc/>

1.**Windows**

- Acesse o site oficial do **Python** em <https://www.python.org/downloads/> e clique no botão "Download Python" para baixar o instalador.
- Execute o instalador e marque a opção "Add Python to PATH" durante a instalação.
- Clique em "Install Now" e aguarde o processo de instalação ser concluído.
- Após a instalação, abra o Prompt de Comando (CMD) ou o PowerShell e digite `python --version` para verificar se o Python foi instalado corretamente.
- Para verificar se o **pip** foi instalado corretamente, digite `pip --version` no prompt de comando.

2.**macOS**

- Acesse o site oficial do **Python** em <https://www.python.org/downloads/> e baixe o instalador para **macOS**.
- Execute o instalador baixado e siga as instruções do assistente de instalação.
- Na tela "Installation Type", marque a opção "Install for all users" e clique em "Continue".
- Após a instalação, abra o Terminal e digite `python3 --version` para verificar se o Python foi instalado corretamente.
- Para verificar se o pip foi instalado corretamente, digite `pip3 --version` no Terminal.

3.**Linux(Ubuntu)**

- O **Python** já vem pré-instalado na maioria das distribuições Linux, mas é recomendado instalar o pacote *python3-venv* para criar ambientes virtuais Python. Você pode instalá-lo digitando o seguinte comando no Terminal:

  `sudo apt-get update`

  `sudo apt-get install python3-venv`
- Verifique a versão do Python digitando `python3 --version` no Terminal.
- Para instalar o **pip**, execute o seguinte comando:

  `sudo apt-get install python3-pip`
- Verifique se o **pip** foi instalado corretamente digitando `pip3 --version` no Terminal.

### As bibliotecas e frameworks podem ser instaladas com o comando a seguir no terminal

`pip install requirements.txt -r`

### MongoDB

Documentação oficial em <https://www.mongodb.com/docs/atlas/>

1.**Windows**

- Acesse o site oficial do **MongoDB** em <https://www.mongodb.com/try/download/community> e clique no botão "Download" para baixar o instalador do MongoDB Community Server.
- Execute o instalador e siga as instruções do assistente de instalação.
- Durante a instalação, você pode escolher o diretório de instalação e se deseja instalar o MongoDB Compass, uma interface gráfica para gerenciar o banco de dados.
- Após a conclusão da instalação, o **MongoDB** estará pronto para uso. Por padrão, o serviço do MongoDB será executado na porta 27017.

2.**macOS**

- No **macOS**, é recomendado instalar o **MongoDB** usando o Homebrew, um gerenciador de pacotes para macOS. Abra o Terminal e execute o seguinte comando:

  `brew tap mongodb/brew`

  `brew install mongodb-community`

- Após a conclusão da instalação, o **MongoDB** estará pronto para uso. O serviço do MongoDB será executado na porta 27017.

3.**Linux(Ubuntu)**

- Abra o Terminal e execute os seguintes comandos para importar a chave GPG do repositório oficial do **MongoDB** e adicionar o repositório em seu sistema:

  `wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu $(lsb_release -cs)/mongodb-org/5.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-5.0.list`
- Em seguida, execute os comandos para atualizar o sistema e instalar o pacote do **MongoDB**:

  `sudo apt-get update`

  `sudo apt-get install -y mongodb-org`

### Docker

Opcional o seu uso caso deseje, a seguir o passo a passo de sua instalação.

1.**Windows**

- Acesse o site oficial do **Docker** em <https://www.docker.com/products/docker-desktop> e clique no botão "Download" para baixar o instalador do Docker Desktop para Windows.
- Execute o instalador baixado e siga as instruções do assistente de instalação.
- Durante a instalação, certifique-se de habilitar a opção "Enable Hyper-V" (ou "Ativar Hyper-V") se solicitado.
- Após a conclusão da instalação, o **Docker** estará pronto para uso.

2.**macOS**

- Acesse o site oficial do **Docker** em <https://www.docker.com/products/docker-desktop> e clique no botão "Download" para baixar o instalador do Docker Desktop para **macOS**.
- Execute o instalador baixado e siga as instruções do assistente de instalação.
- Durante a instalação, o Docker Desktop será adicionado à pasta "Applications" (Aplicativos) em seu sistema.
- Após a conclusão da instalação, o **Docker** estará pronto para uso.

3.**Linux (Ubuntu)**:

- Abra o Terminal e execute os seguintes comandos para instalar o **Docker**:

  `sudo apt-get update`

  `sudo apt-get install docker.io`
- Após a instalação, inicie o serviço do **Docker** usando o seguinte comando:

  `sudo systemctl start docker`

- Para verificar se a instalação foi concluída com sucesso, execute o seguinte comando para exibir a versão do **Docker**:

  `docker version`

## Como usar

### Scraper

- Certifique-se de ter uma instância do MongoDB em execução ou configure a conexão para apontar para um banco de dados MongoDB existente.

- Execute o script **workana_mongodb.py** em um ambiente adequado, como um terminal ou uma IDE Python.

Ao ser executado, o script realizará uma consulta personalizada, perguntando ao usuário o nome da vaga e a forma de pagamento desejada. Caso o usuário opte por não personalizar a consulta, serão buscadas vagas para todas as habilidades únicas presentes no banco de dados.

O script faz a busca por páginas até encontrar a data da última pesquisa realizada no banco de dados, garantindo que não haja coleta duplicada de informações.

E para não ter perca de vagas foi criado um index no banco de dados possibilitando adicionar uma vaga contendo o mesmo título mas em dias diferentes, assim também impedindo de existir vagas duplicadas.

Este código também está disponível em docker:

- Linux(Ubuntu)

<https://hub.docker.com/r/godoimatheus/workana-scraper>

Para executar no docker pode-se usar o comando a seguir
`run -it --network="host" godoimatheus/workana-scraper` que a imagem será baixada se não existir localmente e executada.

- Windows

Em desenvolvimento..

>As vagas que contiverem apenas um valor de pagamento, o valor mínimo e máximo serão o mesmo, por exemplo, se for U$ 3000 significa que o pagamento é superior a este, e as vagas com pagamentos em aberto serão adicionadas com valor igual a 0. 

### Análise

Com o script **analise.py** conectado ao banco de dados, basta executá-lo para que seja convertidos os dados para utilizar o **pandas** para serem gerados os gráficos.

Também disponível em docker:

- Linux(Ubuntu)

<https://hub.docker.com/r/godoimatheus/workana-analise>

- Windows

Em desenvolvimento..

Para executar no docker pode-se usar o comando a seguir
`run -it --network="host" godoimatheus/workana-analise` que a imagem será baixada se não existir localmente e executada.

Alguns dados e gráfico que são possíveis ser gerados:

- Skills com mais vagas
- Skills com maiores médias de pagamentos
- Quantidade de vagas por país
- Média de pagamentos por país (fixos e por hora)
- Skills com maiores médias de pagamentos (fixo e por hora)
- Anos com mais vagas
- Meses com mais vagas
- Dias com mais vagas

### Análise com input do usuário

Com o script **analise.py** configurado corretamente, podemos apenas executar o arquivo **analise_usuario.py**, primeiramente ele irá gerar os mesmos gráficos do **analise.py** mas desta vez permitindo ao usuário informar o país e a skill para gerar gráficos personalizados automaticamente contendo informações dos país requerido com as skills que contém mais vagas e as maiores médias de pagamento e retornando para a skill requisitado os países com mais vagas e as tecnologias que mais aparecem juntas da informada pelo usuário, por fim será exibido no console a qunatidade vagas do país e skill seguidos de suas respectivas médias de pagamentos.

Disponível no docker

- Linux(Ubuntu)

<https://hub.docker.com/r/godoimatheus/workana-analise-usuario>

Para executar no docker pode-se usar o comando a seguir
`run -it --network="host" godoimatheus/workana-analise-usuario` que a imagem será baixada se não existir localmente e executada.

- Windows

Em desenvolvimento..

### API

1.Configure a conexão ao banco de dados

2.Execute o código **api.py**

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

### Documentação API

<https://documenter.getpostman.com/view/27018070/2s93ebUWmm>

## Notas

O site Workana pode bloquear o IP que estiver realizando muitas requisições em um curto período de tempo. É recomendável limitar o número de requisições por minuto ou hora para evitar esse tipo de bloqueio.
