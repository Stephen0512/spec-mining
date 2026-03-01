#!/usr/bin/env python3
"""
Input: Project data in csv format. Use FIRST column as repo (owner/repo).

For each repo, output:
- stars
- commits per month for past 12 months (12 columns)
- average commits/month over last 6 months (from those 12 buckets)
- latest commit SHA (most recent on default branch, via /commits?per_page=1)
- top 2 developers by commit count among last 100 commits (>=2 commits)
- contact info for those devs: profile email/blog/twitter + best non-noreply commit email

Usage:
  export GITHUB_TOKEN=...
  python3 repo_participant_stats_from_csv.py --in success_projects.csv --out repo_stats.csv

Notes:
- No filtering is applied. You can filter later in the output CSV.
- Counts include whatever GitHub /commits returns for the default branch (includes merges/bots).
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


def month_start(dt: datetime) -> datetime:
    return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def add_months(dt: datetime, months: int) -> datetime:
    y = dt.year + (dt.month - 1 + months) // 12
    m = (dt.month - 1 + months) % 12 + 1
    return dt.replace(year=y, month=m, day=1)


def iso8601(dt: datetime) -> str:
    return dt.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def gh_request(session: requests.Session, url: str, params: Dict[str, Any] | None = None) -> Any:
    while True:
        r = session.get(url, params=params)
        if r.status_code == 403 and "rate limit" in r.text.lower():
            reset = r.headers.get("X-RateLimit-Reset")
            if reset:
                sleep_s = max(0, int(reset) - int(time.time()) + 2)
                print(f"[rate-limit] sleeping {sleep_s}s...", file=sys.stderr)
                time.sleep(sleep_s)
                continue
        if r.status_code >= 400:
            raise RuntimeError(f"GitHub API error {r.status_code} for {url}: {r.text[:2000]}")
        return r.json()


def is_noreply(email: Optional[str]) -> bool:
    if not email:
        return True
    e = email.lower()
    return "noreply" in e or e.endswith("@users.noreply.github.com")


def read_first_col_repos(csv_path: str) -> List[str]:
    """
    Reads first column from a CSV file (header or no header). Keeps non-empty unique repos in order.
    """
    repos: List[str] = []
    seen = set()

    with open(csv_path, "r", encoding="utf-8", errors="ignore", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            repo = (row[0] or "").strip()
            if not repo:
                continue
            # Skip common header tokens if present
            if repo.lower() in {"repo", "repository", "project"}:
                continue
            if repo not in seen:
                seen.add(repo)
                repos.append(repo)

    return repos


def repo_info(session: requests.Session, repo: str) -> Dict[str, Any]:
    return gh_request(session, f"{API}/repos/{repo}")


def count_commits_in_range(session: requests.Session, repo: str, since: datetime, until: datetime) -> int:
    url = f"{API}/repos/{repo}/commits"
    per_page = 100
    page = 1
    count = 0

    while True:
        data = gh_request(
            session, url,
            params={
                "since": iso8601(since),
                "until": iso8601(until),
                "per_page": per_page,
                "page": page,
            }
        )
        if not data:
            break
        count += len(data)
        if len(data) < per_page:
            break
        page += 1

    return count


def last_commits(session: requests.Session, repo: str, n: int) -> List[Dict[str, Any]]:
    data = gh_request(session, f"{API}/repos/{repo}/commits", params={"per_page": n})
    return data if isinstance(data, list) else []


def latest_commit_sha(session: requests.Session, repo: str) -> str:
    commits = last_commits(session, repo, 1)
    if not commits:
        return ""
    return commits[0].get("sha", "") or ""


def extract_commit_identity(commit_obj: Dict[str, Any]) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    login = None
    if isinstance(commit_obj.get("author"), dict):
        login = commit_obj["author"].get("login")

    commit = commit_obj.get("commit", {})
    author = commit.get("author", {}) if isinstance(commit, dict) else {}
    email = author.get("email") if isinstance(author, dict) else None
    name = author.get("name") if isinstance(author, dict) else None
    return login, email, name


def user_info(session: requests.Session, login: str) -> Dict[str, Any]:
    return gh_request(session, f"{API}/users/{login}")


def top2_devs_from_commits(commits: List[Dict[str, Any]]) -> List[Tuple[str, int, Optional[str]]]:
    """
    Returns up to 2 (login, count, best_non_noreply_commit_email) with count>=2.
    """
    counts: Dict[str, int] = {}
    best_email: Dict[str, str] = {}

    for c in commits:
        login, email, _name = extract_commit_identity(c)
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True, help="Input CSV file (use first column as repo)")
    ap.add_argument("--out", required=True, help="Output CSV path")
    ap.add_argument("--sleep", type=float, default=0.2, help="Small delay between repos")
    args = ap.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("ERROR: Please set GITHUB_TOKEN in your environment.", file=sys.stderr)
        return 2

    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "repo-participant-stats-script",
    })

    repos = read_first_col_repos(args.inp)

    now = datetime.now(timezone.utc)
    this_month = month_start(now)
    month_starts = [add_months(this_month, -11 + i) for i in range(12)]  # oldest -> newest
    month_ends = [add_months(ms, 1) for ms in month_starts]
    month_labels = [ms.strftime("%Y-%m") for ms in month_starts]

    fieldnames = [
        "repo",
        "stars",
        "latest_sha",
        *[f"commits_{m}" for m in month_labels],
        "avg_commits_last_6_months",
        "top1_login",
        "top1_commits_in_last100",
        "top1_profile_email",
        "top1_commit_email",
        "top1_blog",
        "top1_twitter",
        "top2_login",
        "top2_commits_in_last100",
        "top2_profile_email",
        "top2_commit_email",
        "top2_blog",
        "top2_twitter",
        "notes",
    ]

    with open(args.out, "w", newline="", encoding="utf-8") as out_f:
        w = csv.DictWriter(out_f, fieldnames=fieldnames)
        w.writeheader()

        for idx, repo in enumerate(repos, 1):
            row: Dict[str, Any] = {k: "" for k in fieldnames}
            row["repo"] = repo
            notes: List[str] = []

            try:
                info = repo_info(session, repo)
                row["stars"] = info.get("stargazers_count", "")

                row["latest_sha"] = latest_commit_sha(session, repo)

                monthly_counts: List[int] = []
                for ms, me, label in zip(month_starts, month_ends, month_labels):
                    c = count_commits_in_range(session, repo, ms, me)
                    row[f"commits_{label}"] = c
                    monthly_counts.append(c)

                last6 = monthly_counts[-6:]
                row["avg_commits_last_6_months"] = (sum(last6) / 6.0)

                commits100 = last_commits(session, repo, 100)
                top2 = top2_devs_from_commits(commits100)
                if not top2:
                    notes.append("no_dev_with_>=2_commits_in_last100")
                else:
                    for k, (login, cnt, commit_email) in enumerate(top2, 1):
                        u = user_info(session, login)
                        row[f"top{k}_login"] = login
                        row[f"top{k}_commits_in_last100"] = cnt
                        row[f"top{k}_profile_email"] = u.get("email", "") or ""
                        row[f"top{k}_commit_email"] = commit_email or ""
                        row[f"top{k}_blog"] = u.get("blog", "") or ""
                        row[f"top{k}_twitter"] = u.get("twitter_username", "") or ""

            except Exception as e:
                notes.append(f"error:{type(e).__name__}:{str(e)[:160]}")

            row["notes"] = ";".join(notes)
            w.writerow(row)

            if args.sleep:
                time.sleep(args.sleep)
            if idx % 50 == 0:
                print(f"Processed {idx}/{len(repos)} repos...", file=sys.stderr)

    print(f"Wrote: {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
