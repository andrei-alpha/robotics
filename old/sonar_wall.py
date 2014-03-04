from utils import *

# Put the sensor on the right side
# 0 for right, 1 for left
side = 1
mag = 15
print 'The sensor needs to be placed on the', 'left' if side else 'right', 'side!'

speed = 100

s3 = PORT_3
enableSensor(s3, TYPE_SENSOR_ULTRASONIC_CONT)

def calib(speed, dif):
  mdif = mod(dif)
  sa = speed
  sb = speed  

  if dif > 0:
    sa -= mag * mdif
    sb += mag * mdif
  elif dif < 0:
    sa += mag * mdif
    sb -= mag * mdif
  return [ int(sa), int(sb)]

def keep_wall():
  enableMotor(m1)
  enableMotor(m2)
  update()

  a = enc(m1)
  b = enc(m2)
  
  vals = []
  for i in xrange(0, 10):
    update()
    vals.append( sensor(s3) )
  '''
  # read initial value
  normal = median(vals)   
  '''
  normal = 30
  lastDif = normal
  changeTime = 0
  trackOverTurn = 0

  while True:
    changeTime += 1
    
    # We don't want update to move motors

    # read 5 times sonar sensor
    vals = []
    for i in xrange(0, 5):
      update()
      vals.append( sensor(s3) )
    
    # get the most common out of the last 5 readings
    # this way we discard spike values
    dif = most_common(vals)
    
    if trackOverTurn < 30:
      if dif is 0 or mod(dif) < mod(lastDif) or changeTime < 7:
        spds = [speed, speed]
      else:
        changeTime = 0
        spds = calib(speed, dif - normal)
        if dif > 30:
          trackOverTurn += 1
        else:
          trackOverTurn = 0
      print 'spds', spds, 'dif', dif, 'dif - normal', dif - normal  
    else:
      trackOverTurn = 0
      print 'else code'
      setSpeed(m1, spds[1 - side] + 15)
      setSpeed(m2, spds[side] - 15)
      
    
    # move with the desired calibrated speed
    if side is 1:
      setSpeed(m1, spds[0])
      setSpeed(m2, spds[1])
    else:
      setSpeed(m1, spds[1])
      setSpeed(m2, spds[0])    
    update()
    lastDif = dif

keep_wall()
