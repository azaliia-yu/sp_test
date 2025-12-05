import argparse
import requests
import threading
import time
import json
from queue import Queue

parser = argparse.ArgumentParser()
parser.add_argument("--url", required=True)
parser.add_argument("--concurrency", type=int, default=5)  
parser.add_argument("--requests", type=int, default=10)    
parser.add_argument("--timeout", type=int, default=60)     
parser.add_argument("--delay", type=float, default=0.1)    
args = parser.parse_args()

q = Queue()
for i in range(args.requests):
    q.put(args.url)

lock = threading.Lock()
success = 0
failed = 0
lat = []

def worker(worker_id):
    global success, failed
    while True:
        try:
            url = q.get(block=False)
        except:
            break
        
        time.sleep(args.delay)  
        
        t0 = time.time()
        try:
            r = requests.get(url, timeout=args.timeout)
            dt = (time.time() - t0) * 1000
            
            with lock:
                lat.append(dt)
                if r.status_code == 200:
                    success += 1
                    try:
                        data = r.json()
                        print(f"[Worker {worker_id}] OK: {data.get('items', 0)} items, {dt:.0f}ms")
                    except:
                        print(f"[Worker {worker_id}] OK (no JSON), {dt:.0f}ms")
                else:
                    failed += 1
                    print(f"[Worker {worker_id}] FAIL: HTTP {r.status_code}")
                    
        except requests.exceptions.Timeout:
            with lock:
                failed += 1
            print(f"[Worker {worker_id}] Timeout")
        except Exception as e:
            with lock:
                failed += 1
            print(f"[Worker {worker_id}] Error: {e}")
        
        q.task_done()

print(f"Starting load test:")
print(f"  URL: {args.url}")
print(f"  Threads: {args.concurrency}")
print(f"  Requests: {args.requests}")
print(f"  Delay between requests: {args.delay}s")

threads = []
for i in range(args.concurrency):
    t = threading.Thread(target=worker, args=(i+1,))
    t.start()
    threads.append(t)

q.join()

for t in threads:
    t.join()

avg = sum(lat)/len(lat) if lat else 0
result = {
    "success": success, 
    "failed": failed, 
    "avg_ms": round(avg, 2),
    "total_requests": args.requests,
    "success_rate": round(success/args.requests * 100, 2) if args.requests > 0 else 0
}

print(json.dumps(result, indent=2))