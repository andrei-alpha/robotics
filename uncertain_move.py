from utils import *
import random, math

def getRandomDistr():
  return map(lambda x: random.gauss(0, 0.01), range(3))

def updateParticleMove(particle, D):
   [x, y, theta] = particle
   [e, f, g] = getRandomDistr()
   theta = theta if theta > 0 else theta + 2 * math.pi
   return (x + (e + D) * math.cos(theta), y + (e + D) * math.sin(theta), theta + f)

def updateParticleRotate(particle, A):
  [x, y, theta] = particle
  [e, f, g] = getRandomDistr()
  theta = theta if theta > 0 else theta + 2 * math.pi
  return (x, y, theta + A + g)

# param is Distance for move or Angle for rotate
def updateParticles(particles, param, isMove):
  if isMove:
    _particles = map(lambda par: updateParticleMove(par, param), particles.get())
  else:
    _particles = map(lambda par: updateParticleRotate(par, param), particles.get())
  particles.set(_particles) 

'''
def drawLine(D):
  x1 = reduce(lambda x, y: x + y, map(lambda par: par[0], particles) ) / NOP
  y1 = reduce(lambda x, y: x + y, map(lambda par: par[1], particles) ) / NOP
  theta = reduce(lambda x, y: x + y, map(lambda par: par[2], particles) ) / NOP
  
  x2 = x1 + D * math.cos(theta)
  y2 = y1 + D * math.sin(theta)
  print 'drawLine:' + str((x1, y1, x2, y2))
'''

def moveSmart(particles, updateFunc, cm, speed=250):
  enableMotor(m1)
  enableMotor(m2)
  update()

  # draw expected line
  drawLine(cm * mag)

  a = enc(m1)
  b = enc(m2)
  normal = a - b
  cmAcum = 0
  cnt = 0

  while cnt / encToCm < cm:
    # Update movment
    stepEnc = (mod(a - enc(m1)) +  mod(b - enc(m2))) / 2.0
    cnt += stepEnc
    cmAcum += stepEnc / encToCm   

    if cmAcum > 0.5:
      updateParticles(particles, cmAcum * mag, True)
      MLCParticles(particles)
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

  #print 'rotate'
  rad = (deg * math.pi) / 180 * -1 
  if deg > 0:
    updateParticles(particles, -rad, False)
    MLCParticles(particles)
  else:
    updateParticles(particles, rad, False)
    MLCParticles(particles)
  #particles.draw()

'''
#Test

speed = 250
mag =a16
NOP = 200 
particles = [(150, 100, 0)] * NOP

dist = 40
moveSmart(particles, dist, speed)
rotateSmart(particles, -90)
moveSmart(particles, dist, speed)
rotateSmart(particles, -90)
moveSmart(particles, dist, speed)
rotateSmart(particles, -90)
moveSmart(particles, dist, speed)

'''
