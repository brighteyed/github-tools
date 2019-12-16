#!/usr/bin/env python

from github import Github
import requests
import json
import sys
import os


GITEA_URL = f"{os.environ['GITEA_URL']}/api/v1"

session = requests.Session()
session.headers.update({
    "Authorization": f"token {os.environ['GITEA_TOKEN']}",
    "Content-type": "application/json"
})

resp = session.get(f"{GITEA_URL}/user")
if resp.status_code != 200:
    print("Cannot get user details", file=sys.stderr)
    exit(1)

gitea_uid = json.loads(resp.text)["id"]

GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
gh = Github(GITHUB_TOKEN)

for repo in gh.get_user().get_repos():
    if not repo.fork:
        m = {
            "repo_name": "/".join(repo.full_name.split("/")[1:]),
            "description": repo.description or "",
            "clone_addr": repo.clone_url,
            "mirror": True,
            "private": False,
            "uid": gitea_uid,
        }

        if repo.private:
            m["clone_addr"] = repo.clone_url.replace("github.com", f"{os.environ['GITHUB_USERNAME']}:{GITHUB_TOKEN}@github.com")

        jsonstring = json.dumps(m)

        r = session.post(f"{GITEA_URL}/repos/migrate", data=jsonstring)
        if r.status_code != 201:            # if not created
            if r.status_code == 409:        # already exists
                continue
            print(r.status_code, r.text, jsonstring)
