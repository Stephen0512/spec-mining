#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   ./run_original_and_collect_batch.sh final_projects.csv out_metrics.csv
#
# Input CSV format (one per line; header allowed):
#   owner/repo,sha
# Example:
#   0HugoHu/HugoHu-Python-PySpark,57848da
#
# Output CSV columns:
#   project,owner,repo,sha,url,sloc,stars,age_years,commit_count,stmt_cov_pct,branch_cov_pct,notes
#
# Extra per-project requirements (optional):
#   Place next to this script:
#     ./requirements/<OWNER>-<REPO>_<SHA>/requirements.txt
#
# Notes:
# - Runs repos one-by-one, cleans each repo directory afterward (keeps output CSV).
# - Saves per-repo artifacts into a zip:
#     <OWNER>-<REPO>_Original.zip
#   containing:
#     - <REPO>_Output.txt
#     - coverage.xml (if generated)
#     - coverage_run.log
#
# Env knobs:
#   WORKDIR=./_work
#   TIMEOUT_SEC=1500
#   EXTRA_REQ_ROOT=/path/to/requirements (default <script_dir>/requirements)

INPUT_CSV="${1:-final_projects.csv}"
OUT_CSV="${2:-collected_missing_metrics.csv}"

WORKDIR="${WORKDIR:-./_work}"
TIMEOUT_SEC="${TIMEOUT_SEC:-1500}"

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
EXTRA_REQ_ROOT="${EXTRA_REQ_ROOT:-${SCRIPT_DIR}/requirements}"

mkdir -p "$WORKDIR"

# ---------------- Helpers ----------------
have_cmd() { command -v "$1" >/dev/null 2>&1; }

ensure_cloc() {
  if have_cmd cloc; then return; fi
  mkdir -p "${SCRIPT_DIR}/_bin"
  local cloc_path="${SCRIPT_DIR}/_bin/cloc"
  if [ ! -f "$cloc_path" ]; then
    curl -sSL -o "$cloc_path" "https://raw.githubusercontent.com/AlDanial/cloc/master/cloc"
    chmod +x "$cloc_path"
  fi
  export PATH="${SCRIPT_DIR}/_bin:$PATH"
}

compute_sloc() {
  local dir="$1"
  ensure_cloc
  if ! have_cmd cloc; then echo ""; return; fi
  local out
  out="$(cloc --json --quiet "$dir" 2>/dev/null || true)"
  if [ -z "$out" ]; then echo ""; return; fi
  python3 - <<'PY' "$out"
import sys, json
try:
    d = json.loads(sys.argv[1])
    v = d.get("SUM", {}).get("code", 0)
    print(int(v) if v else "")
except Exception:
    print("")
PY
}

compute_commit_count() {
  local dir="$1"
  (cd "$dir" && git rev-list --count HEAD 2>/dev/null) || echo ""
}

fetch_repo_json() {
  local owner="$1"
  local repo="$2"
  if have_cmd gh; then
    gh api "repos/${owner}/${repo}" 2>/dev/null || true
  else
    curl -sS -H "Accept: application/vnd.github+json" \
      "https://api.github.com/repos/${owner}/${repo}" || true
  fi
}

extract_stars_created() {
  # prints: "<stars> <created_at>"
  local json="$1"
  python3 - <<'PY' "$json"
import sys, json
s = sys.argv[1]
try:
    d = json.loads(s)
    stars = d.get("stargazers_count", "")
    created = d.get("created_at", "")
    stars = "" if stars is None else str(stars)
    created = "" if created is None else str(created)
    print(stars, created)
except Exception:
    print("", "")
PY
}

age_years_from_created_at() {
  local created_at="$1"
  if [ -z "$created_at" ]; then echo ""; return; fi
  python3 - <<'PY' "$created_at"
import sys, datetime
s = sys.argv[1].strip()
try:
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    dt = datetime.datetime.fromisoformat(s)
    now = datetime.datetime.now(datetime.timezone.utc)
    age = (now - dt).total_seconds() / (365.25*24*3600)
    print(f"{age:.1f}")
except Exception:
    print("")
PY
}

parse_coverage_xml_rates() {
  local xml_path="$1"
  python3 - <<'PY' "$xml_path"
import sys, xml.etree.ElementTree as ET
p = sys.argv[1]
try:
    root = ET.parse(p).getroot()
    lr = root.attrib.get("line-rate")
    br = root.attrib.get("branch-rate")
    def pct(x):
        if not x: return ""
        try: return f"{float(x)*100:.1f}"
        except Exception: return ""
    print(pct(lr), pct(br))
except Exception:
    print("", "")
PY
}

write_row() {
  # Args: project owner repo sha url sloc stars age_years commit_count stmt_cov branch_cov notes
  local project="$1" owner="$2" repo="$3" sha="$4" url="$5" sloc="$6" stars="$7" age="$8" commits="$9" stmt="${10}" br="${11}" notes="${12}"
  # keep simple CSV (no commas expected in these fields)
  echo "${project},${owner},${repo},${sha},${url},${sloc},${stars},${age},${commits},${stmt},${br},${notes}" >> "$OUT_CSV"
}

# ---------------- Output header ----------------
echo "project,owner,repo,sha,url,sloc,stars,age_years,commit_count,stmt_cov_pct,branch_cov_pct,notes" > "$OUT_CSV"

