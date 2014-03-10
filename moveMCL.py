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

# Rotates toward the closest wall
def rotate_closest_wall(particles):
  x = sum( map(lambda par: par[0], particles.get()) ) / NOP
  y = sum( map(lambda par: par[1], particles.get()) ) / NOP
  theta = sum( map(lambda par: par[2], particles.get()) ) / NOP

  thetaOffset = 0.0
  isOk = False

  for offset in list([0.0, toRad(45), toRad(-45), toRad(90), toRad(-90)]):
    [m, ang] = wall_intersect(x, y, theta + offset)
    
    if ang < toRad(-40) or ang > toRad(40) or m < 22 or m > 120:
      continue
    thetaOffset = offset
    isOk = True
    break

  print ' [rotate_closest_wall]', thetaOffset
  rotate_sonar(toDeg(thetaOffset), speed)
  disperseParticles(particles, thetaOffset, False)
  return thetaOffset

def rotate_back(particles, thetaOffset):
  rotate_sonar(toDeg(-thetaOffset), speed)
  disperseParticles(particles, -thetaOffset, False)

# Try to intersect with each wall and take closest one
def wall_intersect(x, y, theta):
  m = 9999999
  ang = 0  

  for wall in mymap.get_walls():
    _m = intersect(wall, x, y, theta)
    if (_m < m):
      m = _m
      ang = incidence(wall, x, y, theta)
  return [m, ang]

# Returns how likely the x,y corresponds with sonar reading
def calculate_likelihood((x, y, theta, weight), z):
  [m, ang] = wall_intersect(x, y, theta)
   
  #print ang, m 
  # If the angle is more than 40 deg discard
  if ang > 40 * math.pi / 180:
    return 1.0 / NOP
  
  if m < 22 or m > 120:
    return 1.0 / NOP
 
  a = - ((z - m) * (z - m))
  b = 4 # Varience for a gaussian distribution of sonar offsets
  return math.pow(math.e, a / b) + K

def updateMCL(particles, dispParam, isMove):
  time.sleep(0.001)
  update()
  z = sensor(s3) + 5
  
  # Disperse particles based on standard gaussian deviation 
  disperseParticles(particles, dispParam, isMove)

  #print '#1', particles.get()

  # Compute likelihood
  theta = rotate_closest_wall(particles)
  weights = map(lambda par: calculate_likelihood(par, z), particles.get())
  rotate_back(particles, theta)
  
  #rotate_sonar( toDeg(-theta), speed)
  #disperseParticles(particles, -theta, False)

  _particles = map(lambda tp: tp[0][:-1] + (tp[1],), zip(particles.get(), weights))
  # Normalise and resample

  #print '#2', _particles
  
  _particles = normalise(_particles)
  _particles = sampling(_particles)
  particles.set(_particles)

  #print '#3', _particles[0]

def navigate((wx, wy), particles, speed = 150):
  x = sum( map(lambda par: par[0], particles.get()) ) / NOP
  y = sum( map(lambda par: par[1], particles.get()) ) / NOP
  theta = sum( map(lambda par: par[2], particles.get()) ) / NOP  

  print ' [navigate] I am at:', x, y, theta, ' >>> ', wx, wy 

  [dx, dy] = [wx - x, wy - y]
  alpha = math.atan2(dy, dx)
  beta = alpha - theta

  #print ' [beta.navigate] rad=', beta

  # Convert from radians to deg
  deg = toDeg(beta)
  if deg < -180:
    deg += 360
  elif deg > 180:
    deg -= 360 
 
  rotateSmart(particles, updateMCL, deg, speed)
  distance = dist(x, y, wx, wy)
  
  dist_move = 20
  if distance > dist_move: 
    moveSmart(particles, updateMCL, dist_move, speed)
    updateMCL(particles, dist_move, True)
    navigate((wx, wy), particles, speed)
  else:
    moveSmart(particles, updateMCL, distance, speed)
    updateMCL(particles, distance, True)

def path_follow(points, particles):
  for point in points:
    navigate(point, particles)

