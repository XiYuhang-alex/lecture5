# -*- coding: utf-8 -*-
"""Drive `flutter run -d windows`, send r (hot reload) then R (hot restart),
capture all lifecycle logs to a file."""
import subprocess, threading, time, queue, sys, os

workdir = r"c:\Users\lenovo\lecture5\counter_deep"
logpath = r"c:\Users\lenovo\lecture5\screenshots\lifecycle_console.txt"
os.makedirs(os.path.dirname(logpath), exist_ok=True)

proc = subprocess.Popen(
    "flutter run -d windows",
    cwd=workdir, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace",
    bufsize=1, shell=True,
)

q = queue.Queue()
def reader():
    for line in proc.stdout:
        q.put(line)
t = threading.Thread(target=reader, daemon=True)
t.start()

collected = []
def drain(seconds, tag):
    end = time.time() + seconds
    while time.time() < end:
        try:
            line = q.get(timeout=0.3)
            collected.append(line)
            sys.stdout.write(line)
        except queue.Empty:
            pass

drain(150, "startup")  # wait for build
# mark hot reload
collected.append("\n===== SEND r (hot reload) =====\n")
proc.stdin.write("r\n"); proc.stdin.flush()
drain(12, "reload")
collected.append("\n===== SEND R (hot restart) =====\n")
proc.stdin.write("R\n"); proc.stdin.flush()
drain(20, "restart")
collected.append("\n===== SEND q (quit) =====\n")
proc.stdin.write("q\n"); proc.stdin.flush()
drain(10, "quit")
try:
    proc.terminate()
except Exception:
    pass

with open(logpath, "w", encoding="utf-8") as f:
    f.writelines(collected)
print("LOG SAVED")
