#!/usr/bin/env bash
# run.bash --- run scripts from cron

# Run moody_bot scripts using virtual env with cron.

# bash strict mode
set -euo pipefail

script_dir="$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)"

cd "$script_dir"

. .venv/bin/activate

case $1 in
    reply) python3 moody.py reply ;;
    post)  python3 moody.py post  ;;
esac
