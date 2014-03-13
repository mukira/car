import RPi.GPIO as GPIO
import time
from datetime import datetime

#Ignores any warning
GPIO.setwarnings(False)

#setting the GPIO pins variables
rightWheelForward = 25
leftWheelForward = 18

# Alternatively use GPIO.BOARD to use board pin numbering
GPIO.setmode(GPIO.BCM)

# Select if pins are input or output
GPIO.setup(rightWheelForward, GPIO.OUT)
GPIO.setup(leftWheelForward,GPIO.OUT)

def forward(delayTime):
    print datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #Turn on the GPIO pin
    GPIO.output(rightWheelForward,GPIO.HIGH)
    GPIO.output(leftWheelForward,GPIO.HIGH)
    #wait for the delayTime variable seconds
    time.sleep(delayTime)
    #Turn off the GPIO pin
    GPIO.output(rightWheelForward,False)
    GPIO.output(leftWheelForward,False)
def back():
    print "back!"
def right():
    print "right!"
def left():
    print "left!"
