FROM python:3-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN apk update && apk add gcc libc-dev libffi-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del gcc libc-dev libffi-dev

COPY mirror_repositories.py ./

CMD [ "python", "./mirror_repositories.py" ]