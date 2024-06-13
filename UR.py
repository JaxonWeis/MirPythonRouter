import socket
from time import sleep

host = "192.168.1.25"
port = 29999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
data = s.recv(1024)
print("1: " + data.decode())


s.send(("load Load.urp\n").encode())
data = s.recv(1024)
print("2: " +data.decode())

s.send(("play\n").encode())
data = s.recv(1024)
print("3: " +data.decode())

while True:
    sleep(1)
    s.send(("running\n").encode())
    data = s.recv(1024).decode()
    print(data)
    if data == "Program running: false\n":
        break

s.close()

