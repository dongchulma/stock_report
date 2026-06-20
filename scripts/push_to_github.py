#!/usr/bin/env python3
# Create or update a file in a GitHub repo via the Contents API.
# Required env vars: GH_TOKEN, GH_REPO (e.g. "owner/repo")
# Usage: push_to_github.py <local_file> <repo_path> [commit_message]
import sys
import os
import json
import base64
import urllib.request
import urllib.error


def main():
    token = os.environ["GH_TOKEN"]
    repo = os.environ["GH_REPO"]
    local_file, repo_path = sys.argv[1], sys.argv[2]
    message = sys.argv[3] if len(sys.argv) > 3 else f"update {repo_path}"

    api = f"https://api.github.com/repos/{repo}/contents/{repo_path}"
    headers = {"Authorization": f"token {token}", "User-Agent": "stock_report-bot"}

    sha = None
    try:
        with urllib.request.urlopen(urllib.request.Request(api, headers=headers)) as resp:
            sha = json.loads(resp.read().decode("utf-8")).get("sha")
    except urllib.error.HTTPError as e:
        if e.code != 404:
            raise

    with open(local_file, "rb") as f:
        content_b64 = base64.b64encode(f.read()).decode("ascii")

    body = {"message": message, "content": content_b64}
    if sha:
        body["sha"] = sha

    put_req = urllib.request.Request(
        api,
        data=json.dumps(body).encode("utf-8"),
        headers={**headers, "Content-Type": "application/json"},
        method="PUT",
    )
    with urllib.request.urlopen(put_req) as resp:
        result = json.loads(resp.read().decode("utf-8"))

    print(f"Pushed {local_file} -> {repo}/{repo_path}: {result['content']['html_url']}")


if __name__ == "__main__":
    main()
