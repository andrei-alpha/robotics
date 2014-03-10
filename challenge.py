from place_rec_bits import *
from moveMCL import *
import os, sys

speed = 150
mymap = Map()
initMap(mymap)
K = 0.000014

points = [(84, 30),
  (180, 30),
  (126, 54),
  (126, 168),
  (30, 54),
  (84, 30),
  (180, 30),
  (126, 54),
  (126, 168),
  (30, 54),
  (84, 30),
  (126, 54)]

'''
for i in range(5):
  print 'Enter a key to learn location', i, '...'
  sys.stdin.read(1)
  learn_location()
'''

print 'Put in a previous learnt location ...'
sys.stdin.read(1)

ret = recognize_location()
#print 'recognize', ret

'''
if ret[1] > 180:
  rotate(360 - ret[1], -250)
else:
  rotate(ret[1], 250)

'''
init_ind = ret[0]
location = points[init_ind]

print 'We are in location', "index ", init_ind, " ", location

angle = ret[1] * math.pi / 180
print 'ANGLE', angle
#rotate(angle,speed)
init_loc = list(location)
particles = Particles((init_loc[0], init_loc[1], angle, 1.0 / NOP))

for i in range(5):
  navigate(points[init_ind + i + 1], particles, speed)
