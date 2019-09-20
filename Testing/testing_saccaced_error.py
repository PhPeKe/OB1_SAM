__author__ = 'Sam van Leipsig'

import parameters as pm
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def calc_saccade_error(saccade_distance):
    #TODO include fixdur, as in EZ and McConkie
    sacc_optimal_distance2, saccErr_scaler2, saccErr_sigma2, saccErr_sigma_scaler2 = pm.sacc_optimal_distance, pm.saccErr_scaler, pm.saccErr_sigma, pm.saccErr_sigma_scaler
    saccade_error = (sacc_optimal_distance2 - abs(saccade_distance)) * saccErr_scaler2
    saccade_error_sigma = saccErr_sigma2 + (abs(saccade_distance) * saccErr_sigma_scaler2)
    saccade_error_norm = np.random.normal(saccade_error,saccade_error_sigma)
    if pm.use_saccade_error:
        return saccade_error_norm
    else:
        return 0.

#saccade_distance = np.arange(1,20,0.1)
mylist= []
for i in range(1,6,1):
    saccade_distance = np.empty(100)
    saccade_distance.fill(float(i))
    if i>12:
        print np.sum(np.asarray(calc_saccade_error(saccade_distance))>1.0)
    mylist.append(calc_saccade_error(saccade_distance).mean())

plt.figure("sacc err")
plt.plot(mylist)
plt.show()