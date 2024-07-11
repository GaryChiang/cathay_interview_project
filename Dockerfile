FROM python:3.11-slim-buster as base
RUN mkdir /app
COPY requirements.txt /app/

WORKDIR /app

RUN apt-get -y update && apt-get -y upgrade && apt-get install -y --no-install-recommends build-essential gcc g++ libsasl2-dev python-dev

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


FROM python:3.11-slim-buster
COPY --from=base /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

COPY . /app

EXPOSE 8080

CMD uvicorn --host 0.0.0.0 --port 8080 main:app --proxy-headers