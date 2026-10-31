#!/usr/bin/env python3
import argparse
from pathlib import Path

def load(path):
    lines = [line.strip() for line in Path(path).read_text().splitlines() if line.strip()]
    available = list(map(int, lines[0].split(":",1)[1].split()))
    def matrix_after(label):
        index = next(i for i,line in enumerate(lines) if line.startswith(label))
        return [list(map(int, lines[index+1+j].split())) for j in range(5)]
    return available, matrix_after("Allocation"), matrix_after("Max")

def safe_sequence(available, allocation, maximum):
    n = len(allocation)
    need = [[maximum[i][j]-allocation[i][j] for j in range(len(available))] for i in range(n)]
    work = available[:]
    finish = [False]*n
    sequence = []
    while len(sequence) < n:
        found = False
        for i in range(n):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(len(work))):
                work = [work[j]+allocation[i][j] for j in range(len(work))]
                finish[i] = True
                sequence.append(f"P{i}")
                found = True
        if not found:
            return False, []
    return True, sequence

def request_resources(available, allocation, maximum, pid, request):
    i = int(pid[1:])
    need = [maximum[i][j]-allocation[i][j] for j in range(len(available))]
    if any(request[j] > need[j] for j in range(len(request))):
        return False, "Запрос превышает Need"
    if any(request[j] > available[j] for j in range(len(request))):
        return False, "Недостаточно Available"
    new_avail = [available[j]-request[j] for j in range(len(request))]
    new_alloc = [row[:] for row in allocation]
    new_alloc[i] = [new_alloc[i][j]+request[j] for j in range(len(request))]
    safe, seq = safe_sequence(new_avail, new_alloc, maximum)
    if not safe:
        return False, "Запрос отклонён: состояние небезопасно"
    return True, "Запрос принят; безопасная последовательность: " + " -> ".join(seq)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("--request", nargs=4, metavar=("PID","R1","R2","R3"))
    args = parser.parse_args()
    available, allocation, maximum = load(args.file)
    safe, sequence = safe_sequence(available, allocation, maximum)
    if safe:
        print("SAFE:", " -> ".join(sequence))
    else:
        print("UNSAFE")
    if args.request:
        pid, *values = args.request
        accepted, message = request_resources(available, allocation, maximum, pid, list(map(int,values)))
        print(message)

if __name__ == "__main__":
    main()
