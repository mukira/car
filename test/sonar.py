import RPi.GPIO as GPIO
import time

#pins
sonarTriggerPort = 23
sonarEchoPort = 24

#Ignores any warning
GPIO.setwarnings(False)

# Alternatively use GPIO.BOARD to use board pin numbering
GPIO.setmode(GPIO.BCM)

# Select if pins are input or output
GPIO.setup(sonarTriggerPort, GPIO.OUT)
GPIO.setup(sonarEchoPort,GPIO.IN)

#Sonar might require this sleep time to start properly
time.sleep(0.3)

while True:
    #Sonar variables
    timeOn = 0
    timeOff = 0
    intTimeout = 2100

    #Set sonar trigpin high for 10 us
    GPIO.output(sonarTriggerPort,GPIO.HIGH)
    time.sleep(0.001)
    GPIO.output(sonarTriggerPort,False)

    # Wait for echo pin to go low, then start timer
    while GPIO.input(sonarEchoPort) == GPIO.LOW and intTimeout > 0:
        intTimeout = intTimeout - 1
    timeOn = time.time()

     # Enter here if timeout has not occured
    if intTimeout > 0:
        intTimeout = 2100
        # Wait for echo pin to go high. Then stop timer.
        while GPIO.input(sonarEchoPort) == GPIO.HIGH and intTimeout > 0:
            intTimeout = intTimeout - 1
        timeOff = time.time()
    
        if intTimeout > 0: 
            elapsed = timeOff-timeOn
            distance = (elapsed * 34000)/2;
            print("Distance to object; " , distance)
            
        time.sleep(0.2)