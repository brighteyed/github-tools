# Github-tools

A collection of tools to automate some activities at Github:
  * [gh-mirror](#mirror-repositories): A tool to mirror Github repositories to Gitea
  * [gh-starred](#clone-starred-repositories): A tool to clone starred repositories with [x-motemen/ghq](https://github.com/x-motemen/ghq)
  
## Mirror repositories
Automates the process of mirroring repositories from Github to Gitea. It supports mirroring both personal repositories and repositories belonging to specific organizations

### Key Features:
- **Personal repositories**: Automatically mirrors personal Github repositories to your Gitea account.
- **Organizational repositories**: Mirrors repositories from specified Github organizations to corresponding Gitea organizations.
- **No duplication**: Skips repositories that already exist in Gitea, avoiding duplicate migrations.

### Usage:
To mirror repositories, run the following Docker command:
```
docker run --rm \
  -e GITHUB_USERNAME="changeme" \
  -e GITHUB_TOKEN="changeme" \
  -e GITEA_URL="changeme" \
  -e GITEA_TOKEN="changeme" \
  -e ORG_MAPPING='{"abc-org": "abc-org", "other-org": "other-org"}' \
  --name=gh-mirror \
  ghcr.io/brighteyed/gh-mirror:latest
```

#### Notes:
- The tool will mirror personal repositories to your Gitea account and organizational repositories to the specified Gitea organizations.

- If a Gitea organization does not exist, it will be created automatically.

- Repositories that already exist in Gitea will be skipped.

### Updating Github Token in Mirrored Repositories
If your Github token changes, you can update it in all mirrored repositories using the `update_token.py` script. Run the following Docker command:
```
docker run --rm -v "/path/to/gitea/data/git/repositories:/repositories" ghcr.io/brighteyed/gh-mirror:latest update_token.py --old-token="<old_token>" --new-token="<new_token>"
```

#### Notes:
- Replace `/path/to/gitea/data/git/repositories` with the actual path to your Gitea repositories directory.

## Clone starred repositories

You can use docker to clone or update starred repositories:
```
docker run --rm -e GITHUB_TOKEN="changeme" \
            -v /path/to/dir:/ghq \
            --name=gh-starred \
            ghcr.io/brighteyed/gh-starred:latest
```

## Environment:
  * `GITHUB_USERNAME` – Github username
  * `GITHUB_TOKEN` – Github personal access token
  * `GITEA_URL` – Gitea URL
  * `GITEA_TOKEN` – Gitea personal access token
  * `ORG_MAPPING` – JSON string mapping Github organizations to Gitea organizations
