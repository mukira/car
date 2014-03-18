import threading
import datetime
import time


timeDelay = 1.0
loopVariable = timeDelay

class ThreadClass(threading.Thread):
    def run(self):
        global loopVariable
        global timeDelay
        while loopVariable > 0:
            now = datetime.datetime.now()
            print "%s says Hello World at time: %s \n" % (self.getName(), now)
            time.sleep(timeDelay)
            

global loopVariable
global timeDelay
t = ThreadClass()
t.start()
while True:
    loopVariable += timeDelay
    print"added 1 to the loop variable"
    time.sleep(timeDelay)

    