__author__ = 'ludwig'

import RPi.GPIO as GPIO
import time

#Ignores any warning
GPIO.setwarnings(False)

#setting the GPIO pins variables
rightWheelPort = 25
leftWheelPort = 18

# Alternatively use GPIO.BOARD to use board pin numbering
GPIO.setmode(GPIO.BCM)

# Select if pins are input or output
GPIO.setup(rightWheelPort, GPIO.OUT)
GPIO.setup(leftWheelPort,GPIO.OUT)

#Turn on the GPIO pin
GPIO.output(rightWheelPort,GPIO.HIGH)
GPIO.output(leftWheelPort,GPIO.HIGH)
#wait for 4 seconds
time.sleep(4)
#Turn off the GPIO pin
GPIO.output(rightWheelPort,False)
GPIO.output(leftWheelPort,False)