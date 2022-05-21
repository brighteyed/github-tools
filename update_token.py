#!/usr/bin/env python

import glob
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Replace tokens')
    parser.add_argument("--old-token", help="Old token", required=True)
    parser.add_argument("--new-token", help="New token", required=True)
    args = parser.parse_args()

    for path in glob.glob("/repositories/*/*.git/config", recursive=True):
        repo_name = path.replace("/repositories/", "").replace(".git/config", "")
        print(f"Updating: {repo_name}")

        with open(path, 'r', encoding="utf-8") as file:
            filedata = file.read()

        filedata = filedata.replace(f"{args.old_token}", f"{args.new_token}")

        with open(path, 'w', encoding="utf-8") as file:
            file.write(filedata)
