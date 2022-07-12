FROM python:3.10

ENV PYTHONUNBUFFERED 1

ENV UVICORN_WORKERS 2

ENV APP_HOME /voter
WORKDIR $APP_HOME
COPY . ./

RUN apt-get update -y
RUN apt-get install linux-libc-dev>=5.10.120-1 -y
RUN apt-get install libssl-dev>=1.1.1n-0+deb11u3 -y
RUN apt-get install openssl>=1.1.1n-0+deb11u3 -y
RUN apt-get install libfreetype6>=2.10.4+dfsg-1+deb11u1 -y
RUN apt-get install libfribidi0>=1.0.8-2+deb11u1 -y

RUN pip install --upgrade pip
RUN pip install -r ./aura_voter/requirements/requirements.txt \
    -r ./aura_voter/requirements/dev-requirements.txt \
