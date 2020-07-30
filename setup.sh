#!/usr/bin/env bash

set -e

cd "$(dirname "$0")"

venvname="testing-venv"

if [[ ! -d "$venvname" ]]; then
    virtualenv testing-venv
fi

bindirs=(
    Scripts # Windows in Git Bash
    bin # Linux
)

PS1="${PS1:-}" # Needed in safe bash modes

for bindir in "${bindirs[@]}"; do
    if [[ -d "$bindir" ]]; then
        . "$venvname/$bindir/activate"
        break
    fi
done

pip install -r requirements.txt
