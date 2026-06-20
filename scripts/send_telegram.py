#!/usr/bin/env python3
# Send a message to Telegram, splitting into chunks under the 4096-char limit.
# Required env vars: TG_BOT_TOKEN, TG_CHAT_ID
# Usage: send_telegram.py <message-file>   |   cat msg.txt | send_telegram.py -
import sys
import os
import json
import urllib.request


def main():
    token = os.environ["TG_BOT_TOKEN"]
    chat_id = os.environ["TG_CHAT_ID"]
    path = sys.argv[1] if len(sys.argv) > 1 else "-"
    text = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()

    chunk_size = 3500
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)] or [text]
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    for chunk in chunks:
        data = json.dumps({"chat_id": chat_id, "text": chunk}).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req) as resp:
            body = json.loads(resp.read().decode("utf-8"))
        if not body.get("ok"):
            print(f"Telegram send failed: {body}", file=sys.stderr)
            sys.exit(1)

    print(f"Telegram message sent ({len(text)} chars, {len(chunks)} part(s)).")


if __name__ == "__main__":
    main()
