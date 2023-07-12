FROM python:3

WORKDIR /

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "src/workana_mongodb.py"]