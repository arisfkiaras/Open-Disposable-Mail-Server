FROM ubuntu:bionic

RUN apt update -y
RUN apt upgrade -y

RUN apt install postfix -y

RUN useradd -m recipient

RUN apt install postfix-pcre -y
RUN apt install mailutils -y

COPY ./main.cf /etc/postfix/main.cf
COPY ./virtual /etc/postfix/virtual


RUN postmap /etc/postfix/virtual

RUN service postfix restart
EXPOSE 25
