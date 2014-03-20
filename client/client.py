# Echo client program
import socket
import time
from datetime import datetime

HOST = "raspberrypi.lan"    # The remote host
PORT = 50007              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((HOST, PORT))

print datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "sending"
s.sendall("forward")
print "Received data; ", s.recv(1024)
s.close()