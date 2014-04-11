import RPi.GPIO as GPIO
import time
from datetime import datetime
import threading
from threading import Thread, Event

#global variables
forwardGlo = 0
backGlo = 0
leftGlo = 0
rightGlo = 0
delayTimeGlo = 0
directionGlo = none
#Ignores any warning
GPIO.setwarnings(False)
#setting the GPIO pins variables
rightWheelForward = 25
leftWheelForward = 18
# Alternatively use GPIO.BOARD to use board pin numbering
GPIO.setmode(GPIO.BOARD)
# Select if pins are input or output
GPIO.setup(rightWheelForward, GPIO.OUT)
GPIO.setup(leftWheelForward,GPIO.OUT)
#keep track of all the threads
threadsArray = []
class startChildThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
       if self.name == "forward":
            runCarForward()
       elif self.name == "back":
            runCarBackwards()

def forward():
    print("in method forward")
    global forwardGlo
    global delayTimeGlo
    forwardGlo += delayTimeGlo
    runCarForward()
def back():
    print("in method back")
def right():
    print "in method right!"
def left():
    print "in method left!"
def turnOffPins():
   GPIO.output(rightWheelForward,False)
   GPIO.output(leftWheelForward,False)
def reset():
   turnOffPins()
   forwardGlo = 0
   backGlo = 0
   leftGlo = 0
   rightGlo = 0
   
def runCarBackwards():
   global delayTimeGlo

def runCarForward():
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

def mainThread():
   global directionGlo
   #Define threads
   thread1 = startChildThread(1, "forward")
   thread2 = startChildThread(2, "back")
   thread3 = startChildThread(2, "left")
   thread4 = startChildThread(2, "right")

   if directionGlo == "forward":
      #start the thread
      thread1.start()
      #add them to the array to keep track of them
      threadsArray.append(thread1)
   elif directionGlo == "back":
      thread2.start()
      threadsArray.append(thread2)
   elif directionGlo == "left":
      thread3.start()
      threadsArray.append(thread3)
   elif directionGlo == "right":
      thread4.start()
      threadsArray.append(thread4)

   # Wait for all threads to complete
   while True:
      #print("loop in the parrent thread",threadsArray)
      #time.sleep(1)
      for t in threadsArray:
         t.join()
         print "Exiting Main Thread"
         break
    

def runCar(delayTime,direction):
   directionGlo = direction
   delayTimeGlo = delayTime
   mainThread = Thread(target = forward , args=())
   mainThread.start()
    '''
    if not mainThread.empty():
        if direction == "forward":
            mainThread.start()
        if direction == "back":
            mainThread.start()'''