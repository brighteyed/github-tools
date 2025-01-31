#!/usr/bin/env python

from github import Github
import requests
import json
import sys
import os

# Gitea API URL
GITEA_URL = f"{os.environ['GITEA_URL']}/api/v1"

# Set up Gitea session
session = requests.Session()
session.headers.update({
    "Authorization": f"token {os.environ['GITEA_TOKEN']}",
    "Content-type": "application/json"
})

# Get Gitea user details
resp = session.get(f"{GITEA_URL}/user")
if resp.status_code != 200:
    print("Cannot get Gitea user details", file=sys.stderr)
    exit(1)

gitea_user = json.loads(resp.text)
gitea_uid = gitea_user["id"]  # User ID for personal repositories

# GitHub API client
GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
gh = Github(GITHUB_TOKEN)

# Map GitHub organizations to Gitea organizations
ORG_MAPPING = json.loads(os.environ.get("ORG_MAPPING", "{}"))

# Function to get or create a Gitea organization
def get_or_create_gitea_org(org_name):
    # Check if the organization exists in Gitea
    resp = session.get(f"{GITEA_URL}/orgs/{org_name}")
    if resp.status_code == 200:
        return json.loads(resp.text)["id"]  # Return existing organization ID

    # If the organization doesn't exist, create it
    org_data = {
        "username": org_name,
        "visibility": "public"  # or "private" if needed
    }
    resp = session.post(f"{GITEA_URL}/orgs", data=json.dumps(org_data))
    if resp.status_code != 201:
        print(f"Failed to create Gitea organization {org_name}: {resp.text}", file=sys.stderr)
        exit(1)

    return json.loads(resp.text)["id"]  # Return new organization ID

# Iterate through GitHub repositories
for repo in gh.get_user().get_repos():
    if repo.fork:
        continue

    # Determine the owner type and map to Gitea
    if repo.owner.type == "User":
        # Personal repository: mirror to personal Gitea account
        uid = gitea_uid
    elif repo.owner.type == "Organization" and repo.owner.login in ORG_MAPPING:
        # Organizational repository: mirror to corresponding Gitea organization
        org_name = ORG_MAPPING[repo.owner.login]
        uid = get_or_create_gitea_org(org_name)
    else:
        # Skip repositories from other organizations
        print(f"Skipping repository {repo.full_name} (owned by {repo.owner.login})")
        continue

    # Prepare migration data
    m = {
        "repo_name": "/".join(repo.full_name.split("/")[1:]),
        "description": repo.description or "",
        "clone_addr": repo.clone_url,
        "mirror": True,
        "private": False,
        "uid": uid,
    }

    if repo.private:
        # Add credentials to the clone URL for private repositories
        m["clone_addr"] = repo.clone_url.replace("github.com", f"{os.environ['GITHUB_USERNAME']}:{GITHUB_TOKEN}@github.com")

    # Migrate the repository to Gitea
    jsonstring = json.dumps(m)
    r = session.post(f"{GITEA_URL}/repos/migrate", data=jsonstring)
    if r.status_code != 201:  # If not created
        if r.status_code == 409:  # Already exists
            print(f"Repository {repo.full_name} already exists in Gitea")
            continue
        print(f"Failed to migrate repository {repo.full_name}: {r.status_code}, {r.text}")