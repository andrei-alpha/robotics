from utils import *

s3 = PORT_3
enableSensor(s3, TYPE_SENSOR_ULTRASONIC_CONT)

while True:
  update()
  print '#read', sensor(s3)
  time.sleep(1)
