FROM python:3-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN apk update && apk add gcc libc-dev libffi-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del gcc libc-dev libffi-dev

COPY gh_mirror.py ./
COPY update_token.py ./

VOLUME [ "/repositories" ]

ENTRYPOINT [ "python" ]
CMD [ "gh_mirror.py" ]