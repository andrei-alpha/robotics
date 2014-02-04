import random
from utils import *

left = PORT_1
right = PORT_2

enableSensor(left, TYPE_SENSOR_TOUCH)
enableSensor(right, TYPE_SENSOR_TOUCH)

speed = 250
dirmv = 1

while True:
  move(1, speed)
  update()
  
  val_left = sensor(left)
  val_right = sensor(right)
  
  if val_left and val_right:
    deg = 90 if random.random() < 0.5 else -90
  elif val_left:
    deg = 45
  elif val_right:
    deg = -45
    
  if val_left or val_right:
    move(5, speed * -1)
    rotate (deg, 250)
