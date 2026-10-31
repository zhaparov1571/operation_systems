#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="${1:-$SCRIPT_DIR/data}"
if [[ ! -d "$DATA_DIR" ]]; then
    echo "Каталог не найден: $DATA_DIR" >&2
    echo "Сначала запусти: bash pr02/generate_logs.sh" >&2
    exit 1
fi
shopt -s nullglob
files=("$DATA_DIR"/*.log)
if (( ${#files[@]} == 0 )); then
    echo "В каталоге нет файлов .log: $DATA_DIR" >&2
    exit 1
fi
total=0
max_count=-1
max_file=""
for f in "${files[@]}"; do
    count=$(grep -c "ERROR" "$f" || true)
    total=$((total + count))
    printf '%s: %s ERROR\n' "$(basename "$f")" "$count"
    if (( count > max_count )); then
        max_count=$count
        max_file="$f"
    fi
done
printf 'TOTAL: %d ERROR\n' "$total"
printf 'MAX: %s (%d ERROR)\n' "$(basename "$max_file")" "$max_count"
