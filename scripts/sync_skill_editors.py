#!/usr/bin/env python3
"""
Sync the last-editor and last-edited-at metadata for every skills/**/SKILL.md
file into the corresponding `skill` entity in Port.

Port's native GitHub Ocean integration has no per-file commit history, so this
script fills that specific gap using GitHub's "commits for a path" API. It
does not touch any property the integration mapping already owns.

Required environment variables:
  PORT_CLIENT_ID
  PORT_CLIENT_SECRET
  GITHUB_TOKEN        (provided automatically in GitHub Actions)
  GITHUB_REPOSITORY   (e.g. "revitalb-port/skills-registry-demo", provided
                       automatically in GitHub Actions)
"""

import glob
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
import json

PORT_API_URL = os.environ.get("PORT_API_URL", "https://api.port.io")
GITHUB_API_URL = "https://api.github.com"


def http_json(method, url, headers=None, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code} for {method} {url}: {e.read().decode()}", file=sys.stderr)
        raise


def get_port_token(client_id, client_secret):
    resp = http_json(
        "POST",
        f"{PORT_API_URL}/v1/auth/access_token",
        body={"clientId": client_id, "clientSecret": client_secret},
    )
    return resp["accessToken"]


def get_last_commit_for_path(repo, path, github_token):
    url = f"{GITHUB_API_URL}/repos/{repo}/commits?path={path}&per_page=1"
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json",
    }
    commits = http_json("GET", url, headers=headers)
    if not commits:
        return None, None
    commit = commits[0]
    login = (commit.get("author") or {}).get("login")
    name = (commit.get("commit", {}).get("author") or {}).get("name")
    date = commit.get("commit", {}).get("committer", {}).get("date") or commit.get(
        "commit", {}
    ).get("author", {}).get("date")
    return login or name, date


def upsert_skill_entity(port_token, identifier, last_editor, last_edited_at):
    encoded_identifier = urllib.parse.quote(identifier, safe="")
    url = f"{PORT_API_URL}/v1/blueprints/skill/entities/{encoded_identifier}"
    headers = {"Authorization": f"Bearer {port_token}"}
    body = {"properties": {"lastEditor": last_editor, "lastEditedAt": last_edited_at}}
    http_json("PATCH", url, headers=headers, body=body)


def main():
    client_id = os.environ["PORT_CLIENT_ID"]
    client_secret = os.environ["PORT_CLIENT_SECRET"]
    github_token = os.environ["GITHUB_TOKEN"]
    repo = os.environ["GITHUB_REPOSITORY"]

    port_token = get_port_token(client_id, client_secret)

    skill_paths = sorted(glob.glob("skills/**/SKILL.md", recursive=True))
    print(f"Found {len(skill_paths)} skill files")

    for path in skill_paths:
        last_editor, last_edited_at = get_last_commit_for_path(repo, path, github_token)
        identifier = f"{repo}/{path}"
        upsert_skill_entity(port_token, identifier, last_editor, last_edited_at)
        print(f"  {identifier}: lastEditor={last_editor} lastEditedAt={last_edited_at}")


if __name__ == "__main__":
    sys.exit(main())
