#!/usr/bin/env python3
import os

pid = os.fork()
if pid == 0:
    print(f"Я ребёнок, PID={os.getpid()}, PPID={os.getppid()}", flush=True)
    os._exit(0)
else:
    child_pid, status = os.wait()
    print(f"Родитель PID={os.getpid()} дождался PID={child_pid}; код завершения={os.waitstatus_to_exitcode(status)}")
