# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /bank-account-app

COPY requirements.txt requirements.txt

RUN apt-get update -y &&  \
    python -m pip install --upgrade pip &&  \
    pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
