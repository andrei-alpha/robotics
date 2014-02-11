from utils import *
import random, math

speed = 200

mag = 16
NOP = 200
particles = [(150, 100, 0)] * NOP

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
def updateParticles(param, isMove):
  global particles
  if isMove:
    particles = map(lambda par: updateParticleMove(par, param), particles)
  else:
    particles = map(lambda par: updateParticleRotate(par, param), particles) 

def drawParticles():
  print 'drawParticles:' + str(particles)

def drawLine(D):
  x1 = reduce(lambda x, y: x + y, map(lambda par: par[0], particles) ) / NOP
  y1 = reduce(lambda x, y: x + y, map(lambda par: par[1], particles) ) / NOP
  theta = reduce(lambda x, y: x + y, map(lambda par: par[2], particles) ) / NOP
  
  x2 = x1 + D * math.cos(theta)
  y2 = y1 + D * math.sin(theta)
  print 'drawLine:' + str((x1, y1, x2, y2))

def moveDraw(cm, speed=250):
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
      updateParticles(cmAcum * mag, True)
      drawParticles()
      cmAcum = 0

    # Read new enocder values
    a = enc(m1)
    b = enc(m2)
    dif = a - b

    spds = calibrate(speed, speed, dif - normal)
    setSpeed(m1, spds[0])
    setSpeed(m2, spds[1])
    update() 

def rotateDraw(deg, speed=250):
  enableMotor(m1)
  enableMotor(m2)
  update()

  speed1 = -speed if deg > 0 else speed
  speed2 = speed if deg > 0 else -speed
  cnt = 0

  while cnt / encToDeg < mod(deg):
    a = enc(m1)
    b = enc(m2)    

    setSpeed(m1, speed1)
    setSpeed(m2, speed2)
    update()
    
    stepEnc = (mod(a - enc(m1)) +  mod(b - enc(m2))) / 2.0
    cnt += stepEnc

  #print 'rotate'
  rad = (deg * math.pi) / 180 * -1 
  if deg > 0:
    updateParticles(rad, False)
  else:
    updateParticles(rad, False)
  drawParticles()

dist = 40
moveDraw(dist, speed)
rotateDraw(-90)
moveDraw(dist, speed)
rotateDraw(-90)
moveDraw(dist, speed)
rotateDraw(-90)
moveDraw(dist, speed)

