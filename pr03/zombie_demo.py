#!/usr/bin/env python3
import os
import time

pid = os.fork()
if pid == 0:
    print(f"Ребёнок PID={os.getpid()} завершается; родитель PID={os.getppid()}", flush=True)
    os._exit(0)

print(f"Родитель PID={os.getpid()}, ребёнок PID={pid}.")
print("В течение 20 секунд проверь в другом терминале:")
print(f"ps -o pid,ppid,stat,cmd -p {pid}")
print("В колонке STAT ожидается Z (если среда позволяет наблюдать зомби).", flush=True)
time.sleep(20)
os.waitpid(pid, 0)
print("Родитель вызвал waitpid(); запись зомби убрана.")
