FROM python:3.7-slim

WORKDIR /taxibot
COPY requirements.txt ./req/

RUN apt-get update \
&& apt-get install gcc -y \
&& pip install -r ./req/requirements.txt \
&& rm -rf /var/lib/apt/lists/*

COPY . .
RUN rm requirements.txt

ENTRYPOINT ["python3.7", "run.py"]