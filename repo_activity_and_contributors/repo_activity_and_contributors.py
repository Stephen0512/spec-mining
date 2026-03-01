#!/usr/bin/env python3
"""
Fast repo stats + top contributors + contact email (profile + non-noreply commit email)

Input: Project data in csv format. Use FIRST column as repo (owner/repo).

Outputs per repo:
- repo
- latest_sha
- commits (total in last year)
- stars
- commits per month for past 12 months (12 columns, YYYY-MM)
  (computed from /stats/commit_activity weekly totals; fast)
- average commits/month over last 6 months
- top 2 developers by commit count among last 100 commits (>=2 commits)
- contact email for each dev: GitHub profile email + best non-noreply commit author email

Logging:
- Prints progress for each repo and key steps
- Handles GitHub rate limit sleeping
- Handles stats endpoint 202 Accepted by retrying
- Flushes output per repo so results are written incrementally

Usage:
  export GITHUB_TOKEN=...
  python3 repo_activity_and_contributors.py --in success_projects.csv --out repo_stats.csv

Notes:
- /stats/commit_activity attributes each week’s total to the month containing that week’s start date.
  This is fast and consistent; if you want exact splitting of weeks across month boundaries, say so.
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

import requests

API = "https://api.github.com"


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


def month_start(dt: datetime) -> datetime:
    return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def add_months(dt: datetime, months: int) -> datetime:
    y = dt.year + (dt.month - 1 + months) // 12
    m = (dt.month - 1 + months) % 12 + 1
    return dt.replace(year=y, month=m, day=1)


def month_label(dt: datetime) -> str:
    return dt.strftime("%Y-%m")


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
    """JSON GET with error handling + rate-limit handling."""
    r = gh_get(session, url, params=params)
    if r.status_code >= 400:
        raise RuntimeError(f"GitHub API error {r.status_code} for {url}: {r.text[:500]}")
    return r.json()


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
            # basic sanity: looks like owner/repo
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


def user_profile_email(session: requests.Session, login: str) -> str:
    u = gh_json(session, f"{API}/users/{login}")
    return (u.get("email") or "").strip()


def get_commit_activity_weeks(session: requests.Session, repo: str, max_retries: int = 10) -> List[Dict[str, Any]]:
    """
    GET /stats/commit_activity
    May return 202 while GitHub prepares stats. Retry with backoff.
    """
    url = f"{API}/repos/{repo}/stats/commit_activity"
    for i in range(max_retries):
        r = gh_get(session, url)

        if r.status_code == 202:
            sleep_s = min(30.0, 2.0 * (i + 1))
            log(f"  [stats] 202 Accepted (generating) -> retry in {sleep_s:.1f}s")
            time.sleep(sleep_s)
            continue

        if r.status_code >= 400:
            raise RuntimeError(f"GitHub stats error {r.status_code} for {repo}: {r.text[:300]}")

        data = r.json()
        if isinstance(data, list):
            return data
        return []

    raise RuntimeError(f"stats/commit_activity not ready after {max_retries} retries for {repo}")


def monthly_counts_from_weeks(weeks: List[Dict[str, Any]], month_labels: List[str]) -> Tuple[List[int], int]:
    """
    weeks: list of 52 objects: {"total": int, "week": unix_ts, "days":[...]}
    We attribute each week's 'total' to the month containing the week start date.
    Also returns total commits (sum of all weeks).
    """
    totals = {m: 0 for m in month_labels}
    total_commits = 0
    for w in weeks:
        ts = w.get("week")
        total = int(w.get("total", 0))
        total_commits += total
        if ts is None:
            continue
        dt = datetime.fromtimestamp(int(ts), tz=timezone.utc)
        mk = month_label(dt)
        if mk in totals:
            totals[mk] += total
    return [totals[m] for m in month_labels], total_commits


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
        "User-Agent": "sample-repos-and-participants",
    })

    repos = read_repos_first_col(args.inp)
    log(f"Loaded {len(repos)} repos from {args.inp}")

    now = datetime.now(timezone.utc)
    this_month = month_start(now)

    # 12 buckets: oldest -> newest (includes current month-to-date as newest bucket)
    month_starts = [add_months(this_month, -11 + i) for i in range(12)]
    labels = [month_label(m) for m in month_starts]

    fieldnames = [
        "repo",
        "latest_sha",
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
                log("  fetching repo info (stars)")
                info = repo_info(session, repo)
                row["stars"] = info.get("stargazers_count", "")

                log("  fetching latest SHA")
                row["latest_sha"] = latest_commit_sha(session, repo)

                log("  fetching commit_activity stats (fast)")
                weeks = get_commit_activity_weeks(session, repo)
                counts, total_commits = monthly_counts_from_weeks(weeks, labels)
                row["commits"] = total_commits
                for m, c in zip(labels, counts):
                    row[f"commits_{m}"] = c
                row["avg_commits_last_6_months"] = sum(counts[-6:]) / 6.0

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
            out_f.flush()  # make sure results are written incrementally

            if args.sleep:
                time.sleep(args.sleep)

            log(f"  done: wrote row for {repo}")

    log(f"Wrote output: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
