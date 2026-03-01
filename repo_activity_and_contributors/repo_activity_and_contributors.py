#!/usr/bin/env python3
"""
Repo stats + top contributors + contact email.

Input: Project data in CSV format. Use FIRST column as repo (owner/repo).

Outputs per repo:
- repo
- latest_sha (GitHub API)
- age_years (GitHub API created_at -> now)
- commits (TOTAL commits in repo, all time on default branch)  [GraphQL]
- stars (GitHub API)
- commits per month for past 12 months (12 columns, YYYY-MM)  [LOCAL GIT (clone)]
- average commits/month over last 6 months                    [LOCAL GIT (clone)]
- top 2 developers by commit count among last 100 commits (>=2 commits) [GitHub API]
- contact email for each dev: GitHub profile email + best non-noreply commit author email [GitHub API]

Change requested:
- Replace stats collection (/stats/commit_activity) with local git partial-clone + git log, then delete.

Usage:
  export GITHUB_TOKEN=...
  python3 repo_activity_and_contributors.py --in success_projects.csv --out repo_stats.csv

Notes:
- Local git method uses: git clone --filter=blob:none --no-checkout
- Requires `git` installed and reachable in PATH.
"""

from __future__ import annotations

import argparse
import csv
import os
import shutil
import subprocess
import sys
import tempfile
import time
from collections import Counter
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

import requests

API = "https://api.github.com"
GQL = "https://api.github.com/graphql"


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


# ----------------------------
# Time helpers
# ----------------------------

def month_start(dt: datetime) -> datetime:
    return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def add_months(dt: datetime, months: int) -> datetime:
    y = dt.year + (dt.month - 1 + months) // 12
    m = (dt.month - 1 + months) % 12 + 1
    return dt.replace(year=y, month=m, day=1)


def month_label(dt: datetime) -> str:
    return dt.strftime("%Y-%m")


def parse_github_time(s: str) -> datetime:
    # e.g., "2013-10-05T23:12:34Z"
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def repo_age_years(created_at_iso: str) -> float:
    created = parse_github_time(created_at_iso)
    now = datetime.now(timezone.utc)
    age_days = (now - created).total_seconds() / 86400.0
    return age_days / 365.25


def last_12_month_labels(now_utc: datetime) -> List[str]:
    this_month = month_start(now_utc)
    month_starts = [add_months(this_month, -11 + i) for i in range(12)]
    return [month_label(m) for m in month_starts]


# ----------------------------
# GitHub REST / GraphQL helpers
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


def read_repos_first_col(csv_path: str) -> List[str]:
    """Reads first column from CSV with or without header. Keeps unique repos in order."""
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


def repo_info(session: requests.Session, repo: str) -> Dict[str, Any]:
    return gh_json(session, f"{API}/repos/{repo}")


def last_commits(session: requests.Session, repo: str, n: int) -> List[Dict[str, Any]]:
    data = gh_json(session, f"{API}/repos/{repo}/commits", params={"per_page": n})
    return data if isinstance(data, list) else []


def latest_commit_sha(session: requests.Session, repo: str) -> str:
    c = last_commits(session, repo, 1)
    return c[0].get("sha", "") if c else ""


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


def user_profile_email(session: requests.Session, login: str) -> str:
    u = gh_json(session, f"{API}/users/{login}")
    return (u.get("email") or "").strip()


def total_commits_default_branch(session: requests.Session, repo: str) -> int:
    """Exact total commit count (all time) on the repo's default branch, via GraphQL."""
    if "/" not in repo:
        return 0
    owner, name = repo.split("/", 1)

    query = """
    query($owner: String!, $name: String!) {
      repository(owner: $owner, name: $name) {
        defaultBranchRef {
          target {
            ... on Commit {
              history {
                totalCount
              }
            }
          }
        }
      }
    }
    """

    data = gql_request(session, query, {"owner": owner, "name": name})
    repo_data = (data or {}).get("repository") or {}
    dbr = repo_data.get("defaultBranchRef")
    if not dbr:
        return 0
    target = dbr.get("target") or {}
    history = target.get("history") or {}
    return int(history.get("totalCount", 0) or 0)


# ----------------------------
# Local git stats (clone -> log -> delete)
# ----------------------------

def run_cmd(cmd: List[str], cwd: Optional[str] = None) -> str:
    return subprocess.check_output(cmd, cwd=cwd, text=True, stderr=subprocess.STDOUT).strip()


def git_monthly_stats(repo: str, labels: List[str]) -> Tuple[List[int], float]:
    """
    Returns:
      - monthly_counts aligned to labels (last 12 months)
      - avg6 (avg commits/month over last 6 months)
    Strategy:
      - partial clone with blobs filtered and no checkout
      - git log since 12 months ago, date formatted as YYYY-MM, count occurrences
      - delete repo directory
    """
    repo_url = f"https://github.com/{repo}.git"
    tmpdir = tempfile.mkdtemp(prefix="repo_stats_")
    try:
        # Partial clone, no checkout (minimize blobs)
        run_cmd(["git", "clone", "--filter=blob:none", "--no-checkout", repo_url, tmpdir])

        out = run_cmd(
            ["git", "log", "--since=12 months ago", "--pretty=format:%ad", "--date=format:%Y-%m"],
            cwd=tmpdir,
        )
        months = out.splitlines() if out else []
        c = Counter(months)

        monthly_counts = [int(c.get(lbl, 0)) for lbl in labels]
        avg6 = sum(monthly_counts[-6:]) / 6.0
        return monthly_counts, avg6

    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


# ----------------------------
# Main
# ----------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True, help="Input CSV file (use first column as repo)")
    ap.add_argument("--out", required=True, help="Output CSV path")
    ap.add_argument("--sleep", type=float, default=0.2, help="Small delay between repos")
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

    now = datetime.now(timezone.utc)
    labels = last_12_month_labels(now)

    fieldnames = [
        "repo",
        "latest_sha",
        "age_years",
        "commits",
        "stars",
        *[f"commits_{m}" for m in labels],
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

                log("  fetching TOTAL commits via GraphQL (default branch)")
                row["commits"] = total_commits_default_branch(session, repo)

                log("  cloning repo (partial) and computing monthly stats, then deleting")
                monthly_counts, avg6 = git_monthly_stats(repo, labels)
                for m, c in zip(labels, monthly_counts):
                    row[f"commits_{m}"] = c
                row["avg_commits_last_6_months"] = f"{avg6:.3f}"

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

            except subprocess.CalledProcessError as e:
                msg = (e.output or "").splitlines()[-1] if getattr(e, "output", None) else str(e)
                row["notes"] = f"git_error:{msg[:200]}"
                log(f"  [ERROR] {row['notes']}")
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
