#!/usr/bin/env bash
set -euo pipefail

echo "=== whoami ==="
whoami
echo "=== pwd ==="
pwd
echo "=== uname -a ==="
uname -a
echo "=== lsb_release -a ==="
if command -v lsb_release >/dev/null 2>&1; then
    lsb_release -a
else
    echo "lsb_release не установлен; установи пакет lsb-release."
fi

mkdir -p "$HOME/os-course/pr01"
cd "$HOME/os-course/pr01"
echo "Практическая работа №1" > about.txt
echo "Знакомство с Linux и терминалом" >> about.txt
echo "=== cat about.txt ==="
cat about.txt
echo "=== ls -la ==="
ls -la
