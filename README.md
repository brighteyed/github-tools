# github-tools

A collection of tools to automate some activities at Github:
  * A tool to mirror GitHub repositories to Gitea
  
## Mirror repositories

### Docker
You can use docker to mirror Github repositories to Gitea:
```
    docker run --rm -e GITHUB_USENAME="changeme" \
                    -e GITHUB_TOKEN="changeme" \
                    -e GITEA_URL="changeme" \
                    -e GITEA_TOKEN="changeme" \
                    ghcr.io/brighteyed/github-tools:latest
```

### Docker compose
Sample `docker-compose.yml` for gitea:
```
version: "3"

services:
  gitea:
    image: gitea/gitea:latest
    container_name: gitea
    environment:
      - USER_UID=1000
      - USER_GID=1000
    networks:
      - gitea
    volumes:
      - ./gitea:/data
    ports:
      - "3000:3000"
      - "2222:22"

networks:
  gitea:
    external: true
    name: gitea
```

Sample `docker-compose.yml` to periodically mirror Github repositories using [mcuadros/ofelia](https://github.com/mcuadros/ofelia):
```
version: "3"

services:
  ofelia:
    image: mcuadros/ofelia:latest
    command: daemon --docker
    container_name: github-tools
    networks:
      - gitea
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    labels:
      - "ofelia.job-run.mirror.schedule=0 0 2 * * *"
      - "ofelia.job-run.mirror.network=gitea"
      - "ofelia.job-run.mirror.image=ghcr.io/brighteyed/github-tools"
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
