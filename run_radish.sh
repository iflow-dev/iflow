#!/usr/bin/env bash
set -euo pipefail

# Resolve repo root (directory containing this script)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Prepend tests directory to PYTHONPATH
export PYTHONPATH="${SCRIPT_DIR}/tests${PYTHONPATH+:${PYTHONPATH}}"

# If no basedir (-b/--basedir) was provided, add "-b tests"
ADD_BASEDIR=true
for arg in "$@"; do
    if [[ "$arg" == "-b" || "$arg" == "--basedir" ]]; then
        ADD_BASEDIR=false
        break
    fi
done

if $ADD_BASEDIR; then
    exec radish "$@" -b "${SCRIPT_DIR}/tests"
else
    exec radish "$@"
fi
