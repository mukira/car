#!/usr/bin/python

import threading
import time
from threading import Thread, Event
#global variables
threadLock = threading.Lock()
threadsArray = []

class myThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print ("Starting thread; " + self.name)
        # Get lock to synchronize threads
        threadLock.acquire()
        if self.name == "forward":
            forward()
        elif self.name == "back":
            back()
        #print_time(self.name, self.counter, 3)
        # Free lock to release next thread
        threadLock.release()

def forward():
    while True:
        print("Running method forward!")
        time.sleep(5)
        break
def back():
    while True:
        print("Running method back!")
        time.sleep(5)
        break
        
def parent():


    # Create new threads
    thread1 = myThread(1, "forward")
    thread2 = myThread(2, "back")

    #print("thread1",thread1.isAlive())
    #print("thread2",thread2.isAlive())
    
    if thread1.isAlive() == False and thread2.isAlive() == False:
        # Start new Thread
        thread1.start()
        # Add thread to thread list
        threadsArray.append(thread1)
    if thread1.isAlive() == False and thread2.isAlive() == False:
        # Start new Thread
        thread2.start()
        # Add thread to thread list
        threadsArray.append(thread2)

    # Wait for all threads to complete
    while True:
        for t in threadsArray:
            t.join()
        print "Exiting Main Thread"
        break

if __name__ == "__main__":
    par = Thread(target=parent, args=())
    print("starting parent thread")
    par.start()