# ---------------- Main loop ----------------
# Read input CSV. Skip header lines.
tail -n +1 "$INPUT_CSV" | while IFS= read -r line || [ -n "$line" ]; do
  line="${line#"${line%%[![:space:]]*}"}"
  line="${line%"${line##*[![:space:]]}"}"
  [ -z "$line" ] && continue

  if echo "$line" | grep -qiE '^(project|owner|repo|sha)'; then
    continue
  fi

  owner_repo="${line%%,*}"
  sha="${line#*,}"
  if [ "$owner_repo" = "$line" ]; then
    # no comma => bad row
    continue
  fi

  owner_repo="${owner_repo// /}"
  sha="${sha// /}"

  owner="${owner_repo%%/*}"
  repo="${owner_repo##*/}"

  project="${owner}-${repo}"
  url="https://github.com/${owner}/${repo}.git"

  echo "===== ${owner_repo} @ ${sha} ====="

  # Workspace per project
  CLONE_DIR="${WORKDIR}/${project}_Original"
  REPO_DIR="${CLONE_DIR}/${repo}"

  rm -rf "$CLONE_DIR" || true
  mkdir -p "$CLONE_DIR"

  notes=""

  # Clone
  if ! git clone "$url" "$REPO_DIR" >/dev/null 2>&1; then
    notes="clone_failed"
    write_row "$project" "$owner" "$repo" "$sha" "$url" "" "" "" "" "" "" "$notes"
    rm -rf "$CLONE_DIR" || true
    continue
  fi

  # Checkout
  if ! (cd "$REPO_DIR" && git checkout -q "$sha" >/dev/null 2>&1); then
    notes="checkout_failed"
    write_row "$project" "$owner" "$repo" "$sha" "$url" "" "" "" "" "" "" "$notes"
    rm -rf "$CLONE_DIR" || true
    continue
  fi

  # Repo-level metrics
  sloc="$(compute_sloc "$REPO_DIR")"
  commit_count="$(compute_commit_count "$REPO_DIR")"

  repo_json="$(fetch_repo_json "$owner" "$repo")"
  read -r stars created_at < <(extract_stars_created "$repo_json")
  age_years="$(age_years_from_created_at "$created_at")"

  # Create venv + run tests
  (
    cd "$REPO_DIR"

    python3 -m venv venv
    # shellcheck disable=SC1090
    source venv/bin/activate

    # Install root *.txt (best-effort)
    for file in *.txt; do
      if [ -f "$file" ]; then
        pip install -r "$file" >/dev/null 2>&1 || true
      fi
    done

    # Extra requirements: ./requirements/<OWNER>-<REPO>_<SHA>/requirements.txt
    extra_req="${EXTRA_REQ_ROOT}/${owner}-${repo}_${sha}/requirements.txt"
    if [ -f "$extra_req" ]; then
      pip install -r "$extra_req" >/dev/null 2>&1 || true
    fi

    # Install package with test deps
    if [ -f myInstall.sh ]; then
      bash ./myInstall.sh >/dev/null 2>&1 || true
    else
      pip install .[dev,test,tests,testing] >/dev/null 2>&1 || true
    fi

    pip install pytest pandas coverage >/dev/null 2>&1 || true

    # Run original tests (capture output)
    timeout -k 9 "$TIMEOUT_SEC" pytest --continue-on-collection-errors &> "${repo}_Output.txt"
    exit_code=$?

    # Coverage run (best-effort; do not affect exit_code)
    COV_LOG="${PWD}/coverage_run.log"
    : > "$COV_LOG" || true
    rm -f .coverage coverage.xml || true
    timeout -k 9 "$TIMEOUT_SEC" coverage run --branch -m pytest --continue-on-collection-errors -q >>"$COV_LOG" 2>&1 || true
    coverage xml -o coverage.xml >>"$COV_LOG" 2>&1 || true

    deactivate || true
    rm -rf venv || true

    exit "$exit_code"
  )
  exit_code=$?

  # Parse coverage
  stmt_cov=""
  branch_cov=""
  if [ -f "${REPO_DIR}/coverage.xml" ]; then
    read -r stmt_cov branch_cov < <(parse_coverage_xml_rates "${REPO_DIR}/coverage.xml")
  else
    # Let notes reflect missing coverage if you want:
    # notes="${notes:+$notes; }coverage_missing"
    :
  fi

  # If timed out, record and keep going
  if [ $exit_code -eq 124 ] || [ $exit_code -eq 137 ]; then
    notes="${notes:+$notes; }timeout"
  elif [ $exit_code -ne 0 ]; then
    notes="${notes:+$notes; }tests_failed"
  fi

  # Save artifacts into zip next to WORKDIR (optional)
  zip_name="${WORKDIR}/${project}_Original.zip"
  # Ensure WORKDIR exists and use absolute path for zip
  mkdir -p "$WORKDIR" || true
  zip_name_abs="$(cd "$WORKDIR" && pwd)/${project}_Original.zip"
  (
    cd "$CLONE_DIR"
    zip -qr "$zip_name_abs" "./${repo}/${repo}_Output.txt" "./${repo}/coverage.xml" "./${repo}/coverage_run.log" 2>/dev/null || true
  )

  # Write output row
  write_row "$project" "$owner" "$repo" "$sha" "$url" "$sloc" "$stars" "$age_years" "$commit_count" "$stmt_cov" "$branch_cov" "$notes"

  # Cleanup
  rm -rf "$CLONE_DIR" || true
done

echo "Done. Wrote: $OUT_CSV"