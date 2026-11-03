#!/usr/bin/env python3
"""Refresh the GitHub profile with live public repository telemetry."""
from datetime import datetime, timezone
import json
import os
import urllib.request

REPOSITORIES = [
    ("LedgerTrace", "DT-09/LedgerTrace"),
    ("PaceLab", "DT-09/PaceLab"),
    ("Verity", "DT-09/Verity"),
    ("Aurelis Outcome Assurance", "DT-09/aurelis-aoa"),
    ("Aurelis Authority", "DT-09/Aurelis-Authority"),
    ("Aurelis ACI", "DT-09/aurelis-aci"),
    ("Aurelis AAI", "DT-09/aurelis-aai"),
    ("AI Assurance Infrastructure", "DT-09/ai-assurance-infrastructure"),
    ("DealTie / AI Acceptance Assurance", "DT-09/DealTie"),
    ("AUREL Desktop", "DT-09/AurelDesktop"),
    ("IL ROSSO", "DT-09/IL-ROSSO"),
    ("VentureLabs", "DT-09/VentureLabs"),
]
START = "<!-- PROFILE_PULSE:START -->"
END = "<!-- PROFILE_PULSE:END -->"


def github_get(path: str):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "DT-09-profile-pulse",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request("https://api.github.com" + path, headers=headers)
    with urllib.request.urlopen(request, timeout=25) as response:
        return json.loads(response.read().decode("utf-8"))


def main():
    rows = []
    for label, full_name in REPOSITORIES:
        repo = github_get(f"/repos/{full_name}")
        commits = github_get(f"/repos/{full_name}/commits?per_page=1")
        latest = commits[0] if commits else {}
        commit = latest.get("commit", {})
        author = commit.get("author") or commit.get("committer") or {}
        date = author.get("date", "")
        if date:
            parsed = datetime.fromisoformat(date.replace("Z", "+00:00"))
            date_label = parsed.astimezone(timezone.utc).strftime("%Y-%m-%d")
        else:
            date_label = "—"
        sha = latest.get("sha", "")[:7] or "—"
        commit_url = latest.get("html_url", repo["html_url"])
        message = (commit.get("message") or "No commit message").splitlines()[0]
        message = message.replace("|", "\\|").replace("<", "&lt;").replace(">", "&gt;")
        language = repo.get("language") or "—"
        rows.append(
            f"| [{label}]({repo['html_url']}) | {language} | "
            f"{repo.get('stargazers_count', 0)} | {repo.get('forks_count', 0)} | "
            f"{date_label} · [<code>{sha}</code>]({commit_url}) · {message} |"
        )

    refreshed = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    section = (
        f"_Refreshed: {refreshed}. Source: GitHub public repository and commit APIs._\n\n"
        "| Repository | Primary language | Stars | Forks | Latest commit |\n"
        "|---|---:|---:|---:|---|\n"
        + "\n".join(rows)
    )
    readme_path = os.path.join(os.path.dirname(__file__), "..", "README.md")
    with open(readme_path, "r", encoding="utf-8") as handle:
        content = handle.read()
    if START not in content or END not in content:
        raise RuntimeError("Profile pulse markers are missing from README.md")
    before, remainder = content.split(START, 1)
    _, after = remainder.split(END, 1)
    updated = before + START + "\n" + section + "\n" + END + after
    with open(readme_path, "w", encoding="utf-8") as handle:
        handle.write(updated)


if __name__ == "__main__":
    main()
