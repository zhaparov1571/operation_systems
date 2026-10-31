#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="$SCRIPT_DIR/data"
mkdir -p "$DATA_DIR"
for i in $(seq -w 1 50); do
    file="$DATA_DIR/$i.log"
    : > "$file"
    for j in $(seq 1 10); do
        level="INFO"
        n=$(( (10#$i + j) % 5 ))
        if (( n == 0 )); then level="ERROR"; elif (( n == 1 )); then level="WARN"; fi
        printf '2026-02-%02d 10:%02d:%02d %s module=module_%d msg=sample_%d\n' \
            "$(( (10#$i % 28) + 1 ))" "$((j * 3))" "$((j * 5))" "$level" "$(( (10#$i % 4) + 1 ))" "$j" >> "$file"
    done
done
echo "Создано 50 журналов в $DATA_DIR"
