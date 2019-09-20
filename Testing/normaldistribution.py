__author__ = 'SAM'
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import math
# plt.figure()
# plt.plot(range(0,10),range(0,10))
# plt.show()
value=1.5
mu = 5.
sigma = 2.

normal = []
for i in range(0,400):
    normal.append(np.random.normal(mu,sigma))
plt.figure(1)
plt.hist(normal,bins=20,alpha=0.3)

mu -= value
sigma = 1.9

normal = []
for i in range(0,400):
    normal.append(np.random.normal(mu,sigma))
plt.hist(normal, bins=20,alpha=0.3)
plt.show()
# s = np.random.normal(mu,sigma,100)
# count, bins, ignored = plt.hist(s, 30, normed=True)
# plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins - mu)**2 / (2 * sigma**2) ),linewidth=2, color='r')
# plt.show()

#print stats.skew(s)
# for i in range(0,10):
#     print int(np.random.normal(mu,sigma,1))
#
# np.random.normal(mu,sigma,1)
# np.random.uniform(6,12,1)
#
# print round(1.4,0), round(1.6,0)


# from scipy import linspace
# from scipy import pi,sqrt,exp
#
# from pylab import plot,show
#
# def skew(x,e=0,w=1,a=0):
#     t = (x-e) / w
#     return 2 * stats.norm.pdf(t) * stats.norm.cdf(a*t)
#
#
# def make_skewed_distribution():
#     n = 1000
#     e = 8 # location
#     w = 2.0 # scale
#     x = linspace(0,15,n)
#     p = skew(x,e,w,8)
#     return p
#
# distribution = make_skewed_distribution()
# def select_from_skew(distribution):
#     plt.plot(distribution)
#     plt.show()
#
# select_from_skew(distribution)