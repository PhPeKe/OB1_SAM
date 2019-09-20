import codecs
import re
import chardet
from unidecode import unidecode
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import math

filepath = "texts/PSC_short.txt"

# # Detect text encoding
# rawdata=open("PSC.txt","r").read()
# print chardet.detect(rawdata)


# mylist = []
# for i in range(0,100):
#     mylist.append(math.pow(i,0.5))
# plt.plot(mylist)
# plt.show()
#
def is_similar_word_length(word1,word2):
    return abs(len(word1)-len(word2)) < (0.2* max(len(word1),len(word2)))
print is_similar_word_length('123456789','12345678911')

#
# wordlength = 15
# is_similar_dict = {}
# for x in range(1,wordlength ,1):
#     templist = []
#     for i in range(1,wordlength ,1):
#         templist.append(is_similar_word_length(x*'A',i*'A'))
#     is_similar_dict[x] = templist
#
# df_issimilar = pd.DataFrame(is_similar_dict)
# print df_issimilar
# plt.plot(df_issimilar.sum(axis=1))
# plt.show()




def get_stimulus_text_from_file(filepath):
    with codecs.open(filepath, encoding = 'ISO-8859-1', errors ='strict') as text_to_read:
        textfile = text_to_read.readline().lower()
        #textfile  = textfile.encode("utf-8", errors="strict")
        #textfile_clean = textfile.decode("ISO-8859-1",errors = "strict")
        #textfile = unidecode(textfile)

        # remove non-alphabet_numeric symbols
        #textfile_clean = re.sub('([^\s\w]|_)+', '', textfile)
        my_re = re.compile('([^\s\w]|_)+', re.UNICODE)
        textfile_clean = my_re.sub('', textfile)
        mylist = textfile_clean.split(" ")
        print mylist[14]
    return textfile_clean


# def bin_freq(x):
#     return min(freqbins, key=lambda nr:abs(nr-(math.ceil(x)+0.01)))
#get_stimulus_text_from_file(filepath)

#re.sub('[\W_]', '', string.printable)
#re.sub(r'[^a-zA-Z0-9\[\]]',' ', text)
#'([^\s\w]|_)+'


# __author__ = 'SAM'
# import pickle
#
# output_word_frequency_map = "frequency_map.dat"
# with open (output_word_frequency_map,"r") as f:
#     word_freq_dict = pickle.load(f)
#
# print word_freq_dict
#
#
# __author__ = 'SAM'
#
# # word_freq_dict = all words as key and relative frequency as value
# # individual_words = list with all words (unicode)
# # Lexicon =
# # lexicon_word_bigrams = key is word and values are all the bigrams
# # word_inhibition_matrix = calculate overlap with other words for bigram and monogram, set true if any overlap
# # Fixation = position of current fixated word
# # allbigram/allmonograms = increase with movement of stimulus
# # bigramsTOlocations = all bigrams als key and all the locations (i of words) as the values
#
# # unitactivations are the activations of the seperate monograms/bigrams
#
# # Changed enumerate in is_new_word_recognised
# # Changed max_frequency, removed global
#
# import timeit,pickle
# global frequency_flag
# global word1,max_frequency1
# frequency_flag = True
#
# output_word_frequency_map = "frequency_map.dat"
# with open(output_word_frequency_map, "r") as f:
#     word_freq_dict = pickle.load(f)
# word = 'you'
# word1 = 'you'
# max_frequency_key = max(word_freq_dict, key=word_freq_dict.get)
# max_frequency = word_freq_dict[max_frequency_key]
# max_frequency1 = word_freq_dict[max_frequency_key]
#
# def get_threshold(word,max_frequency):
#     word_frequency_multiplier = 1
#     if frequency_flag and word in word_freq_dict.keys():
#         word_frequency = word_freq_dict[word]
#         word_frequency_multiplier = ((2 * max_frequency) - word_frequency) / (2 * max_frequency)
#
#     return word_frequency_multiplier * (0.03 * len(word) + 0.03)
#
# def get_threshold2(word,max_frequency):
#     word_frequency_multiplier = 1
#     if frequency_flag:
#         try:
#             word_frequency = word_freq_dict[word]
#             word_frequency_multiplier = ((2 * max_frequency) - word_frequency) / (2 * max_frequency)
#         except KeyError:
#             pass
#
#     return word_frequency_multiplier * (0.03 * len(word) + 0.03)
#
#
# if __name__ == '__main__':
#     import timeit
#     print(timeit.timeit("get_threshold(word,max_frequency)", setup="from __main__ import get_threshold, word, max_frequency",number=1000000))
#     print(timeit.timeit("get_threshold2(word,max_frequency)", setup="from __main__ import get_threshold2, word, max_frequency",number=1000000))
#     #print(timeit.timeit(function_name,number=1000000))
#
#
# def wrapper(func, *args, **kwargs):
#     def wrapped():
#         return func(*args, **kwargs)
#     return wrapped

