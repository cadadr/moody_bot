#!/usr/bin/env bash
# run.bash --- run moody bot scripts from cron with virtual env

# Copyright (C) 2022 İ. Göktuğ Kayaalp <self at gkayaalp dot com>
# This file is part of “Moody Bot”.
#
# “Moody Bot” is non-violent software: you can use, redistribute,
# and/or modify it under the terms of the CNPLv6+ as found in the
# LICENSE file in the source code root directory or at
# <https://git.pixie.town/thufie/CNPL>.
#
# “Moody Bot” comes with ABSOLUTELY NO WARRANTY, to the extent
# permitted by applicable law. See the CNPL for details.

# bash strict mode
set -euo pipefail

script_dir="$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)"

cd "$script_dir"

. .venv/bin/activate

case $1 in
    reply) python3 moody.py reply ;;
    post)  python3 moody.py post  ;;
esac
