from utils import *
import random, math

def getRandomDistr():
  return map(lambda x: random.gauss(0, 0.01), range(3))

def disperseParticleMove(particle, D):
   [x, y, theta, weight] = particle
   [e, f, g] = getRandomDistr()
   theta = theta if theta >= -math.pi else theta + 2 * math.pi
   return (x + (e + D) * math.cos(theta), y + (e + D) * math.sin(theta), theta + f, weight)

def disperseParticleRotate(particle, A):
  [x, y, theta, weight] = particle
  [e, f, g] = getRandomDistr()
  theta = theta if theta >= -math.pi else theta + 2 * math.pi

  return (x, y, theta + A + g, weight)

# param is Distance for move or Angle for rotate
def disperseParticles(particles, param, isMove):
  if isMove:
    _particles = map(lambda par: disperseParticleMove(par, param), particles.get())
  else:
    _particles = map(lambda par: disperseParticleRotate(par, param), particles.get())
  particles.set(_particles) 

def moveSmart(particles, updateFunc, cm, speed=250):
  enableMotor(m1)
  enableMotor(m2)
  update()

  a = enc(m1)
  b = enc(m2)
  normal = a - b
  cmAcum = 0
  cnt = 0

  #print 'move', cm

  while cnt / encToCm < cm:
    # Update movment
    stepEnc = (mod(a - enc(m1)) +  mod(b - enc(m2))) / 2.0
    cnt += stepEnc
    cmAcum += stepEnc / encToCm   

    if cmAcum > 0.5:
      updateFunc(particles, cmAcum, True)
      particles.draw()
      cmAcum = 0

    # Read new enocder values
    a = enc(m1)
    b = enc(m2)
    dif = a - b

    spds = calibrate(speed, speed, dif - normal)
    setSpeed(m1, spds[0])
    setSpeed(m2, spds[1])
    update()

def rotateSmart(particles, updateFunc, deg, speed=250):
  rotate(deg, speed)

  print 'rotate', deg
  
  rad = (deg * math.pi) / 180
  updateFunc(particles, rad, False)
  particles.draw()

