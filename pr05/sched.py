#!/usr/bin/env python3
import argparse
from collections import deque
from pathlib import Path

def read_processes(path):
    processes = []
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        pid, arrival, burst, priority = line.split()
        processes.append({"pid": pid, "arrival": int(arrival), "burst": int(burst), "priority": int(priority)})
    if not processes:
        raise ValueError("Файл не содержит процессов")
    return processes

def metrics(processes, segments):
    completion = {}
    first_start = {}
    for pid, start, end in segments:
        first_start.setdefault(pid, start)
        completion[pid] = end
    rows = []
    for p in processes:
        turnaround = completion[p["pid"]] - p["arrival"]
        waiting = turnaround - p["burst"]
        rows.append((p["pid"], waiting, turnaround))
    n = len(rows)
    return rows, sum(r[1] for r in rows)/n, sum(r[2] for r in rows)/n

def fcfs(ps):
    t, seg = 0, []
    for p in sorted(ps, key=lambda x: (x["arrival"], x["pid"])):
        t = max(t, p["arrival"])
        seg.append((p["pid"], t, t+p["burst"]))
        t += p["burst"]
    return seg

def sjf(ps):
    pending = [dict(p) for p in ps]
    t, seg = 0, []
    while pending:
        ready = [p for p in pending if p["arrival"] <= t]
        if not ready:
            t = min(p["arrival"] for p in pending)
            ready = [p for p in pending if p["arrival"] <= t]
        p = min(ready, key=lambda x: (x["burst"], x["arrival"], x["pid"]))
        seg.append((p["pid"], t, t+p["burst"]))
        t += p["burst"]
        pending.remove(p)
    return seg

def rr(ps, quantum=3):
    if quantum < 1:
        raise ValueError("Квант должен быть >= 1")
    items = {p["pid"]: dict(p, remaining=p["burst"]) for p in ps}
    arrivals = sorted(ps, key=lambda x: (x["arrival"], x["pid"]))
    ready, seg = deque(), []
    i, t = 0, 0
    while i < len(arrivals) or ready:
        if not ready and i < len(arrivals) and t < arrivals[i]["arrival"]:
            t = arrivals[i]["arrival"]
        while i < len(arrivals) and arrivals[i]["arrival"] <= t:
            ready.append(arrivals[i]["pid"])
            i += 1
        pid = ready.popleft()
        p = items[pid]
        run = min(quantum, p["remaining"])
        start, end = t, t+run
        seg.append((pid, start, end))
        t = end
        p["remaining"] -= run
        # Новые процессы, прибывшие ровно в момент окончания кванта,
        # попадают в очередь раньше вытесненного процесса.
        while i < len(arrivals) and arrivals[i]["arrival"] <= t:
            ready.append(arrivals[i]["pid"])
            i += 1
        if p["remaining"] > 0:
            ready.append(pid)
    return seg

def show(name, ps, segments):
    rows, avg_wait, avg_turn = metrics(ps, segments)
    print(f"\n{name}")
    print("Gantt: " + " | ".join(f"{pid}[{start}-{end}]" for pid,start,end in segments))
    print("PID   waiting   turnaround")
    for pid, waiting, turnaround in rows:
        print(f"{pid:<5} {waiting:>7}   {turnaround:>10}")
    print(f"Среднее ожидание: {avg_wait:.2f}")
    print(f"Средний оборот:   {avg_turn:.2f}")

def main():
    parser = argparse.ArgumentParser(description="Симулятор FCFS, SJF, RR")
    parser.add_argument("--algo", choices=["fcfs","sjf","rr","all"], default="all")
    parser.add_argument("--quantum", type=int, default=3)
    parser.add_argument("file")
    args = parser.parse_args()
    ps = read_processes(args.file)
    algorithms = {"fcfs": lambda: fcfs(ps), "sjf": lambda: sjf(ps), "rr": lambda: rr(ps,args.quantum)}
    names = algorithms if args.algo == "all" else [args.algo]
    for name in names:
        show(name.upper() + (f" q={args.quantum}" if name == "rr" else ""), ps, algorithms[name]())

if __name__ == "__main__":
    main()
