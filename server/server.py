__author__ = 'ludwig'
#!/usr/bin/python           # This is server.py file

import socket               # Import socket module
import RPi.GPIO as GPIO
import time

#Ignores any warning
GPIO.setwarnings(False)
#setting the GPIO pins variables
rightWheelPort = 25
leftWheelPort = 18
# Alternatively use GPIO.BOARD to use board pin numbering
GPIO.setmode(GPIO.BCM)
# Select if pins are input or output
GPIO.setup(rightWheelPort, GPIO.OUT)
GPIO.setup(leftWheelPort,GPIO.OUT)

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

print(host + port)

def forward():
    #Turn on the GPIO pin
    GPIO.output(rightWheelPort,GPIO.HIGH)
    GPIO.output(leftWheelPort,GPIO.HIGH)
    #wait for 4 seconds
    time.sleep(4)
    #Turn off the GPIO pin
    GPIO.output(rightWheelPort,False)
    GPIO.output(leftWheelPort,False)


s.listen(5)                 # Now wait for client connection.
while True:
   c, addr = s.accept()     # Establish connection with client.
   print 'Got connection from', addr
   c.send('Thank you for connecting')
   print addr
   forward()
   c.close()                # Close the connection








