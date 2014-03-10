from place_rec_bits import *
import os, sys

os.system('rm loc_*.dat')

for i in range(5):
  print 'Enter a key to learn location', i, '...'
  sys.stdin.read(1)
  learn_location()

'''
print 'Put in a previous learnt location ...'
sys.stdin.read(1)
recognize_location()

OneDeg = 0.33

error = 0
for i in range(360):
  error = rotate_sonar(1, 250)
  #print error, i
rotate_sonar(360, -250)
'''
