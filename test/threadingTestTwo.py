import time
from threading import Thread, Event

#global variables
timeDelay = 1.0 #pre set variable for the time intervals
loopVariable = timeDelay #used for the loops
timeToDie = 0 #makes sure the loops don't run for ever

def child(quit):
    #imports the global variables
    global loopVariable
    global timeDelay
    global timeToDie
    while True:
        loopVariable -= timeDelay
        print("Child is running")
        time.sleep(timeDelay)
        if quit.isSet(): #kills the thread
            print "Parent sent kill command"
            return

def parent():
    #imports the global variables
    global loopVariable
    global timeDelay
    global timeToDie

    quitEvent = Event() #creates an event for closing the child
    c = Thread(target=child, args=(quitEvent,)) #sets up the child
    c.start() #starts the child
    
    while True:
        loopVariable += timeDelay #adds to the variable to keep the loops going
        print("Parent is running")
        time.sleep(timeDelay)
        timeToDie += 1 #adds to the variable used to kill the threads
        if timeToDie > 5: 
            quitEvent.set() #kills the child
        if timeToDie > 10:
            break #kills the while loop
        if c.isAlive():
            print("Child is alive according to parrent")
        if not c.isAlive():
            print("Child is NOT alive according to parrent")
        

if __name__ == "__main__":
    t = Thread(target=parent, args=())
    t.start()
    #t.join() #this joins the thread and prevents any code after from running until the thread is closed
    if t.isAlive():
        print("Parent is alive")