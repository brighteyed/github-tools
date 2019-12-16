FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV GITEA_URL="http://localhost:3000" \
    GITEA_TOKEN="changeme" \
    GITHUB_USERNAME="changeme" \
    GITHUB_TOKEN="changeme"

CMD [ "python", "./mirror_repositories.py" ]