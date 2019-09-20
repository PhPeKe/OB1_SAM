__author__ = 'Sam van Leipsig'

import parameters as pm
import matplotlib.pyplot as plt

frequency_effect =  1. - (36./121.)
predictability_effect =  1. - (18./121.)
print frequency_effect,predictability_effect

def get_threshold(word,word_frequency,max_frequency,word_predictability):
    word_frequency_multiplier = ((3.4 * max_frequency) - word_frequency) / (3.4 * max_frequency)
    word_predictability_multiplier = ((6.7 * 1.) - word_predictability) / (6.7 * 1.)
    print word_frequency_multiplier,word_predictability_multiplier
    #print word_frequency_multiplier * word_predictability_multiplier * (0.04 * len(word))

get_threshold('letters',0,6,0.96)


def get_threshold2(len_effect,wordlen,wordadd,word_frequency,max_frequency,word_predictability):
    word_frequency_multiplier = ((2.5 * max_frequency) - word_frequency) / (2.5 * max_frequency)
    word_predictability_multiplier = ((6.7 * 1.) - word_predictability) / (6.7 * 1.)
    # print word_frequency_multiplier,word_predictability_multiplier
    # print word_frequency_multiplier  * (0.04 * wordlen)
    return word_frequency_multiplier  * (len_effect * wordlen) + wordadd

mylist= [0.02,0.03,0.04]
myadd = [0.1,0.0,0.0]
for x in range(len(mylist)):
    toplot = []
    for i in range(2,15):
        toplot.append(get_threshold2(mylist[x],i,myadd[x],5,6,1))
    plt.plot(toplot)
plt.show()
#get_threshold2('letters',6,6,1)

# Make scaled predictions -> before
# scaled_pred = {}
# for i,word in enumerate(individual_words):
#     try:
#         pred = word_pred_dict[word]
#         scaled_pred[word] = ((pred - min_predictability) / (max_predictability - min_predictability))
#         scaled_pred[word] = scaled_pred[word] * (1 - 0.9) + 0.9
#         print word
#     except KeyError:
#         pass