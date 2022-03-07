FROM golang:alpine as build

RUN go install github.com/x-motemen/ghq@latest

FROM python:3-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN apk update && apk add git

RUN apk update && apk add gcc libc-dev libffi-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del gcc libc-dev libffi-dev

COPY --from=build /go/bin/ghq /usr/local/bin/
COPY gh_starred.py ./

ENV GHQ_ROOT="/ghq"
VOLUME ${GHQ_ROOT}

CMD [ "python", "./gh_starred.py" ]