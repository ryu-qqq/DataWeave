FROM apache/airflow:2.7.2-python3.10

COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r /app/requirements.txt

ENV ENVIRONMENT=local
