FROM ubuntu:bionic

RUN apt update -y
RUN apt upgrade -y

RUN apt install procmail -y
RUN apt install python3-pip -y --fix-missing

RUN mkdir -p /data/emails

WORKDIR /usr/src/app
COPY . .
RUN echo "new build"
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["/bin/bash", "daemon.sh"]