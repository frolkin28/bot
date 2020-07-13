FROM python:3.7-slim

COPY . /taxibot
WORKDIR /taxibot


RUN apt-get update \
&& apt-get install gcc -y \
&& pip install -r requirements.txt

CMD ["python3.7", "run.py"]