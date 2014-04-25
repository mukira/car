import threading
import datetime
import time
from sys import exit

global loopVariable
global timeDelay
timeDelay = 1.0
loopVariable = timeDelay

    
class ThreadClass(threading.Thread):
    def run(self):
        global loopVariable
        global timeDelay
        shutDown = 0
        while loopVariable > 0:
            loopVariable -= timeDelay
            timeNow = time.strftime("%Y-%m-%d %H:%M")
            print(timeNow)
            time.sleep(timeDelay)
            shutDown +=1
            if shutDown > 10:
                exit(0)
            

def main():
    global loopVariable
    global timeDelay
    t = ThreadClass()
    t.start()

    while True:
        loopVariable += timeDelay
        print"added 1 to the loop variable"
        time.sleep(timeDelay)
        if not t.isAlive:
            print("Thread is dead")
        else:
            print("Thread is alive")
        if loopVariable > 5:
            break


if __name__ == "__main__":
    main()