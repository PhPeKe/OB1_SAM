__author__ = 'Sam van Leipsig'

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def factor(wordlength):
    if wordlength<2:
        return wordlength
    else:
         return wordlength + factor(wordlength-1)

def factor_range(wordlength,bigram_range):
    totalbigrams=0
    for i in range(wordlength,0,-1):
        if i - (bigram_range) > 0:
            totalbigrams+= bigram_range
        else:
            totalbigrams+=(i-1)
    return totalbigrams


mydict = {}
for bigram_range in range(2,14,1):
    mylist2= []
    for wordlength in range(2,14):
        mylist2.append(factor_range(wordlength,bigram_range))
    mydict[bigram_range] = mylist2
df_mydict = pd.DataFrame(mydict)
fig = plt.figure('Number bigrams')
df_mydict.plot(ax = fig.gca(),title='Number bigrams with bigram range')
plt.xlabel('Word length')
plt.ylabel("Number bigrams")
plt.show()