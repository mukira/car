import time
from threading import Thread, Event


timeDelay = 1.0
loopVariable = timeDelay
timeToDie = 0

def child(quit):
    global loopVariable
    global timeDelay
    global timeToDie
    while True:
        loopVariable -= timeDelay
        print("Child is running")
        time.sleep(timeDelay)
        #if timeToDie > 5:
        #    break
        if quit.isSet():
            print "Parent sent kill command"
            return
            
    """
    for _ in xrange(10):
        if quit.isSet():
            print "Parent is dead. Leaving child."
            return

        print "Child alive"
        time.sleep(.5)
    """
def parent():
    global loopVariable
    global timeDelay
    global timeToDie

    quitEvent = Event()
    c = Thread(target=child, args=(quitEvent,))
    c.start()
    
    while True:
        loopVariable += timeDelay
        print("Parent is running")
        time.sleep(timeDelay)
        timeToDie += 1
        if timeToDie > 5:
            quitEvent.set()
        if timeToDie > 10:
            break
        if c.isAlive():
            print("Child is alive according to parrent")
        if not c.isAlive():
            print("Child is NOT alive according to parrent")
        
"""
    try:
        time.sleep(2)
        raise Exception("Parent thread raises exception")
    finally:
        quitEvent.set()

    t.join()
"""

if __name__ == "__main__":
    t = Thread(target=parent, args=())
    t.start()
    #t.join()