# Andrei Antonescu
# Initial Date: January 30, 2014
# Last Updated: January 30, 2014
# 
# We assume we only use two motors PORT_A & PORT_B

from BrickPi import *   #import BrickPi.py file to use BrickPi operations

m1 = PORT_A
m2 = PORT_B
encToCm = 53.03 # 42
encToDeg = 6.88 # 6.05
difRot = 5.6 # 5.6
BrickPiSetup()  # setup the serial port for communication

BrickPiSetupSensors()   #Send the properties of sensors to BrickPi

def enableMotor(m):
  BrickPi.MotorEnable[m] = 1

def disableMotor(m):
  BrickPi.MotorEnable[m] = 0
  
def setSpeed(m, speed=250):
  BrickPi.MotorSpeed[m] = speed

def update():
  BrickPiUpdateValues()

def enc(m):
  return BrickPi.Encoder[m]

def calibrate(sa, sb, dif, step=5):
  dif = int(dif)
  ga = 1 if sa > 0 else -1
  gb = 1 if sb > 0 else -1
  sa = max(sa, -sa)
  sb = max(sb, -sb)
  step = max(dif / 5, -dif / 5)

  if dif > 0:
    ex = min(250 - sb, step)
    sb += ex
    sa = max(30, sa - step + ex)
  elif dif < 0:
    ex = min(250 - sa, step)
    sa += ex
    sb = max(30, sb - step + ex)
  return [sa * ga, sb * gb]

def distMod(enc0, enc1):
  return enc1 - enc0 if enc0 < enc1 else enc0 - enc1

def mod(x):
  return x if x > 0 else -x

def move(cm, speed):
  enableMotor(m1)
  enableMotor(m2)
  setSpeed(m1, 0)
  setSpeed(m2, 0)
  update()

  a = enc(m1)
  b = enc(m2)
  
  normal = a - b
  speed1 = speed
  speed2 = speed
  cnt = 0

  while cnt / encToCm < cm:
    setSpeed(m1, speed1)
    setSpeed(m2, speed2)
    update()
    cnt += (mod(a - enc(m1)) +  mod(b - enc(m2))) / 2.0
    a = enc(m1)
    b = enc(m2)
    dif = a - b

    spds = calibrate(speed, speed, dif - normal)
    speed1 = spds[0]
    speed2 = spds[1]

    print dif - normal, speed1, speed2, '#', cnt
 
  setSpeed(m1, 0)
  setSpeed(m2, 0)
  update()
  return cnt / encToCm - cm

def rotate(deg, speed):
  enableMotor(m1)
  enableMotor(m2)
  setSpeed(m1, 0)
  setSpeed(m2, 0)
  update()

  a = enc(m1)
  b = enc(m2)

  normal = a - b
  step = -difRot if deg > 0 else difRot
  inispeed1 = -speed if deg > 0 else speed
  inispeed2 = speed if deg > 0 else -speed
  deg = mod(deg)
  speed1 = inispeed1
  speed2 = inispeed2
  cnt = 0

  while cnt / encToDeg < deg:
    setSpeed(m1, speed1)
    setSpeed(m2, speed2)
    update()
    cnt += (mod(a - enc(m1)) +  mod(b - enc(m2))) / 2.0
    a = enc(m1)
    b = enc(m2)
    dif = a - b

    # Expected increase
    #normal += step
    #spds = calibrate(inispeed1, inispeed2, dif - normal)
    #speed1 = spds[0]
    #speed2 = spds[1]
  
    #print normal, dif, speed1, speed2
 
  setSpeed(m1, 0)
  setSpeed(m2, 0)
  update()
  return cnt / encToDeg - deg
