from utils import *
from particleDataStructure import *
from prob_motion import *
from normalise_resample import *
import random, math

speed = 150
mymap = Map()
initMap(mymap)
K = 0.000014

s3 = PORT_3
enableSensor(s3, TYPE_SENSOR_ULTRASONIC_CONT)

# Returns how likely the x,y corresponds with sonar reading
def calculate_likelihood((x, y, theta, weight), z):
  m = 9999999
  ang = 0

  # Try to intersect with each wall and take closest one
  for wall in mymap.get_walls():
    _m = intersect(wall, x, y, theta)
    if (_m < m):
      m = _m
      ang = incidence(wall, x, y, theta)
    
  # If the angle is more than 40 deg discard
  if ang > 40 * math.pi / 180:
    return 1.0 / NOP
    #return 0.1
  
  if m < 22:
    return 1.0 / NOP
 
  a = - ((z - m) * (z - m))
  b = 4 # Varience for a gaussian distribution of sonar offsets
  return math.pow(math.e, a / b) + K

def updateMCL(particles, dispParam, isMove):
  update()
  z = sensor(s3)
  
  # Disperse particles based on standard gaussian deviation 
  disperseParticles(particles, dispParam, isMove)

  #print '#1', particles.get()[0]

  # Compute likelihood
  weights = map(lambda par: calculate_likelihood(par, z), particles.get())
  _particles = map(lambda tp: tp[0][:-1] + (tp[1],), zip(particles.get(), weights))
  # Normalise and resample

  #print '#2', _particles[0]
  
  _particles = normalise(_particles)
  _particles = sampling(_particles)
  particles.set(_particles)

  #print '#3', _particles[0]

def navigate((wx, wy), particles):
  x = sum( map(lambda par: par[0], particles.get()) ) / NOP
  y = sum( map(lambda par: par[1], particles.get()) ) / NOP
  theta = sum( map(lambda par: par[2], particles.get()) ) / NOP  

  print 'I am at:', x, y, theta, ' >>> ', wx, wy 

  [dx, dy] = [wx - x, wy - y]
  alpha = math.atan2(dy, dx)
  beta = alpha - theta

  #print 'rad=', beta

  # Convert from radians to deg
  deg = int(beta / math.pi * 180)
  if deg < -180:
    deg += 360
  elif deg > 180:
    deg -= 360
  
  #print 'deg=', deg

  rotateSmart(particles, updateMCL, deg, speed)
  distance = dist(x, y, wx, wy)
  
  #print 'navigate', distance
  if distance > 20: 
    moveSmart(particles, updateMCL, 20, speed)
    navigate((wx, wy), particles)
  else:
    moveSmart(particles, updateMCL, distance, speed)


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

particles = Particles((84, 30, 0, 1.0))
path_follow(points, particles)

