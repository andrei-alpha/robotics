from utils import *
import math

speed = 170
[x, y, theta] = [0, 0, 0]

def navigate(wx, wy):
  global x, y, theta

  [dx, dy] = [wx - x, wy - y]
  alpha = math.atan2(dy, dx)
  beta =  alpha - theta 
  ang = beta / math.pi * 180

  # do stuff
  rotate(-ang, speed)
  move(dist(x, y, wx, wy), speed)

  [x, y, theta] = [wx, wy, alpha]

navigate(50, 50)
navigate(50, -20)
navigate(0, 0)
