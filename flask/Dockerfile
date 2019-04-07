FROM ubuntu:latest
MAINTAINER fanshaohua.fan@gmail.com
RUN apt-get -y update 
RUN apt-get install -y \
    python3-dev \
    python3-pip
RUN pip3 install Flask \
    Flask-SQLAlchemy \
    httplib2 \
    lxml
WORKDIR /app
