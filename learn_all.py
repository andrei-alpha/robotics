from place_rec_bits import *
import sys

for i in xrange(5):
  learn_location()
  print 'Enter a key to continue...'
  sys.stdin.read(1)
