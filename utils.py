# Andrei Antonescu
# Initial Date: January 30, 2014
# Last Updated: January 30, 2014
# 
# We assume we only use two motors PORT_A & PORT_B

from BrickPi import *   #import BrickPi.py file to use BrickPi operations

m1 = PORT_A
m2 = PORT_B
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
  ga = 1 if sa > 0 else -1
  gb = 1 if sb > 0 else -1
  sa = max(sa, -sa)
  sb = max(sb, -sb)
  step = max(dif / 5, -dif / 5)

  if dif > 0:
    ex = min(250 - sb, step)
    sb += ex
    sa = max(50, sa - step + ex)
  elif dif < 0:
    ex = min(250 - sa, step)
    sa += ex
    sb = max(50, sb - step + ex)
  return [sa * ga, sb * gb]

def dist(enc0, enc1):
  return enc1 - enc0 if enc0 < enc1 else enc0 - enc1

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

  while cnt / 42 < cm:
    setSpeed(m1, speed1)
    setSpeed(m2, speed2)
    update()
    cnt += (dist(a, enc(m1)) +  dist(b, enc(m2))) / 2.0
    a = enc(m1)
    b = enc(m2)
    dif = a - b

    spds = calibrate(speed, speed, dif - normal)
    speed1 = spds[0]
    speed2 = spds[1]

    #print dif - normal, speed1, speed2
  
    time.sleep(.1)

def rotate(deg):
  enableMotor(m1)
  enableMotor(m2)
  setSpeed(m1, 0)
  setSpeed(m2, 0)
  update()

  a = enc(m1)
  b = enc(m2)

  normal = a - b
  inispeed1 = -250 if deg > 0 else 250
  inispeed2 = 250 if deg > 0 else -250
  speed1 = inispeed1
  speed2 = inispeed2
  cnt = 0

  while cnt / 6.5 < deg:
    setSpeed(m1, speed1)
    setSpeed(m2, speed2)
    update()
    cnt += (dist(a, enc(m1)) +  dist(b, enc(m2))) / 2.0
    a = enc(m1)
    b = enc(m2)
    dif = a - b
     
    #spds = calibrate(inispeed1, inispeed2, dif - normal)
    #speed1 = spds[0]
    #speed2 = spds[1]
  
    #print dif - normal, speed1, speed2
 
    time.sleep(.1)

"""
while True:
    print "Spin right"
    BrickPi.MotorSpeed[PORT_A] = 200  #Set the speed of MotorA (-255 to 255)
    BrickPi.MotorSpeed[PORT_B] = -200  #Set the speed of MotorB (-255 to 255)
    ot = time.time()
    while(time.time() - ot < 20):    #running while loop for 3 seconds
        BrickPiUpdateValues()       # Ask BrickPi to update values for sensors/motors
        time.sleep(.1)              # sleep for 100 ms
    print "Spin left"
    BrickPi.MotorSpeed[PORT_A] = -200  #Set the speed of MotorA (-255 to 255)
    BrickPi.MotorSpeed[PORT_B] = 200  #Set the speed of MotorB (-255 to 255)
    ot = time.time()
    while(time.time() - ot < 20):    #running while loop for 3 seconds
        BrickPiUpdateValues()       # Ask BrickPi to update values for sensors/motors
        time.sleep(.1)              # sleep for 100 ms
"""
