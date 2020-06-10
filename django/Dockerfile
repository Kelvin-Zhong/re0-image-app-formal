FROM python:3.7-slim-buster
MAINTAINER guigudiuge

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN apt-get update
RUN apt-get install -y postgresql-server-dev-11 postgresql-11 postgresql-client-11 \
  libpq-dev libjpeg-dev gcc libc-dev musl-dev libpng-dev zlib1g-dev libgtk2.0-dev
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app/ /app
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN adduser user
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/web
USER user