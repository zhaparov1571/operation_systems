#!/usr/bin/env python3
import subprocess

first = subprocess.Popen(["ls"], stdout=subprocess.PIPE, text=True)
second = subprocess.run(["grep", "py"], stdin=first.stdout, text=True, check=False)
first.stdout.close()
first.wait()
print(f"grep exit code: {second.returncode}")
