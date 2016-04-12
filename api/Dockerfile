FROM ubuntu:latest
MAINTAINER fanshaohua.fan@gmail.com
RUN apt-get -y update 
RUN apt-get install -y \
    python3-dev \
    python3-pip \
    python3-pil \
    python3-httplib2 \
    tesseract-ocr
RUN pip3 install Flask \
    pytesseract 
WORKDIR /api
