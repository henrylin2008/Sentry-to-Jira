FROM registry-gitlab.i.wish.com/contextlogic/tooling-image/golang:1.13.4-alpine3.10 AS base
# install python
RUN apk add --update \
    python \
    py-pip \
    build-base \
    curl \
  && pip install virtualenv \
  && pip install twine \
  && rm -rf /var/cache/apk/*

# include all dependencies needed to upload Python client package
RUN apk update
RUN apk add bash
RUN apk add git
RUN apk add docker
RUN which python
RUN which apk

# Copy the current directory contents into the container at /app
COPY . /app

RUN pip install -r /app/pip-requirements.txt

