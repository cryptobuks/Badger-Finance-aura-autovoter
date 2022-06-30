FROM python:3.10

ENV PYTHONUNBUFFERED 1

ENV UVICORN_WORKERS 2

ENV APP_HOME /voter
WORKDIR $APP_HOME
COPY . ./

RUN apt-get update -y
RUN apt-get install linux-libc-dev>=5.10.120-1 -y
RUN apt-get install libssl-dev>=1.1.1n-0+deb11u3 -y

RUN pip install --upgrade pip
RUN pip install -r ./aura_voter/requirements/requirements.txt \
    -r ./aura_voter/requirements/dev-requirements.txt \
