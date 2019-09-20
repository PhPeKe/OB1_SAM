__author__ = 'Sam van Leipsig'

import numpy as np
import matplotlib.pyplot as plt
import math
import cProfile
import pstats
import parameters as pm

this = 5
this2 = "strigng"
this34= 3453453

def my_print(*args):
    if pm.print_all:
        for i in args:
            print i,
        print

my_print(this,this2,this34)
my_print(this,this2,this34)

x_values = np.arange(1,15,1.)

mylist = []
mylist2 = []
mylist3 = []
for i,x in enumerate(x_values):
    mylist.append(0.135 - (0.2*(math.exp(-0.42*x))))
    mylist2.append(0.135 - (0.21*(math.exp(-0.43*x))))
    #mylist.append(0.145 - (0.2*(math.exp(-0.8*x))))
    #mylist2.append(0.06 +(0.006*i))
    #mylist2.append(0.145 - (0.22*(math.exp(-0.8*x))))
    #mylist3.append(mylist2[i]-mylist[i])
plt.xlim(2,15)
plt.ylim(0.07,0.15)
plt.plot(mylist,'b')
plt.plot(mylist2, 'g--')
plt.plot(mylist3, 'r--')
plt.show()

euler = math.e
# this= np.zeros((50,2),dtype=int)
# this[49,1]=10
# print this
def nonlinear(x_values):
    mylist = []
    for i in x_values:
        mylist.append(0.14 - (0.13*(math.exp(-0.2*i))))
    return mylist

def nonlinear2(x_values,euler):
    mylist = []
    for i in x_values:
        mylist.append(0.14 - (0.13*(euler**(-0.2*i))))
    return mylist

def linear(x_values):
    mylist2 = []
    for i in x_values:
        mylist2.append(0.06 +(0.006*i))
    return mylist2

def run(x_values,euler):
    #test(one)
    #test(two)
    return nonlinear(x_values),linear(x_values),nonlinear2(x_values,euler)

profile = cProfile.run('run(x_values,euler)','thresholdspeed.stats')
p = pstats.Stats('thresholdspeed.stats')
p.sort_stats('tottime').print_stats(30)




#should always ensure that the maximum possible value of the threshold doesn't exceed the maximum allowable word activity
def get_threshold(word,word_freq_dict,max_frequency,word_pred_dict,freq_p,pred_p,len_p,start_p):
    word_frequency_multiplier = 1 # from 0-1, inverse of frequency
    word_predictability_multiplier = 1
    if pm.frequency_flag:
        try:
            word_frequency = word_freq_dict[word]
            word_frequency_multiplier = ((freq_p * max_frequency) - word_frequency) / (freq_p * max_frequency)
        except KeyError:
            pass
    if pm.prediction_flag:
        max_predictability = 1.
        try:
            word_predictability = word_pred_dict[word]
            word_predictability_multiplier = ((pred_p * max_predictability) - word_predictability) / (pred_p * max_predictability)
        except KeyError:
            pass

    #return (word_frequency_multiplier * word_predictability_multiplier) * (len_p * len(word)) + start_p
    return (word_frequency_multiplier * word_predictability_multiplier) * (0.128 - (0.15*(math.exp(-0.3*len(word)))))


