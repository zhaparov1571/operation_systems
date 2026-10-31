#!/usr/bin/env python3
from pathlib import Path

root = Path(__file__).parent / "webroot"
root.mkdir(exist_ok=True)
for i in range(20):
    (root / f"file_{i:02d}.txt").write_text((f"Файл для теста {i}\n" * 1000), encoding="utf-8")
print(f"Создано 20 файлов: {root}")
