__author__ = 'Sam van Leipsig'

import numpy as np
import cProfile
import pstats

myarray1 = np.zeros((100),dtype=int)
myarray2 = np.zeros((100),dtype=int)

def create(myarray):
    myarray = np.zeros((100),dtype=int)
    return myarray

def fillthis(myarray):
    myarray =  myarray.fill(1.0)
    return myarray

def run(myarray1,myarray2):
    for i in range(0,100000):
        create(myarray1)
        fillthis(myarray2)
    return myarray1,myarray2

profile = cProfile.run('run(myarray1,myarray2)','zerosspeed.stats')
p = pstats.Stats('zerosspeed.stats')
p.sort_stats('tottime').print_stats(10)