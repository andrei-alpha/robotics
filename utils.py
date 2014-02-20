# Andrei Antonescu
# Initial Date: January 30, 2014
# Last Updated: February 18, 2014
# 
# We assume we only use two motors PORT_A & PORT_B

from BrickPi import *   #import BrickPi.py file to use BrickPi operations
import math

eps = 1e-8
m1 = PORT_A
m2 = PORT_B
encToCm = 53.03 # 42
encToDeg = 6.88 # 6.05
difRot = 5.6 # 5.6
BrickPiSetup()  # setup the serial port for communication
BrickPiSetupSensors()   #Send the properties of sensors to BrickPi

def enableSensor(s, stype):
  BrickPi.SensorType[s] = stype
  BrickPiSetupSensors()

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

def sensor(s):
  return BrickPi.Sensor[s]

def calibrate(sa, sb, dif, step=5):
  dif = int(dif)
  ga = 1 if sa > 0 else -1
  gb = 1 if sb > 0 else -1
  if sa < 0 and sb < 0:
    dif *= -1
  sa = mod(sa)
  sb = mod(sb)
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

def dist(x1, y1, x2, y2):
  return math.sqrt( (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2) )

# Returns the distance from a point to a wall segment
def intersect(wall, x, y, theta):
  a = (wall[3] - wall[1]) * (wall[0] - x) - (wall[2] - wall[0]) * (wall[1] - y)
  b = (wall[3] - wall[1]) * math.cos(theta) - (wall[2] - wall[0]) * math.sin(theta)
  m = a / (b if b != 0 else 1e-14)
  
  # If m is less than zero the intersection is behind
  if m < 0:
    return 9999999
  xi = x + m * math.cos(theta)
  yi = y + m * math.sin(theta)

  #Check if the intersection point lies on the line segment
  if xi < min(wall[0],wall[2]) - eps or xi > max(wall[0],wall[2]) + eps:
    return 9999999
  if yi < min(wall[1],wall[3]) - eps or yi > max(wall[1],wall[3]) + eps:
    return 9999999
  return m

# Returns the incidence angle from a point to a wall segment
def incidence(wall, x, y, theta):
  a = math.cos(theta) * (wall[1] - wall[3]) + math.sin(theta) * (wall[2] - wall[0])
  b = math.sqrt( (wall[1] - wall[3]) * (wall[1] - wall[3]) + (wall[2] - wall[0]) * (wall[2] - wall[0]) )
  return math.acos(a / b)
'''
  # Oy parallel wall
  if wall[0] == wall[2]:
    if abs(theta) < math.pi / 2.0:
      return abs(theta)
    else:
      return math.pi - abs(theta)
  # Ox parallel wall
  if abs(theta) < math.pi / 2.0:
    return math.pi / 2.0 - abs(theta)
  return math.pi - abs(theta)
'''

def most_common(lst):
  return max(set(lst), key=lst.count)

def median(lst):
  lst.sort()
  length = len(lst)
  if length % 2:
    return lst[length / 2 + 1]
  return lst[length / 2] * 0.5 + lst[length / 2 + 1] * 0.5

def move(cm, speed, obstacle=False):
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
  ind = 0
  cnt = 0
  sumLastEnc = 0.0
  
  while cnt / encToCm < cm:
    ind += 1
    setSpeed(m1, speed1)
    setSpeed(m2, speed2)
    update()
    
    # get new encoder values

    stepEnc = (mod(a - enc(m1)) +  mod(b - enc(m2))) / 2.0
    sumLastEnc += stepEnc
    cnt += stepEnc

    # Try to guess if something is going wrong
    if obstacle == True and ind % 10 == 0:
      meanEnc = sumLastEnc / 10.0
      sumLastEnc = 0.0
      print meanEnc, cnt / ind, stepEnc
      if meanEnc < (cnt / ind) * 0.8:
        return -1

    # Replace old encoder values
    a = enc(m1)
    b = enc(m2)
    dif = a - b

    spds = calibrate(speed, speed, dif - normal)
    speed1 = spds[0]
    speed2 = spds[1]

    #print dif - normal, speed1, speed2, '#', stepEnc
 
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

