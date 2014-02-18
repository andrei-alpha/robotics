import random
import os
from utils import *

def speak(text):
  os.system('espeak -a 200 "' + text + ' &"')

speed = 100
dirmv = 1

while True:
  er = move(10, dirmv * speed, True)
  
  # if it hits an obstacle
  if er is -1:
    speak('Ops an obstacle!')    

    dirmv *= -1
    move(4, dirmv * speed, False)
    #rotate between -50 and 50 degrees
    deg = int( (random.random() - 0.5) * 100.0)
    
    speak('Rotate ' +  str(deg) +  ' degrees')
    rotate(deg, 250)

    
