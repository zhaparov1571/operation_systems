#!/usr/bin/env python3
import queue
import threading
import time

def counter_test(use_lock):
    global_counter = [0]
    lock = threading.Lock()
    def worker():
        for _ in range(100_000):
            if use_lock:
                with lock:
                    global_counter[0] += 1
            else:
                global_counter[0] += 1
    threads = [threading.Thread(target=worker) for _ in range(4)]
    start = time.perf_counter()
    for t in threads: t.start()
    for t in threads: t.join()
    return global_counter[0], time.perf_counter()-start

def bank_demo():
    accounts = [1000, 1000, 1000]
    total_before = sum(accounts)
    lock = threading.Lock()
    def transfer(src, dst, amount):
        for _ in range(5000):
            with lock:
                if accounts[src] >= amount:
                    accounts[src] -= amount
                    accounts[dst] += amount
                assert sum(accounts) == total_before
    threads = [
        threading.Thread(target=transfer, args=(0,1,1)),
        threading.Thread(target=transfer, args=(1,2,1)),
    ]
    for t in threads: t.start()
    for t in threads: t.join()
    assert sum(accounts) == total_before
    return accounts

def producer_consumer():
    q = queue.Queue(maxsize=5)
    consumed = []
    sentinel = object()
    def producer():
        for value in range(20):
            q.put(value)
        q.put(sentinel)
    def consumer():
        while True:
            item = q.get()
            try:
                if item is sentinel:
                    return
                consumed.append(item)
            finally:
                q.task_done()
    p = threading.Thread(target=producer)
    c = threading.Thread(target=consumer)
    p.start(); c.start()
    p.join(); c.join()
    assert sorted(consumed) == list(range(20))
    return len(consumed)

if __name__ == "__main__":
    for locked in (False, True):
        value, elapsed = counter_test(locked)
        print(f"{'С lock' if locked else 'Без lock'}: counter={value}, время={elapsed:.6f} с")
    print("Счета после переводов:", bank_demo())
    print("Потреблено элементов:", producer_consumer())
