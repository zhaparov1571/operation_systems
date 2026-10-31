#!/usr/bin/env python3
import threading

counter = 0

def worker(_):
    global counter
    for _ in range(100_000):
        counter += 1

threads = [threading.Thread(target=worker, args=(i,)) for i in range(4)]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

print(f"counter={counter}")
print("Ожидаемое значение при отсутствии потерянных обновлений: 400000")
