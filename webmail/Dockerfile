FROM ubuntu:bionic

RUN apt update -y
RUN apt upgrade -y

RUN apt install python3-pip -y --fix-missing

WORKDIR /usr/src/app
COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "odms_webmail/manage.py runserver 0.0.0.0:8000"]