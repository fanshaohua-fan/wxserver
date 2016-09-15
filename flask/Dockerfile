FROM ubuntu:latest
MAINTAINER fanshaohua.fan@gmail.com
RUN apt-get -y update 
RUN apt-get install -y \
    python-dev \
    python-pip \
    python-httplib2 \
    python-lxml
RUN pip install Flask \
    Flask-SQLAlchemy
WORKDIR /app
