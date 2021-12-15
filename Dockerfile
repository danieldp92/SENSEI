FROM python:3.7.1

RUN apt-get update && apt-get install -y default-jdk
RUN mkdir /trend-analysis
COPY /projects/trend-analysis/python/requirements.txt /trend-analysis/requirements.txt

WORKDIR /trend-analysis

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install connexion[swagger-ui]

COPY /projects/trend-analysis /trend-analysis
WORKDIR /trend-analysis/python/
