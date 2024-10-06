FROM python:3.10-slim

WORKDIR /app

RUN pip install pipenv

COPY data/sample_data.csv data/sample_data.csv
COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --deploy --ignore-pipfile --system

COPY app .

EXPOSE 5000

CMD gunicorn --bind 0.0.0.0:5000 app:app