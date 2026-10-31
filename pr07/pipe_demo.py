#!/usr/bin/env python3
import os

read_fd, write_fd = os.pipe()
pid = os.fork()
if pid == 0:
    os.close(read_fd)
    message = b"Hello from child through pipe"
    os.write(write_fd, message)
    os.close(write_fd)
    os._exit(0)
else:
    os.close(write_fd)
    chunks = []
    while True:
        chunk = os.read(read_fd, 1024)
        if not chunk:
            break
        chunks.append(chunk)
    os.close(read_fd)
    os.waitpid(pid, 0)
    print(b"".join(chunks).decode())
