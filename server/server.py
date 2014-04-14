# Echo server program
import socket
import CarController as carCon
#global variables
delayTime = 1 #the delay between the packages for making the car move
#handeling the socket
HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
c, addr = s.accept()
c.sendall('connected to server')
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
            carCon.runCar(delayTime,"forward")
       elif switch == "back":
            c.sendall('ok')     #returns "ok" if the command exists
            carCon.runCar(delayTime,"back")
       elif switch == "right":
            c.sendall('ok')     #returns "ok" if the command exists
       elif switch == "left":
            c.sendall('ok')     #returns "ok" if the command exists
       elif switch == "reset":
          c.sendall("ok")
          carCon.reset();
       else:
            c.sendall('Error')  #returns "Error" if the command DON'T exists

   c.close()                # Close the connection
