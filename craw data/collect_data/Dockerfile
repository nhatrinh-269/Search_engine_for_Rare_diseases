FROM --platform=linux/amd64 python:3.9-buster

COPY ./chrome_114_amd64.deb /tmp/

RUN apt-get update && \
    apt-get install -y /tmp/chrome_114_amd64.deb && \
    apt-get install -f

RUN apt-get update && \
    apt-get install -yqq unzip && \
    wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip

ENV DISPLAY=:99

COPY . /craw_data

WORKDIR /craw_data

RUN pip install -r requirements.txt

RUN mkdir /craw_data/collected_data

