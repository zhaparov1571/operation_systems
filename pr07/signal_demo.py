#!/usr/bin/env python3
import signal
import os
import time

def handle_sigint(signum, frame):
    print(f"Получен SIGINT ({signum}); программа продолжает работу.", flush=True)

signal.signal(signal.SIGINT, handle_sigint)
print(f"PID={os.getpid()}. Отправь kill -INT {os.getpid()} или нажми Ctrl+C. Для выхода нажми Ctrl+\\ или заверши процесс.", flush=True)
while True:
    time.sleep(1)
