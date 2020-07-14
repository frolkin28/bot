FROM python:3.7-slim

WORKDIR /taxibot
COPY requirements.txt .

RUN apt-get update \
&& apt-get install gcc -y \
&& pip install -r requirements.txt \
&& rm -rf /var/lib/apt/lists/*

COPY . .

ENTRYPOINT ["python3.7", "run.py"]