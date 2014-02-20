from particleDataStructure import *

import random

def set_weight(particle, new_weight):
  part = list(particle)
  part[3] = new_weight
  return tuple(part)

def normalise_particle(particle, total_weight):
  return set_weight(particle, particle[3] / total_weight)

def normalise(particles):
  total_weight = 0
  for particle in particles:
    total_weight += particle[3]
  particles = map(lambda particle: normalise_particle(particle, total_weight), particles)
  return particles

def getRandomArray(particles):
  return map(lambda x: random.random(), range(NOP))
   
# Returns position of the particle to be copied.
def search_particle(cumulative_weight, random_num):
  for i in range(len(cumulative_weight)):
    if cumulative_weight[i] >= random_num:
      return i
      
def sampling(particles):
  sum_weight = 0
  cumulative_weight = []
  for particle in particles:
    sum_weight += particle[3]
    cumulative_weight.append(sum_weight)
#  cumulative_weight = map(lambda particle: particle[3] +
  
  random_array = getRandomArray(particles)
  new_set = []
  for random_num in random_array:
    pos = search_particle(cumulative_weight, random_num)
    new_set.append(set_weight(particles[pos], 1.0 / NOP))

  particles = new_set
  return particles

