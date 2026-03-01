#!/usr/bin/env python3
"""
Repo stats + top contributors + contact email (fast, no cloning).

Input: Project data in CSV format. Use FIRST column as repo (owner/repo).

Outputs per repo:
- repo
- latest_sha
- age_years (repo age in years, based on created_at -> now)
- stars
- total_commits (TOTAL commits in repo, all time on default branch)         [GraphQL]
- avg_commits_last_6_months (commits since ~6 months ago / 6)              [GraphQL]
- top 2 developers by commit count among last 100 commits (>=2 commits)    [REST]
- contact email for each dev: GitHub profile email + best non-noreply commit author email [REST]

Logging:
- Prints progress for each repo and key steps
- Handles GitHub rate limit sleeping (REST + GraphQL)
- Flushes output per repo so results are written incrementally

Usage:
  export GITHUB_TOKEN=...
  python3 repo_activity_and_contributors.py --in success_projects.csv --out repo_stats.csv
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple

import requests

API = "https://api.github.com"
GQL = "https://api.github.com/graphql"


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


# ----------------------------
# Time helpers
# ----------------------------

def parse_github_time(s: str) -> datetime:
    # e.g., "2013-10-05T23:12:34Z"
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def repo_age_years(created_at_iso: str) -> float:
    created = parse_github_time(created_at_iso)
    now = datetime.now(timezone.utc)
    age_days = (now - created).total_seconds() / 86400.0
    return age_days / 365.25


def approx_months_ago_iso(months: float) -> str:
    """
    GitHub GraphQL expects GitTimestamp.
    We approximate months using average days/month = 365.25/12.
    """
    days = int(round(months * (365.25 / 12.0)))
    dt = datetime.now(timezone.utc) - timedelta(days=days)
    return dt.replace(microsecond=0).isoformat().replace("+00:00", "Z")


# ----------------------------
# GitHub REST helpers
# ----------------------------

def gh_get(session: requests.Session, url: str, params: Dict[str, Any] | None = None) -> requests.Response:
    """Low-level GET with rate-limit handling (returns Response)."""
    while True:
        r = session.get(url, params=params)

        if r.status_code == 403 and "rate limit" in r.text.lower():
            reset = int(r.headers.get("X-RateLimit-Reset", 0))
            remaining = r.headers.get("X-RateLimit-Remaining")
            wait = max(reset - int(time.time()) + 2, 1)
            log(f"[RATE LIMIT] remaining={remaining} reset={reset} -> sleeping {wait}s")
            time.sleep(wait)
            continue

        return r


def gh_json(session: requests.Session, url: str, params: Dict[str, Any] | None = None) -> Any:
    r = gh_get(session, url, params=params)
    if r.status_code >= 400:
        raise RuntimeError(f"GitHub API error {r.status_code} for {url}: {r.text[:500]}")
    return r.json()


def repo_info(session: requests.Session, repo: str) -> Dict[str, Any]:
    return gh_json(session, f"{API}/repos/{repo}")


def last_commits(session: requests.Session, repo: str, n: int) -> List[Dict[str, Any]]:
    data = gh_json(session, f"{API}/repos/{repo}/commits", params={"per_page": n})
    return data if isinstance(data, list) else []


def latest_commit_sha(session: requests.Session, repo: str) -> str:
    c = last_commits(session, repo, 1)
    return c[0].get("sha", "") if c else ""


def user_profile_email(session: requests.Session, login: str) -> str:
    u = gh_json(session, f"{API}/users/{login}")
    return (u.get("email") or "").strip()


def is_noreply(email: Optional[str]) -> bool:
    if not email:
        return True
    e = email.lower()
    return "noreply" in e or e.endswith("@users.noreply.github.com")


def extract_commit_identity(commit_obj: Dict[str, Any]) -> Tuple[Optional[str], Optional[str]]:
    login = None
    if isinstance(commit_obj.get("author"), dict):
        login = commit_obj["author"].get("login")

    commit = commit_obj.get("commit", {})
    author = commit.get("author", {}) if isinstance(commit, dict) else {}
    email = author.get("email") if isinstance(author, dict) else None
    return login, email


def top2_devs_from_last100(commits: List[Dict[str, Any]]) -> List[Tuple[str, int, Optional[str]]]:
    """
    Top 2 devs by commit count among last 100 commits, requiring >=2 commits.
    Returns [(login, count, best_non_noreply_commit_email), ...] (len 0..2)
    """
    counts: Dict[str, int] = {}
    best_email: Dict[str, str] = {}

    for c in commits:
        login, email = extract_commit_identity(c)
        if not login:
            continue
        counts[login] = counts.get(login, 0) + 1
        if login not in best_email and email and not is_noreply(email):
            best_email[login] = email

    items = [(login, cnt) for login, cnt in counts.items() if cnt >= 2]
    items.sort(key=lambda x: (-x[1], x[0]))

    out: List[Tuple[str, int, Optional[str]]] = []
    for login, cnt in items[:2]:
        out.append((login, cnt, best_email.get(login)))
    return out


# ----------------------------
# GitHub GraphQL helpers
# ----------------------------

def gql_request(session: requests.Session, query: str, variables: Dict[str, Any]) -> Any:
    """GraphQL POST with basic error handling + basic rate-limit handling."""
    while True:
        r = session.post(GQL, json={"query": query, "variables": variables})

        if r.status_code == 403 and "rate limit" in r.text.lower():
            reset = int(r.headers.get("X-RateLimit-Reset", 0))
            remaining = r.headers.get("X-RateLimit-Remaining")
            wait = max(reset - int(time.time()) + 2, 1)
            log(f"[GQL RATE LIMIT] remaining={remaining} reset={reset} -> sleeping {wait}s")
            time.sleep(wait)
            continue

        if r.status_code >= 400:
            raise RuntimeError(f"GitHub GraphQL error {r.status_code}: {r.text[:500]}")

        data = r.json()
        if "errors" in data and data["errors"]:
            raise RuntimeError(f"GitHub GraphQL errors: {str(data['errors'])[:500]}")
        return data.get("data")


def total_and_recent_commits_default_branch(session: requests.Session, repo: str, since_iso: str) -> Tuple[int, int]:
    """
    Returns:
      - total commits (all time) on default branch
      - commits since `since_iso` on default branch
    """
    if "/" not in repo:
        return 0, 0
    owner, name = repo.split("/", 1)

    query = """
    query($owner: String!, $name: String!, $since: GitTimestamp!) {
      repository(owner: $owner, name: $name) {
        defaultBranchRef {
          target {
            ... on Commit {
              total: history { totalCount }
              recent: history(since: $since) { totalCount }
            }
          }
        }
      }
    }
    """

    data = gql_request(session, query, {"owner": owner, "name": name, "since": since_iso})
    repo_data = (data or {}).get("repository") or {}
    dbr = repo_data.get("defaultBranchRef")
    if not dbr:
        return 0, 0
    target = dbr.get("target") or {}
    total = int(((target.get("total") or {}).get("totalCount")) or 0)
    recent = int(((target.get("recent") or {}).get("totalCount")) or 0)
    return total, recent


# ----------------------------
# Input reading
# ----------------------------

def read_repos_first_col(csv_path: str) -> List[str]:
    """
    Reads first column from CSV with or without header.
    Keeps unique repos in order. Skips obvious header tokens.
    """
    repos: List[str] = []
    seen = set()
    header_tokens = {"repo", "repository", "project"}

    with open(csv_path, "r", encoding="utf-8", errors="ignore", newline="") as f:
        for row in csv.reader(f):
            if not row:
                continue
            repo = (row[0] or "").strip()
            if not repo:
                continue
            if repo.lower() in header_tokens:
                continue
            if "/" not in repo:
                continue
            if repo not in seen:
                seen.add(repo)
                repos.append(repo)

    return repos


# ----------------------------
# Main
# ----------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True, help="Input CSV file (use first column as repo)")
    ap.add_argument("--out", required=True, help="Output CSV path")
    ap.add_argument("--sleep", type=float, default=0.0, help="Optional delay between repos (seconds)")
    args = ap.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        log("ERROR: Please set GITHUB_TOKEN in your environment.")
        return 2

    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "repo-activity-and-contributors",
    })

    repos = read_repos_first_col(args.inp)
    log(f"Loaded {len(repos)} repos from {args.inp}")

    since_6m = approx_months_ago_iso(6)

    fieldnames = [
        "repo",
        "latest_sha",
        "age_years",
        "stars",
        "total_commits",
        "avg_commits_last_6_months",
        "top1_login",
        "top1_commits_in_last100",
        "top1_profile_email",
        "top1_commit_email",
        "top2_login",
        "top2_commits_in_last100",
        "top2_profile_email",
        "top2_commit_email",
        "notes",
    ]

    with open(args.out, "w", newline="", encoding="utf-8") as out_f:
        w = csv.DictWriter(out_f, fieldnames=fieldnames)
        w.writeheader()
        out_f.flush()

        for idx, repo in enumerate(repos, 1):
            log(f"[{idx}/{len(repos)}] {repo}")
            row: Dict[str, Any] = {k: "" for k in fieldnames}
            row["repo"] = repo
            notes: List[str] = []

            try:
                log("  fetching repo info (stars, created_at)")
                info = repo_info(session, repo)
                row["stars"] = info.get("stargazers_count", "")
                created_at = info.get("created_at", "")
                row["age_years"] = f"{repo_age_years(created_at):.2f}" if created_at else ""

                log("  fetching latest SHA")
                row["latest_sha"] = latest_commit_sha(session, repo)

                log("  fetching total commits + recent commits (GraphQL)")
                total, recent6 = total_and_recent_commits_default_branch(session, repo, since_6m)
                row["total_commits"] = total
                row["avg_commits_last_6_months"] = f"{(recent6 / 6.0):.3f}"

                log("  fetching last 100 commits for top contributors")
                commits100 = last_commits(session, repo, 100)
                top2 = top2_devs_from_last100(commits100)

                if not top2:
                    notes.append("no_dev_with_>=2_commits_in_last100")
                else:
                    for k, (login, cnt, commit_email) in enumerate(top2, 1):
                        log(f"    top{k}: {login} ({cnt} commits) -> fetching profile email")
                        prof_email = user_profile_email(session, login)
                        row[f"top{k}_login"] = login
                        row[f"top{k}_commits_in_last100"] = cnt
                        row[f"top{k}_profile_email"] = prof_email
                        row[f"top{k}_commit_email"] = commit_email or ""

                row["notes"] = ";".join(notes)

            except Exception as e:
                row["notes"] = f"error:{type(e).__name__}:{str(e)[:200]}"
                log(f"  [ERROR] {row['notes']}")

            w.writerow(row)
            out_f.flush()

            if args.sleep:
                time.sleep(args.sleep)

            log(f"  done: wrote row for {repo}")

    log(f"Wrote output: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
