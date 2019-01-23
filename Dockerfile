# Dokcerfile made to test this
FROM python:alpine

MAINTAINER David Connor

RUN pip3 install -U python-draytonwiser-api pytest

WORKDIR /root/
ADD . /root/python-draytonwiser-api

WORKDIR /root/python-draytonwiser-api
RUN pip3 install -U -r requirements_dev.txt

CMD python3 -m pytest