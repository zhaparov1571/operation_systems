#!/usr/bin/env python3
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import urlopen
import time

BASE = "http://127.0.0.1:8000"
OUT = Path(__file__).parent / "downloads"
OUT.mkdir(exist_ok=True)
urls = [f"{BASE}/file_{i:02d}.txt" for i in range(20)]

def download(item):
    index, url = item
    with urlopen(url, timeout=10) as response:
        data = response.read()
    (OUT / f"download_{index:02d}.txt").write_bytes(data)
    return len(data)

def run_sequential():
    start = time.perf_counter()
    sizes = [download(item) for item in enumerate(urls)]
    return time.perf_counter() - start, sum(sizes)

def run_threads():
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=4) as pool:
        sizes = list(pool.map(download, enumerate(urls)))
    return time.perf_counter() - start, sum(sizes)

try:
    sequential_time, sequential_bytes = run_sequential()
    threaded_time, threaded_bytes = run_threads()
except Exception as exc:
    raise SystemExit(f"Не удалось скачать файлы. Убедись, что сервер запущен на порту 8000: {exc}")

print(f"Последовательно: {sequential_time:.4f} с, {sequential_bytes} байт")
print(f"4 потока:       {threaded_time:.4f} с, {threaded_bytes} байт")
