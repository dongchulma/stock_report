#!/usr/bin/env python3
# Update one entry in _status.json on GitHub (creates the file if missing).
# Required env vars: GH_TOKEN, GH_REPO
# Usage: update_status.py <key> <date YYYY-MM-DD> <status>
import sys
import os
import json
import base64
import datetime
import urllib.request
import urllib.error


def main():
    token = os.environ["GH_TOKEN"]
    repo = os.environ["GH_REPO"]
    key, date, status = sys.argv[1], sys.argv[2], sys.argv[3]

    api = f"https://api.github.com/repos/{repo}/contents/_status.json"
    headers = {"Authorization": f"token {token}", "User-Agent": "stock_report-bot"}

    sha = None
    data = {}
    try:
        with urllib.request.urlopen(urllib.request.Request(api, headers=headers)) as resp:
            file_info = json.loads(resp.read().decode("utf-8"))
            sha = file_info["sha"]
            data = json.loads(base64.b64decode(file_info["content"]).decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code != 404:
            raise

    data[key] = {
        "date": date,
        "status": status,
        "updated_at": datetime.datetime.utcnow().isoformat() + "Z",
    }

    content_b64 = base64.b64encode(
        json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")
    ).decode("ascii")
    body = {"message": f"update status: {key}", "content": content_b64}
    if sha:
        body["sha"] = sha

    put_req = urllib.request.Request(
        api,
        data=json.dumps(body).encode("utf-8"),
        headers={**headers, "Content-Type": "application/json"},
        method="PUT",
    )
    with urllib.request.urlopen(put_req) as resp:
        json.loads(resp.read().decode("utf-8"))

    print(f"_status.json updated: {key} = {data[key]}")


if __name__ == "__main__":
    main()
