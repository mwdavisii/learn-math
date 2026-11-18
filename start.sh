#!/usr/bin/env bash
# Start a study sitting: set up the venv if needed, show what's next, open Jupyter.
#   ./start.sh          status + launch Jupyter Lab
#   ./start.sh status   status only
set -euo pipefail
cd "$(dirname "$0")"

# --- venv (system python; the Nix python breaks numpy) ---
if [[ ! -x .venv/bin/python ]]; then
  echo "Creating .venv with /usr/bin/python3 ..."
  /usr/bin/python3 -m venv .venv
  .venv/bin/pip install -q -r requirements.txt
fi

# --- next unchecked item in progress.md ---
next=$(grep -m1 -E '^- \[ \] [0-9]+\.' progress.md || true)
echo
if [[ -z "$next" ]]; then
  echo "Nothing unchecked in progress.md. Done, or the next tier isn't written yet."
else
  id=$(sed -E 's/^- \[ \] ([0-9]+\.[0-9A-Z]+).*/\1/' <<<"$next")
  tier=${id%%.*}
  rest=${id#*.}
  dir=$(ls -d tier-"$tier"-*/ 2>/dev/null | head -1)
  if [[ "$rest" == CP ]]; then
    file="${dir}checkpoint.md"
  else
    num=$(printf '%02d' "${rest%[AB]}")
    file=$(ls "${dir}${num}"-*.md 2>/dev/null | head -1 || true)
  fi
  label=${next#- \[ \] }; echo "Next up:  ${label% — date:*}"
  [[ -n "${file:-}" ]] && echo "File:     $file"
  [[ "$rest" == *A ]] && echo "Half A:   read + key ideas + worked example"
  [[ "$rest" == *B ]] && echo "Half B:   problems (paper, then 🐍 in ${dir}notebooks/sessions.ipynb) + proof thread"
fi

stuck=$(sed -n '/^## Stuck/,/^## /p' progress.md | grep -E '^- ' || true)
[[ -n "$stuck" ]] && { echo; echo "Stuck list:"; echo "$stuck"; }

cat <<'EOF'

Claude:   run `claude` here and say "where was I?"
          check work with "check 0.3 problem 4" + paste/photo
Finish:   tick the box + date in progress.md
EOF

[[ "${1:-}" == status ]] && exit 0
echo
exec .venv/bin/jupyter lab
