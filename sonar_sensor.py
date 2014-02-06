from utils import *

s3 = PORT_3
enableSensor(s3, TYPE_SENSOR_ULTRASONIC_CONT)

rangev = [150, 250]

def most_common(lst):
    return max(set(lst), key=lst.count)

def keep_distance(desired, slowStep = 15):
  enableMotor(m1)
  enableMotor(m2)
  update()

  a = enc(m1)
  b = enc(m2)
  vals = []

  normal = a - b
  
  while True:
    # We don't want update to move motors

    # read 5 times sonar sensor
    for i in xrange(0, 5):
      update()
      vals.append( sensor(s3) )
    
    # get the most common out of the last 5 readings
    # this way we discard spike values
    val_sonar = most_common(vals)
    vals = []
    err = val_sonar - desired
    
    if err > slowStep:
      speed = 250 * err
    elif mod(err) <= slowStep and mod(err) > 0.5:
      speed = rangev[0] + (rangev[1] - rangev[0]) / slowStep * mod(err)
      speed = speed if err > 0 else -speed
    else:
      speed = 0 

    # get new encoder values
    a = enc(m1)
    b = enc(m2)
    dif = a - b
  
    #print 'err', err, 'speed', speed, 'dif', dif-normal   

    spds = calibrate(speed, speed, dif - normal)
    #print 'spds', spds  
  
    # move with the desired calibrated speed
    setSpeed(m1, spds[0])
    setSpeed(m2, spds[1])
    update()


keep_distance(30)
