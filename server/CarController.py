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
    global forwardGlo
    global delayTimeGlo
    forwardGlo += delayTimeGlo
def back():
    global backGlo
    global delayTimeGlo
    backGlo += delayTimeGlo
def left():
    global leftGlo
    global delayTimeGlo
    leftGlo += delayTimeGlo
def right():
    global forwardGlo
    global delayTimeGlo
    rightGlo += delayTimeGlo

def turnOffPins():
   GPIO.output(rightWheelForward,False)
   GPIO.output(leftWheelForward,False)
def reset():
   turnOffPins()
   forwardGlo = 0
   backGlo = 0
   leftGlo = 0
   rightGlo = 0
    
def runCarForward():
   global delayTimeGlo
   global forwardGlo
   #Turn on the GPIO pin
   GPIO.output(rightWheelForward,GPIO.HIGH)
   GPIO.output(leftWheelForward,GPIO.HIGH)
   while forwardGlo > 0:
      time.sleep(delayTimeGlo)
      forwardGlo -= delayTimeGlo
    turnOffPins()
    break
def runCarBackwards():
   global delayTimeGlo
   global backGlo
   while backGlo > 0:
       time.sleep(delayTimeGlo)
       backGlo -= delayTimeGlo
    turnOffPins() 
    break
def runCarLeft():
   global delayTimeGlo
   global leftGlo
   while leftGlo > 0:
       time.sleep(delayTimeGlo)
       leftGlo -= delayTimeGlo
    turnOffPins()
    break
def runCarRight():
   global delayTimeGlo
   global rightGlo
   while rightGlo > 0:
       time.sleep(delayTimeGlo)
       rightGlo -= delayTimeGlo
    turnOffPins()
    break
def mainThread():
   global directionGlo
   #Define threads
   thread1 = startChildThread(1, "forward")
   thread2 = startChildThread(2, "back")
   thread3 = startChildThread(2, "left")
   thread4 = startChildThread(2, "right")
   if threadsArray > 1:
       break
   
   if directionGlo == "forward":
       if thread1.isAlive():
           #run the method since the thread that runs the car is started
           forward()
       elif not threadsArray > 1:
            #start the thread
            thread1.start()
            #add them to the array to keep track of them
            threadsArray.append(thread1)
            #start the method that runs the car
            runCarForward()
   elif directionGlo == "back":
       if thread2.isAlive():
           back()
       elif not threadsArray > 1:
            thread2.start()
            threadsArray.append(thread2)
            runCarBackwards():
   elif directionGlo == "left":
       if thread3.isAlive():
           left()
       elif not threadsArray > 1:
            thread3.start()
            threadsArray.append(thread3)
            runCarLeft()
   elif directionGlo == "right":
       if thread4.isAlive():
           right()
       elif not threadsArray > 1:
           thread4.start()
           threadsArray.append(thread4)
           runCarRight()
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