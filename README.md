# github-tools

A collection of tools to automate some activities at Github:
  * A tool to mirror GitHub repositories to Gitea
  * A tool to clone starred repositories with [ghq](https://github.com/x-motemen/ghq)
  
## Mirror repositories

### Docker
You can use docker to mirror Github repositories to Gitea:
```
    docker run --rm -e GITHUB_USENAME="changeme" \
                    -e GITHUB_TOKEN="changeme" \
                    -e GITEA_URL="changeme" \
                    -e GITEA_TOKEN="changeme" \
                    ghcr.io/brighteyed/gh-mirror:latest
```

Sample `docker-compose.yml` to periodically mirror Github repositories using [mcuadros/ofelia](https://github.com/mcuadros/ofelia):
```
version: "3"

services:
  ofelia:
    image: mcuadros/ofelia:latest
    command: daemon --docker
    container_name: gh-mirror
    networks:
      - gitea
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    labels:
      - "ofelia.job-run.mirror.schedule=0 0 2 * * *"
      - "ofelia.job-run.mirror.network=gitea"
      - "ofelia.job-run.mirror.image=ghcr.io/brighteyed/gh-mirror"
      - ofelia.job-run.mirror.environment=["GITEA_URL=${GITEA_URL}", "GITEA_TOKEN=${GITEA_TOKEN}", "GITHUB_USERNAME=${GITHUB_USERNAME}", "GITHUB_TOKEN=${GITHUB_TOKEN}"]

networks:
  gitea:
    external: true
    name: gitea
```

### Environment:
  * `GITHUB_USERNAME` – Github account name
  * `GITHUB_TOKEN` – Github token to access repositories
  * `GITEA_URL` – Gitea URL
  * `GITEA_TOKEN` – Gitea user token to access via API

## Clone starred repositories

### Docker
You can use docker to clone and update starred repositories:
```
    docker run --rm -v /path/to/dir:/ghq ghcr.io/brighteyed/gh-starred:latest
```

Sample `docker-compose.yml` to periodically clone/update starred repositories using [mcuadros/ofelia](https://github.com/mcuadros/ofelia):
```
version: "3"

services:
  ofelia:
    image: mcuadros/ofelia:latest
    command: daemon --docker
    container_name: gh-starred
    networks:
      - gitea
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    labels:
      - "ofelia.job-run.starred.schedule=0 0 2 * * *"
      - "ofelia.job-run.starred.network=gitea"
      - "ofelia.job-run.starred.image=ghcr.io/brighteyed/gh-starred"
      - ofelia.job-run.starred.volume="./ghq:/ghq"

networks:
  gitea:
    external: true
    name: gitea
```
