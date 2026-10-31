#!/usr/bin/env python3
import threading
import time

lock_a = threading.Lock()
lock_b = threading.Lock()
barrier = threading.Barrier(2)

def first():
    with lock_a:
        print("Поток 1 захватил A", flush=True)
        barrier.wait()
        print("Поток 1 ждёт B", flush=True)
        with lock_b:
            print("Поток 1 получил B")

def second():
    with lock_b:
        print("Поток 2 захватил B", flush=True)
        barrier.wait()
        print("Поток 2 ждёт A", flush=True)
        with lock_a:
            print("Поток 2 получил A")

threading.Thread(target=first, daemon=True).start()
threading.Thread(target=second, daemon=True).start()
time.sleep(3)
print("Если оба потока ждут второй lock, возник deadlock. Заверши Ctrl+C.", flush=True)
while True:
    time.sleep(1)
