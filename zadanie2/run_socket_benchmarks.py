import subprocess
import csv
import time

CONC = [10, 50, 100, 200, 500]

def run(path, port, conc):
    procs = []
    t0 = time.time()
    for _ in range(conc):
        p = subprocess.Popen(
            ["python", "socket_client.py", path],
            stdout=subprocess.PIPE
        )
        procs.append(p)
    
    for p in procs:
        p.wait()
    
    return time.time() - t0

rows = []
for server_port in [9001, 9002]:
    for c in CONC:
        dt = run(".", server_port, c)
        rows.append({
            "server_port": server_port,
            "concurrency": c,
            "elapsed_s": round(dt, 3)
        })

with open("socket_results.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)

print("done")