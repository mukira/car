#!/usr/bin/python
import Queue
import threading
import time

#global variables
workQueue = Queue.Queue(10)
exitFlag = 0
queueLock = threading.Lock()

class sThread (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    def run(self):
        print ("Starting " + self.name)
        if self.name == "forward":
            forward()
        elif self.name == "back":
            back()
        print "Exiting " + self.name
        
def process_data(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            queueLock.release()
            print "%s processing %s" % (threadName, data)
        else:
            queueLock.release()
        time.sleep(1)
        

def forward():
    print("Method forward!")
def back():
    print("Method back!")

if __name__ == "__main__":
    threadID = 1
    tName = "forward"
    thread = sThread(threadID, tName, workQueue)
    thread.start()
    if thread.isAlive():
        print("threadName; " + thread.name)