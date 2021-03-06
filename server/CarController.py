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
sonarGlo = 0
#Ignores any warning
GPIO.setwarnings(False)
#setting the GPIO pins variables
turnForward = 23
turnLeftOne = 24
turnLeftTwo = 26
turnRightOne = 19
turnRightTwo = 21
sonarTrigger = 18
sonarEcho = 22
# Alternatively use GPIO.BOARD to use board pin numbering
#GPIO.setmode(GPIO.BCM)
GPIO.setmode(GPIO.BOARD)
# Select if pins are input or output
GPIO.setup(turnForward, GPIO.OUT)
GPIO.setup(turnLeftOne, GPIO.OUT)
GPIO.setup(turnLeftTwo, GPIO.OUT)
GPIO.setup(turnRightOne, GPIO.OUT)
GPIO.setup(turnRightTwo, GPIO.OUT)
GPIO.setup(sonarTrigger, GPIO.OUT)
GPIO.setup(sonarEcho, GPIO.IN)
#make sure trigger isn't on
GPIO.output(sonarTrigger, False)
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
            #start the method that runs the car
            runCarForward()
        elif self.name == "back":
            runCarBackwards()
        elif self.name == "right":
            runCarRight()
        elif self.name == "left":
            runCarLeft()
        elif self.name == "sonar":
            startSonar()
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

def reset():
   print("resetting pins")
   turnOffPins()

   global forwardGlo
   global  backGlo
   global  leftGlo
   global  rightGlo
   global threadsArray

   forwardGlo = 0
   backGlo = 0
   leftGlo = 0
   rightGlo = 0
   threadsArray = []

def runCarForward():
    print("starting runCarForward")
    global delayTimeGlo
    global forwardGlo
    #Turn on the GPIO pin
    GPIO.output(turnForward,GPIO.HIGH)
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
def startSonar():
    print("starting sonar")
    global sonarGlo
    # ultrasonic module needs a moment to settle in
    time.sleep(0.5)
    while True:
      GPIO.output(sonarTrigger, True)
      time.sleep(0.00001)
      GPIO.output(sonarEcho, False)
      sent = time.time()
      while GPIO.input(sonarTrigger)==0:
        sent = time.time()

      while GPIO.input(sonarTrigger)==1:
        returned = time.time()
    #Calculate time
    elapsed = returned-sent
    distance = elapsed * 34300 / 2
    sonarGlo = distance
    print "Distance is : %.1f" % distance

    if distance < 10:
      reset()
      global directionGlo
      global backGlo
      directionGlo = "back"
      backGlo = 0.5
      runCarBackwards()
      reset()

def sonarReturn():
  return sonarGlo

def mainThread():
    global directionGlo
    global threadsArray
    #Define threads
    thread1 = startChildThread(1, "forward")
    thread2 = startChildThread(2, "back")
    thread3 = startChildThread(3, "left")
    thread4 = startChildThread(4, "right")
    thread5 = startChildThread(5, "sonar")
    print("threads array; " , len(threadsArray))
    if not thread5.isAlive():
        thread5.start()
    if directionGlo == "forward":
       print("direction forward")
       if thread1.isAlive():
          #run the method since the thread that runs the car is started
          print("thread is alive")
          forward()
       elif not len(threadsArray) > 0:
          #adding the time to make it run
          forward()
          #start the thread
          thread1.start()
          #add them to the array to keep track of them
          threadsArray.append(thread1)

    elif directionGlo == "back":
        if thread2.isAlive():
            back()
        elif not len(threadsArray) > 1:
            back()
            thread2.start()
            threadsArray.append(thread2)
    elif directionGlo == "left":
        if thread3.isAlive():
            left()
        elif not len(threadsArray) > 1:
            left()
            thread3.start()
            threadsArray.append(thread3)
    elif directionGlo == "right":
        if thread4.isAlive():
            right()
        elif not len(threadsArray) > 1:
            right()
            thread4.start()
            threadsArray.append(thread4)
   # Wait for all threads to complete
    while True:
        for t in threadsArray:
            t.join()
            if threadsArray > 1:
                threadsArray = []
                break
        threadsArray = []
        break

def runCar(delayTime,direction):
   global directionGlo
   global delayTimeGlo

   directionGlo = direction
   delayTimeGlo = delayTime

   mainThreadV = Thread(target=mainThread , args=())
   #if mainThreadV.isAlive():
      #mainThreadV.join()
   #else:
   mainThreadV.start()
