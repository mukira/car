# Echo server program
import socket

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print "Connected by", addr

while True:
    data = conn.recv(1024)
    receivedData = repr(data)
    if (receivedData != None):
        switch = receivedData
        receivedData = None
        if switch == "forward":
            print"forward"
        elif switch == "back":
            print"back"
        elif switch == "left":
            print"left"
        elif switch == "right":
            print"right"
        else:
            conn.sendall("error")

    conn.sendall(data)
conn.close()