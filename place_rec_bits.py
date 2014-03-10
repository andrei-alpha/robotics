#!/usr/bin/env python
# By Jacek Zienkiewicz and Andrew Davison, Imperial College London, 2014
# Based on original C code by Adrien Angeli, 2009

from utils import *
from particleDataStructure import *
import random
import math
import os

s3 = PORT_3
enableSensor(s3, TYPE_SENSOR_ULTRASONIC_CONT)
magDrawLine = 2
sonar_speed = 170
rotate_speed = 80 
ERROR = 1000000

# Location signature class: stores a signature characterizing one location
class LocationSignature:
    def __init__(self, no_bins = 360):
        self.sig = [0] * no_bins
        self.freq = [0] * 256
        
    def print_signature(self):
        for i in range(len(self.sig)):
            print self.sig[i]

# --------------------- File management class ---------------
class SignatureContainer():
    def __init__(self, size = 5):
        self.size      = size; # max number of signatures that can be stored
        self.filenames = [];
        
        # Fills the filenames variable with names like loc_%%.dat 
        # where %% are 2 digits (00, 01, 02...) indicating the location number. 
        for i in range(self.size):
            self.filenames.append('loc_{0:02d}.dat'.format(i))

    # Get the index of a filename for the new signature. If all filenames are 
    # used, it returns -1;
    def get_free_index(self):
        n = 0
        while n < self.size:
            if (os.path.isfile(self.filenames[n]) == False):
                break
            n += 1
            
        if (n >= self.size):
            return -1;
        else:    
            return n;
 
    # Delete all loc_%%.dat files
    def delete_loc_files(self):
        print "STATUS:  All signature files removed."
        for n in range(self.size):
            if os.path.isfile(self.filenames[n]):
                os.remove(self.filenames[n])
            
    # Writes the signature to the file identified by index (e.g, if index is 1
    # it will be file loc_01.dat). If file already exists, it will be replaced.
    def save(self, signature, index):
        filename = self.filenames[index]
        if os.path.isfile(filename):
            os.remove(filename)
            
        f = open(filename, 'w')

        for i in range(len(signature.sig)):
            s = str(signature.sig[i]) + "\n"
            f.write(s)
        f.close();

    # Read signature file identified by index. If the file doesn't exist
    # it returns an empty signature.
    def read(self, index):
        ls = LocationSignature()
        filename = self.filenames[index]
        if os.path.isfile(filename):
            f = open(filename, 'r')
            for i in range(len(ls.sig)):
                s = f.readline()
                if (s != ''):
                    ls.sig[i] = int(s)
                    ls.freq[ int(s) ] += 1
            f.close();
        else:
            print "WARNING: Signature does not exist."
            ls.sig = [999] * 360
            ls.freq = [50] * 256
        
        return ls
        
# FILL IN: spin robot or sonar to capture a signature and store it in ls
def characterize_location(ls):
  enableMotor(m3)
  setSpeed(m3, 0)
  update()  

  c = enc(m3)
  cnt = 0.0
  cntAcum = 0
  ind = 0

  while cnt / encToDegSonar < 360:
    setSpeed(m3, rotate_speed)
    update()
    setSpeed(m3, 0)

    cnt += mod(c - enc(m3)) * 1.0
    cntAcum += mod(c - enc(m3)) * 1.0
    c = enc(m3)
    #print 'total', cnt / encToDegSonar, 'acum', cntAcum / encToDegSonar  

    if cntAcum / encToDegSonar >= 1.0:
      cntAcum -= encToDegSonar
      update()
      reading = sensor(s3)
      ls.sig[ind] = sensor(s3)
      ls.freq[ sensor(s3) ] += 1
      #print ls.sig[ind]
      #time.sleep(.5)
      ind = ind + 1
    """
    x1 = 500 + ls.sig[i]*math.cos(i * rad) * magDrawLine
    y1 = 300 + ls.sig[i]*math.sin(i * rad) * magDrawLine
    #print "x1", x1
    #print "y1", y1
    x1 = max(x1, 0)
    y1 = max(y1, 0)
    line = (500, 300, int(x1), int(y1))
    print "drawLine:" + str(line)
    """
  #print ls.sig

  setSpeed(m3, 0)
  update()
  #rotate_sonar(360, -sonar_speed)

# This function compare two signatures
def compare_signatures(ls1, ls2):
    dist = 999999999
    
    for i in range(360):
      sum = 0
      for j in range(360):
        a = ls1.sig[j]
        b = ls2.sig[(i + j) % 360]
        if a > 170 or b > 170:
          continue
        #  a = 0
        #if b > 170:
        #  b = 0
        sum += pow(a - b, 2)  
      dist = min(dist, sum)
    '''
    sum = 0
    for i in range(170):
      sum += pow(ls1.freq[i] - ls2.freq[i], 2)
    dist = min(dist, sum)
    '''
    #sum1 = sum(ls1.freq[i] * i for i in xrange(256))
    #sum2 = sum(ls2.freq[i] * i for i in xrange(256))
          
    return dist

# This function gets the angle of best match of two signatures
def angle_signatures(ls1, ls2):
  dist = 99999999
  angle = 0

  for i in range(360):
    sumx = 0
    for j in range(360):
       a = ls1.sig[j]
       b = ls2.sig[(i + j) % 360]
       if a > 170 or b > 170:
         continue
       sumx += pow(a - b, 2)   
    if sumx < dist:
      angle = i
      dist = sumx
  return angle

# This function characterizes the current location, and stores the obtained 
# signature into the next available file.
def learn_location():
    ls = LocationSignature()
    characterize_location(ls)
    idx = signatures.get_free_index();
    if (idx == -1): # run out of signature files
        print "\nWARNING:"
        print "No signature file is available. NOTHING NEW will be learned and stored."
        print "Please remove some loc_%%.dat files.\n"
        return
    
    signatures.save(ls,idx)
    print "STATUS:  Location " + str(idx) + " learned and saved."

# This function tries to recognize the current location.
# 1.   Characterize current location
# 2.   For every learned locations
# 2.1. Read signature of learned location from file
# 2.2. Compare signature to signature coming from actual characterization
# 3.   Retain the learned location whose minimum distance with
#      actual characterization is the smallest.
# 4.   Display the index of the recognized location on the screen
def recognize_location():
    ls_obs = LocationSignature();
    characterize_location(ls_obs);

    print 'Observed'
    print ls_obs.sig

    loc = [9999999, 0]
    # FILL IN: COMPARE ls_read with ls_obs and find the best match
    for idx in range(signatures.size):
        print "STATUS:  Comparing signature " + str(idx) + " with the observed signature."
        ls_read = signatures.read(idx);
        dist    = compare_signatures(ls_obs, ls_read)
        print 'Error for', idx, ' of', dist
        if dist < loc[0]:
          loc = [dist, idx]

    ls_read = signatures.read(loc[1])
    if loc[0] < ERROR:
      angle = angle_signatures(ls_obs, ls_read)
      print 'We are in location %d with angle %d' % (loc[1], angle)
      return [loc[1], angle]
    else:
      print 'No good match'
      return [-1, -1]       

# Prior to starting learning the locations, it should delete files from previous
# learning either manually or by calling signatures.delete_loc_files(). 
# Then, either learn a location, until all the locations are learned, or try to
# recognize one of them, if locations have already been learned.

signatures = SignatureContainer(5);
#signatures.delete_loc_files()

#learn_location();
#recognize_location();


