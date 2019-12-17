# github-tools

A collection of tools to automate some activities at Github:
  * A tool to mirror GitHub repositories to Gitea
  
## Mirror repositories
You can use docker to mirror Github repositories to Gitea:

    docker run --rm -e GITHUB_USENAME="changeme" \
                    -e GITHUB_TOKEN="changeme" \
                    -e GITEA_URL="changeme" \
                    -e GITEA_TOKEN="changeme" \
                    docker.pkg.github.com/brighteyed/github-tools/mirror_repositories:latest

### Environment variables
  * `GITHUB_USERNAME` – Github account name
  * `GITHUB_TOKEN` – Github token to access repositories
  * `GITEA_URL` – Gitea URL
  * `GITEA_TOKEN` – Gitea user token to access via API

