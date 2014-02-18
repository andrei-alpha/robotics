from utils import *
from particleDataStructure import *
from uncertain_move import *
from normalise_resample import *
import random, math

mymap = Map()
initMap(mymap)
K = 0.000014

s3 = PORT_3
enableSensor(s3, TYPE_SENSOR_ULTRASONIC_CONT)

# Returns how likely the x,y corresponds with sonar reading
def calculate_likelihood(x, y, theta, z):
  m = 9999999

  # Try to intersect with each wall and take closest one
  for wall in mymap.get_walls():
    _m = intersect(wall, x, y, theta)
    if (_m < m):
      m = _m
      ang = incidence(wall, x, y, theta)
    
  # If the angle is more than 40 deg discard
  if ang > 40 * math.pi / 180:
    return 0.5

  print m, z
  a = - ((z - m) * (z - m))
  b = 4 # Varience for a gaussian distribution of sonar offsets
  return math.pow(math.e, a / b) + K

def updateMCL(particles):
  _wparticles = map(

#m = calculate_likelihood(50, 10, -1.6253, 12)
#print ">>>", m

def navigate((wx, wy), particles):
  x = sum( map(lambda par: par[0], particles.get()) ) / NOP
  y = sum( map(lambda par: par[1], particles.get()) ) / NOP
  theta = sum( map(lambda par: par[2], particles.get()) ) / NOP  

  [dx, dy] = [wx - x, wy - y]
  alpha = math.atan2(dy, dx)
  beta = alpha - theta
  ang = beta / math.pi * 180
  
  #rotateMCLDraw(-ang, speed, True)
  #moveMCLDraw(dist(x, y, wx, wy), speed, True)

def path_follow(points, particles):
  for point in points:
    navigate(point, particles)

points = [(84, 30),
  (180, 30),
  (180, 54),
  (126, 54),
  (126, 168),
  (126, 126),
  (30, 54),
  (84, 54),
  (84, 30)]

particles = Particles((84, 30, 0))
path_follow(points, particles)

