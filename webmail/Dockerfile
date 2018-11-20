FROM ubuntu:bionic

RUN apt update -y
RUN apt upgrade -y

RUN apt install python3-pip -y --fix-missing

WORKDIR /usr/src/app
COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt
