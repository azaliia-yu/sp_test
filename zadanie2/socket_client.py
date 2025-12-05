import socket
import sys

path = sys.argv[1]
s = socket.socket()
s.connect(("127.0.0.1", 9001))  # или 9002
s.send(path.encode())
print("Lines:", s.recv(1024).decode())
s.close()