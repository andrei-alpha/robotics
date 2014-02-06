from utils import *

# Put the sensor on the rigth side
# 0 for rigth, 1 for left
side = 0
print 'The sensor needs to be placed on the', 'left' if side else 'right', 'side!'

speed = 200

s3 = PORT_3
enableSensor(s3, TYPE_SENSOR_ULTRASONIC_CONT)

def most_common(lst):
    return max(set(lst), key=lst.count)

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
  
  # read initial value
  normal = most_common(vals)   

  while True:
    # We don't want update to move motors

    # read 5 times sonar sensor
    vals = []
    for i in xrange(0, 6):
      update()
      vals.append( sensor(s3) )
    
    # get the most common out of the last 5 readings
    # this way we discard spike values
    dif = most_common(vals)
    
    spds = calibrate(speed, speed, (dif - normal) * 56)
    print 'spds', spds, 'dif', dif - normal  

    # move with the desired calibrated speed
    if side is 1:
      setSpeed(m1, spds[0])
      setSpeed(m2, spds[1])
    else:
      setSpeed(m1, spds[1])
      setSpeed(m2, spds[0])    
    update()

keep_wall()
