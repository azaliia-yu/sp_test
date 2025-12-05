import socket
import threading
import os

def count_lines(path):
    total = 0
    for root, dirs, files in os.walk(path):
        for f in files:
            try:
                with open(os.path.join(root, f), "r", errors="ignore") as fh:
                    total += sum(1 for _ in fh)
            except:
                pass
    return total

def handle(conn):
    data = conn.recv(1024).decode()
    path = data.strip()
    total = count_lines(path)
    conn.send(str(total).encode())
    conn.close()

s = socket.socket()
s.bind(("0.0.0.0", 9001))
s.listen()

print("Thread socket server on 9001")
while True:
    c, _ = s.accept()
    threading.Thread(target=handle, args=(c,), daemon=True).start()