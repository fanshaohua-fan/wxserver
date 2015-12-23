FROM ubuntu:latest
MAINTAINER fanshaohua.fan@gmail.com
RUN apt-get -y update 
RUN apt-get install -y \
    python-dev \
    python-pip \
    tesseract-ocr \
    python-lxml
RUN pip install Flask \
    Flask-SQLAlchemy \
    pytesseract
WORKDIR /app
