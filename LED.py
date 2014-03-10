# Jaikrishna
# Initial Date: June 28, 2013
# Last Updated: June 28, 2013
#
# These files have been made available online through a Creative Commons Attribution-ShareAlike 3.0  license.
# (http://creativecommons.org/licenses/by-sa/3.0/)
#
# http://www.dexterindustries.com/
# This code is for testing the BrickPi LEDs with GPIO library
# If GPIO library isn't installed enter: sudo apt-get install python-rpi.gpio

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print "Error importing RPi.GPIO. You need to run this with superuser privileges. Try sudo python LED.py"
import time

def flush_led():
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(12, GPIO.OUT)    #GPIO 18
  GPIO.setup(13, GPIO.OUT)    #GPIO 27 

  GPIO.output(12, True)
  GPIO.output(13, True)
  time.sleep(.1) 
  
  GPIO.output(12, False)
  GPIO.output(13, False)
  GPIO.cleanup()

def flush():
  for i in range(5):
    flush_led()
    time.sleep(.1)
