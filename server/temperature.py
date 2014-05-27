#!/usr/bin/python

#--------------------------------------
# BWC    - Temperature sensor
# Author - Kasper Wilkosz
# a temperature sensor using a pt100 thermocouple (-50 to 550 degrees celcius range)
# with an MCP3008 converting the analog voltage reading into a digital reading on
# the raspberry pi
# 470 ohm resistor for calibration of temperature readings
#--------------------------------------

import spidev
import time
import os

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)

# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

# Function to convert data to voltage level,
# rounded to specified number of decimal places.
def ConvertVolts(data,places):
  volts = (data * 3.3) / float(1023)
  volts = round(volts,places)
  return volts

def ConvertTemp(data,places):

  temp = ((data * 330)/float(1023))-50

  temp = temp + 10

  temp = round(temp,places)
  return temp

def ConvertVoltToTemp(volts):

  temp = 0
  # temp = (575 * volts) - 354
  if volts > 0.64:
    temp = (700 * volts) - 437
  else:
    temp = (575 * volts) - 343
  temp = round(temp,2)
  return temp


# Define sensor channels
temp_channel  = 1

# Define delay between readings
delay = 2

while True:

  # Read the temperature sensor data
  temp_level = ReadChannel(temp_channel)
  temp_volts = ConvertVolts(temp_level,3)
  temp       = ConvertVoltToTemp(temp_volts)

  # Print out results
  print "--------------------------------------------"
  print("Temp  : {}V {}C".format(temp_volts,temp))

  # Wait before repeating loop
  time.sleep(delay)
