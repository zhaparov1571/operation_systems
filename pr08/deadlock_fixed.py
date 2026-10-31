#!/usr/bin/env python3
import threading

lock_a = threading.Lock()
lock_b = threading.Lock()

def worker(name):
    # Все потоки захватывают ресурсы в одном и том же порядке.
    with lock_a:
        with lock_b:
            print(f"{name}: оба lock получены")

threads = [threading.Thread(target=worker, args=(f"Поток {i}",)) for i in range(2)]
for t in threads: t.start()
for t in threads: t.join()
print("Завершено без взаимоблокировки.")
