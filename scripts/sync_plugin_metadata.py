#!/usr/bin/env python3
"""
Sync each plugin's skills relation into the corresponding Port agentPlugin
entity, aggregated from the real symlinks under plugins/<name>/skills/.

Port's native GitHub Ocean integration can't aggregate a folder of symlinks
into a single relation, so this script fills that gap. It does not touch
any property the integration mapping already owns.

sync_skills() is currently disabled (see main()) now that skill entities no
longer carry lastEditor/lastEditedAt properties.

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


def upsert_entity(port_token, blueprint, identifier, properties=None, relations=None):
    encoded_identifier = urllib.parse.quote(identifier, safe="")
    url = f"{PORT_API_URL}/v1/blueprints/{blueprint}/entities/{encoded_identifier}"
    headers = {"Authorization": f"Bearer {port_token}"}
    body = {"properties": properties or {}}
    if relations is not None:
        body["relations"] = relations
    http_json("PATCH", url, headers=headers, body=body)


def get_plugin_skill_identifiers(repo, plugin_name):
    skills_dir = f"plugins/{plugin_name}/skills"
    if not os.path.isdir(skills_dir):
        return []
    identifiers = []
    for entry in sorted(os.listdir(skills_dir)):
        link_path = os.path.join(skills_dir, entry)
        if not os.path.islink(link_path):
            continue
        target = os.path.realpath(link_path)
        skill_path = os.path.join(os.path.relpath(target, os.getcwd()), "SKILL.md")
        identifiers.append(f"{repo}/{skill_path}")
    return identifiers


def sync_skills(port_token, repo, github_token):
    skill_paths = sorted(glob.glob("skills/**/SKILL.md", recursive=True))
    print(f"Found {len(skill_paths)} skill files")

    for path in skill_paths:
        last_editor, last_edited_at = get_last_commit_for_path(repo, path, github_token)
        identifier = f"{repo}/{path}"
        upsert_entity(
            port_token,
            "skill",
            identifier,
            properties={"lastEditor": last_editor, "lastEditedAt": last_edited_at},
        )
        print(f"  {identifier}: lastEditor={last_editor} lastEditedAt={last_edited_at}")


def sync_plugins(port_token, repo, github_token):
    plugin_dirs = sorted(
        {p.split("/")[1] for p in glob.glob("plugins/*/") if len(p.split("/")) > 1}
    )
    print(f"Found {len(plugin_dirs)} plugin folders")

    for plugin_name in plugin_dirs:
        skill_identifiers = get_plugin_skill_identifiers(repo, plugin_name)
        identifier = f"{repo}/{plugin_name}"
        upsert_entity(
            port_token,
            "agentPlugin",
            identifier,
            relations={"skills": skill_identifiers},
        )
        print(f"  {identifier}: skills={skill_identifiers}")


def main():
    client_id = os.environ["PORT_CLIENT_ID"]
    client_secret = os.environ["PORT_CLIENT_SECRET"]
    github_token = os.environ["GITHUB_TOKEN"]
    repo = os.environ["GITHUB_REPOSITORY"]

    port_token = get_port_token(client_id, client_secret)

    # sync_skills(port_token, repo, github_token)  # disabled: skill entities no longer carry lastEditor/lastEditedAt
    sync_plugins(port_token, repo, github_token)


if __name__ == "__main__":
    sys.exit(main())
