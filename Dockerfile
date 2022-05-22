FROM python:3.10

ENV PYTHONUNBUFFERED 1

ENV UVICORN_WORKERS 2

ENV APP_HOME /voter
WORKDIR $APP_HOME
COPY . ./

RUN pip install --upgrade pip
RUN pip install -r ./aura_voter/requirements/requirements.txt \
    -r ./aura_voter/requirements/dev-requirements.txt \
