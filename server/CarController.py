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
directionGlo = None
#Ignores any warning
GPIO.setwarnings(False)
#setting the GPIO pins variables
turnForward = 23
turnLeftOne = 24
turnLeftTwo = 24
turnRightOne = 19
turnRightTwo = 21
#turnHeadlightFront = 0
#turnHeadlightBack = 0
# Alternatively use GPIO.BOARD to use board pin numbering
#GPIO.setmode(GPIO.BCM)
GPIO.setmode(GPIO.BOARD)
# Select if pins are input or output
GPIO.setup(turnForward, GPIO.OUT)
GPIO.setup(turnLeftOne, GPIO.OUT)
GPIO.setup(turnLeftTwo, GPIO.OUT)
GPIO.setup(turnRightOne, GPIO.OUT)
GPIO.setup(turnRightTwo, GPIO.OUT)
#GPIO.setup(turnHeadlightFront, GPIO.OUT)
#GPIO.setup(turnHeadlightBack, GPIO.OUT)
#keep track of all the threads
threadsArray = []
class startChildThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        if self.name == "forward":
            #add the time to make it run
            forward()
            #start the method that runs the car
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
    global rightGlo
    global delayTimeGlo
    rightGlo += delayTimeGlo

def turnOffPins():
    GPIO.output(turnForward,False)
    GPIO.output(turnLeftOne,False)
    GPIO.output(turnLeftTwo,False)
    GPIO.output(turnRightOne,False)
    GPIO.output(turnRightTwo,False)
    GPIO.output(turnHeadlightFront,False)
    GPIO.output(turnHeadlightBack,False)

def reset():
   print("resetting pins")
   turnOffPins()
   forwardGlo = 0
   backGlo = 0
   leftGlo = 0
   rightGlo = 0
    
def runCarForward():
    print("starting runCarForward")
    global delayTimeGlo
    global forwardGlo
    #Turn on the GPIO pin
    GPIO.output(turnForward,GPIO.HIGH)
    print("fowardGlo; " , forwardGlo)
    while forwardGlo > 0:
        time.sleep(delayTimeGlo)
        forwardGlo -= delayTimeGlo
    turnOffPins()
def runCarBackwards():
    global delayTimeGlo
    global backGlo
    GPIO.output(turnRightOne,GPIO.HIGH)
    GPIO.output(turnRightTwo,GPIO.HIGH)
    GPIO.output(turnLeftOne,GPIO.HIGH)
    GPIO.output(turnLeftTwo,GPIO.HIGH)
    GPIO.output(turnForward,GPIO.HIGH)
    while backGlo > 0:
        time.sleep(delayTimeGlo)
        backGlo -= delayTimeGlo
    turnOffPins() 
def runCarLeft():
    global delayTimeGlo
    global leftGlo
    GPIO.output(turnLeftOne,GPIO.HIGH)
    GPIO.output(turnLeftTwo,GPIO.HIGH)
    GPIO.output(turnForward,GPIO.HIGH)
    while leftGlo > 0:
        time.sleep(delayTimeGlo)
        leftGlo -= delayTimeGlo
    turnOffPins()
def runCarRight():
    global delayTimeGlo
    global rightGlo
    GPIO.output(turnRightOne,GPIO.HIGH)
    GPIO.output(turnRightTwo,GPIO.HIGH)
    GPIO.output(turnForward,GPIO.HIGH)
    while rightGlo > 0:
        time.sleep(delayTimeGlo)
        rightGlo -= delayTimeGlo
    turnOffPins()
def mainThread():
    global directionGlo
    #Define threads
    thread1 = startChildThread(1, "forward")
    thread2 = startChildThread(2, "back")
    thread3 = startChildThread(3, "left")
    thread4 = startChildThread(4, "right")
    print("mainthread direction;",directionGlo )
   
    if directionGlo == "forward":
       print("direction forward")
       if thread1.isAlive():
          print("thread is alive, adding time")
          #run the method since the thread that runs the car is started
          forward()
       else:
          print("starting thread forward")
          #start the thread
          thread1.start()
          #add them to the array to keep track of them
          threadsArray.append(thread1)

    elif directionGlo == "back":
        if thread2.isAlive():
            back()
        elif not threadsArray > 1:
            thread2.start()
            threadsArray.append(thread2)
            runCarBackwards()
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
            if threadsArray > 1:
                break
        print "Exiting Main Thread"
        break
    

def runCar(delayTime,direction):
   print("starting car controller")
   global directionGlo
   global delayTimeGlo
   
   directionGlo = direction
   delayTimeGlo = delayTime
   print("direction; " + directionGlo)

   print("delayTime; " , delayTimeGlo)

   mainThreadV = Thread(target=mainThread , args=())
   mainThreadV.start()