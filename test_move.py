from moveMCL import *
import os, sys

speed = 100
mymap = Map()
initMap(mymap)
K = 0.000014

points = [(0, 0),
  (40, 0),
  (0, 0),
  (40, 0),
  (0, 0)]

init_ind = 0
angle = 0
location = points[init_ind]

print 'We are in location', "index ", init_ind, " ", location

init_loc = list(location)
particles = Particles((init_loc[0], init_loc[1], angle, 1.0 / NOP))

for i in range(2):
  navigate(points[init_ind + i + 1], particles, speed)
