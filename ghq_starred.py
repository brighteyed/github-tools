#!/usr/bin/env python

import os
import subprocess

from github import Github


def starred():
    gh = Github(os.environ['GITHUB_TOKEN'])
    for star in gh.get_user().get_starred():
        try:
            subprocess.run(["ghq", "get", "--update", star.clone_url], check=True)
        except subprocess.CalledProcessError as e:
            print(f"ghq for {e.cmd} failed!")


if __name__ == '__main__':
    starred()
