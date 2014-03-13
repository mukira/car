# Echo server program
import socket
import CarController as carCon
HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
c, addr = s.accept()
print "Connected by", addr

while True:
   c, addr = s.accept()     # Establish connection with client.
   print 'Got connection from', addr
   inData =  c.recv(1024)
   if(len(inData) > 0):
       switch = inData
       inData = None
       if switch == "forward":
            c.sendall('ok')     #returns "ok" if the command exists
            carCon.forward()
       elif switch == "back":
            c.sendall('ok')     #returns "ok" if the command exists
       elif switch == "right":
            c.sendall('ok')     #returns "ok" if the command exists
       elif switch == "left":
            c.sendall('ok')     #returns "ok" if the command exists
       else:
            c.sendall('Error')  #returns "Error" if the command DON'T exists

   c.close()                # Close the connection