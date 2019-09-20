__author__ = 'SAM'

import math
import matplotlib.pyplot as plt
from scipy.stats import rv_continuous as norm
from scipy import linspace
from scipy import pi,exp,sqrt
from scipy.special import erf
import numpy as np
import pandas as pd

import sys;



#print("%x" % sys.maxsize, sys.maxsize > 2**32)

# min =2.
# max= 14.
# print  ((1-0.2) * (2 - min)) / (max-min) + 0.2

# for letter_index_reversed in xrange(0,20,1):
#     print letter_index_reversed,20-letter_index_reversed

attention_eccentricity = np.arange(0,18,0.5)
attention_eccentricity1 = np.arange(0,18,0.5)
attention_eccentricity2 = linspace(-10,10,2**10)
attentionWidth = [4.0,]  #np.arange(2,6,1.)

letPerDeg = .35
def visualAccuity1(attention_eccentricity1):
    return (1/35.555556)/(0.018*(attention_eccentricity1*letPerDeg+1/0.64))

# letPerDeg1 = .3
# def visualAccuity2(attention_eccentricity1):
#     return (1/35.555556)/(0.018*(attention_eccentricity1*letPerDeg1+1/0.64))


def get_attention_right(attentionWidth,attention_eccentricity):
    #attention_eccentricity-=11.5
    attention = 1/(attentionWidth)*math.exp(-(pow(attention_eccentricity,2))/(2*pow(attentionWidth,2)))+0.25
    return attention

def get_attention_left(attentionWidth,attention_eccentricity):
    attention_eccentricity-=10.
    attention = 1/(attentionWidth)*math.exp(-(pow(attention_eccentricity,2))/(2*pow(attentionWidth,2)))+0.25
    return attention


# df_attention1 = pd.DataFrame(index=attention_eccentricity)
# df_attention2 = pd.DataFrame(index=attention_eccentricity1)
df_attention1 = pd.DataFrame(attention_eccentricity)
df_attention2 = pd.DataFrame(attention_eccentricity1)

for width in attentionWidth:
    attention_list1 = []
    attention_list2 = []
    acuity_list1 = []
    acuity_list2 = []
    combined1 = []
    combined2 = []
    for i in attention_eccentricity:
        attention_list1.append(get_attention_right(width,i))
        attention_list2.append(get_attention_left(width,i))
        combined1.append(get_attention_right(width,i)*visualAccuity1(i))
        combined2.append(get_attention_left(width,i)*visualAccuity1(i))
    df_attention1.loc[:,"Att right " + str(width)] = attention_list1
    df_attention2.loc[:,"Att left " + str(width)] = attention_list2
    df_attention1.loc[:,"Att*Ac right" + str(width)] = combined1
    df_attention2.loc[:,"Att*Ac left " + str(width)] = combined2 #+ str(width)


df_attention1.set_index(0)
print df_attention1
# df_attention2.loc[:,0] = df_attention2.loc[:,0]*-1
# df_attention2.set_index(0)
#df_attention2.loc[:,[2,3,4,5]] = df_attention2.loc[:,[2,3,4,5]]*-1
#fig, axes = plt.subplots(nrows=2, ncols=2)
ax = df_attention1.plot(x=[0],style = ['b','b--','g','g--'],title = ("Attentional width" + str(width)))
df_attention2.plot(x=[0],ax=ax,style = ['b','b--','g','g--'])
plt.ylim(0,.5)
plt.ylabel('Strength')
plt.xlabel('Eccentricity')
plt.show()


# def skew(x,e=0,w=1,a=0):
#     t = (x-e) / w
#     return 2 * norm.pdf(t) * norm.cdf(a*t)

def pdf(x):
    return 1/sqrt(2*pi) * exp(-x**2/2)

def cdf(x):
    return (1 + erf(x/sqrt(2))) / 2

def skew(x,e=0,w=1,a=0):
    t = (x-e) / w
    return 2 / w * pdf(t) * cdf(a*t)

# skewd = skew(attention_eccentricity,1,2,1)
# print attention_eccentricity
# plt.plot(attention_eccentricity,skewd)
# plt.show()
