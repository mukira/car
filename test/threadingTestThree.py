#!/usr/bin/python

import threading
import time
from threading import Thread, Event
from time import gmtime, strftime
import datetime
#global variables
#threadLock = threading.Lock()
threadsArray = []
loopVariableForward = 1
loopVariableBack = 1
class myThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print ("Starting thread; " + self.name)
        # Get lock to synchronize threads
        #threadLock.acquire() #prevents any new threads from spawning
        if self.name == "forward":
            forward()
        elif self.name == "back":
            back()
        #print_time(self.name, self.counter, 3)
        #threadLock.release() # Free lock to release next thread


def forward():
    global loopVariableForward
    while loopVariableForward < 20:
        timeNow = datetime.datetime.now().strftime("%H:%M:%S.%f")
        print timeNow, "Running method forward! ",loopVariableForward, "\n"
        time.sleep(1)
        loopVariableForward += 1
def back():
    global loopVariableBack
    time.sleep(1)
    while loopVariableBack < 20:
        timeNow = datetime.datetime.now().strftime("%H:%M:%S.%f")
        print timeNow,"Running method back! ",loopVariableBack, "\n"
        time.sleep(1)
        loopVariableBack += 1

def parent():


    # Create new threads
    thread1 = myThread(1, "forward")
    thread2 = myThread(2, "back")

    #print("thread1",thread1.isAlive())
    #print("thread2",thread2.isAlive())
    thread1.start()
    thread2.start()
    threadsArray.append(thread1)
    threadsArray.append(thread2)

    
    # Wait for all threads to complete
    while True:
        #print("loop in the parrent thread",threadsArray)
        #time.sleep(1)
        for t in threadsArray:
            t.join()
        print "Exiting Main Thread"
        break

if __name__ == "__main__":
    par = Thread(target=parent, args=())
    print("starting parent thread")
    par.start()
    print("parent thread started")
