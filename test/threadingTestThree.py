#!/usr/bin/python

import threading
import time
from threading import Thread, Event
#global variables
threadLock = threading.Lock()
threads = []

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print "Starting " + self.name
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
    thread1 = myThread(1, "forward", 1)
    thread2 = myThread(2, "back", 2)

    if not thread1.isAlive() or thread2.isAlive():
        # Start new Threads
        thread1.start()
        # Add threads to thread list
        threads.append(thread1)
    if not thread1.isAlive() or thread2.isAlive():
        thread2.start()
        threads.append(thread2)

    # Wait for all threads to complete
    while True:
        for t in threads:
            t.join()
        print "Exiting Main Thread"
        break

if __name__ == "__main__":
    par = Thread(target=parent, args=())
    print("starting parent thread")
    par.start()
