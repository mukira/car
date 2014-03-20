import RPi.GPIO as GPIO
import time
from datetime import datetime
import threading
#global variables
forwardGlo = 0
backGlo = 0
leftGlo = 0
rightGlo = 0
delayTimeGlo = 0
#Ignores any warning
GPIO.setwarnings(False)
#setting the GPIO pins variables
rightWheelForward = 25
leftWheelForward = 18
# Alternatively use GPIO.BOARD to use board pin numbering
GPIO.setmode(GPIO.BCM)
# Select if pins are input or output
GPIO.setup(rightWheelForward, GPIO.OUT)
GPIO.setup(leftWheelForward,GPIO.OUT)

def forward(delayTime):
   global forwardGlo
   global delayTimeGlo
   delayTimeGlo = delayTime
   forwardGlo += delayTime
   runCar()
def back():
    print "back!"
def right():
    print "right!"
def left():
    print "left!"
def turnOffPins():
   GPIO.output(rightWheelForward,False)
   GPIO.output(leftWheelForward,False)
def reset():
   turnOffPins()
   forwardGlo = 0
   backGlo = 0
   leftGlo = 0
   rightGlo = 0
    
def runCar():
   global forwardGlo
   global delayTimeGlo
   while forwardGlo > 0:
      print datetime.now().strftime('%Y-%m-%d %H:%M:%S')
      #Turn on the GPIO pin
      GPIO.output(rightWheelForward,GPIO.HIGH)
      GPIO.output(leftWheelForward,GPIO.HIGH)
      time.sleep(delayTimeGlo)
      print "time left to move forward",forwardGlo
      forwardGlo -= delayTimeGlo
      print "time left to move forward",forwardGlo
   while backGlo != 0:
      print datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   while leftGlo != 0:
      print datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   while rightGlo != 0:
      print datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   #when the loop stops turn off the pins
      turnOffPins()