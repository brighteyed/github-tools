# github-tools

A collection of tools to automate some activities at Github:
  * [gh-mirror](#mirror-repositories): A tool to mirror Github repositories to Gitea
  * [gh-starred](#clone-starred-repositories): A tool to clone starred repositories with [x-motemen/ghq](https://github.com/x-motemen/ghq)
  
## Mirror repositories
You can use docker to mirror Github repositories to Gitea:
```
docker run --rm -e GITHUB_USENAME="changeme" \
                -e GITHUB_TOKEN="changeme" \
                -e GITEA_URL="changeme" \
                -e GITEA_TOKEN="changeme" \
                --name=gh-mirror \
                ghcr.io/brighteyed/gh-mirror:latest
```
To update Github token execute `update_token.py`:
```
docker run --rm -v "/path/to/gitea/data/git/repositories:/repositories" ghcr.io/brighteyed/gh-mirror:latest update_token.py --old-token="<old_token>" --new-token="<new_token>"
```

## Clone starred repositories

You can use docker to clone or update starred repositories:
```
docker run --rm -e GITHUB_TOKEN="changeme" \
            -v /path/to/dir:/ghq \
            --name=gh-starred \
            ghcr.io/brighteyed/gh-starred:latest
```

## Environment:
  * `GITHUB_USERNAME` – Github account name
  * `GITHUB_TOKEN` – Github token to access repositories
  * `GITEA_URL` – Gitea URL
  * `GITEA_TOKEN` – Gitea user token to access via API
