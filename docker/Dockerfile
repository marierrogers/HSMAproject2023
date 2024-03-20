FROM python:3.9-slim-buster

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update
RUN apt-get -y install git
RUN git clone https://github.com/marierrogers/HSMAproject2023

RUN apt-get -y install nano wget ca-certificates
RUN apt-get -y install gcc python3-dev build-essential
RUN apt-get -y install tk

RUN cp -a HSMAproject2023/. . && rm -r HSMAproject2023
RUN mkdir -p -v data

RUN pip install -r ./docker/requirements.txt

CMD cd "03_dashboard" && python index.py
