#!/usr/bin/env python

from github import Github
import requests
import json
import sys
import os

gitea_url = "http://localhost:3000/api/v1"
os.environ['NO_PROXY'] = 'localhost'

with open("./gitea_token") as gitea_token_file:
    gitea_token = gitea_token_file.read().strip()

session = requests.Session()
session.headers.update({
    "Authorization": f"token {gitea_token}",
    "Content-type": "application/json"
})

resp = session.get(f"{gitea_url}/user")
if resp.status_code != 200:
    print("Cannot get user details", file=sys.stderr)
    exit(1)

gitea_uid = json.loads(resp.text)["id"]

github_username = "brighteyed"
with open("./github_token") as github_token_file:
    github_token = github_token_file.read().strip()

gh = Github(github_token)

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
            m["clone_addr"] = repo.clone_url.replace("github.com", f"{github_username}:{github_token}@github.com")

        jsonstring = json.dumps(m)

        r = session.post(f"{gitea_url}/repos/migrate", data=jsonstring)
        if r.status_code != 201:            # if not created
            if r.status_code == 409:        # already exists
                continue
            print(r.status_code, r.text, jsonstring)
