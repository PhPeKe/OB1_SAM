__author__ = 'Sam van Leipsig'
import numpy as np
import cProfile
import pstats

# def get_word_inhibition(norm_inhibition,lexicon_word_activity,lexicon,otherword_index,overlap_list,overlap_list_key):
#     return norm_inhibition * lexicon_word_activity[lexicon[otherword_index]] * overlap_list[overlap_list_key]
          # if complete_selective_word_inhibition:
                        #     if word_inhibition_matrix[word_index,otherword_index] == True:
                        #         overlap_list_key = (word_index, otherword_index)
                        #         lexicon_activewords[word][1] += get_word_inhibition(lexicon_normalized_word_inhibition,lexicon_word_activity,lexicon,otherword_index,word_overlap_matrix,overlap_list_key)
                        # else:
                        #     if word_inhibition_matrix[word_index,otherword_index] == True:
                        #         overlap_list_key = (word_index, otherword_index)
                        #         lexicon_activewords[word][1] += get_word_inhibition(lexicon_normalized_word_inhibition,lexicon_word_activity,lexicon,otherword_index,overlap_list,overlap_list_key)

p = pstats.Stats('myprofile1.stats')
p.sort_stats('tottime').print_stats(50)

lexicon = []
for i in range(0,1500):
    lexicon.append(0)

# mymatrix_int = np.zeros((100,100),dtype=int)
# mymatrix  =  np.zeros((100,100),dtype=bool)
# for i in range(0,100):
#     mymatrix[i,i] = True
#     mymatrix_int[i,i] = 5
# print mymatrix_int[mymatrix]

def make_matrix():
    word_overlap_matrix = np.zeros((len(lexicon),len(lexicon)),dtype=int)
    for other_word in xrange(len(lexicon)):
        for word in xrange(len(lexicon)):
            word_overlap_matrix[word,other_word] = 1
            word_overlap_matrix[word,other_word] = 2
    return word_overlap_matrix

def make_dict():
    overlap_list = {}
    for other_word in xrange(len(lexicon)):
        for word in xrange(int(len(lexicon)/2.)):
            overlap_list[word,other_word] = 1
            overlap_list[word,other_word] = 2
    return overlap_list


def test_matrix(structure):
    counter = 0
    for other_word in xrange(len(lexicon)):
        for word in xrange(len(lexicon)):
            if structure[word,other_word] != 1:
                counter+=1
            else:
                counter-=2
    return structure

def test_dict(structure):
    counter = 0
    for other_word in xrange(len(lexicon)):
        for word in xrange(int(len(lexicon)/2.)):
            if structure[word,other_word] != 1:
                counter+=1
            else:
                counter-=2
    return structure

# one = make_matrix()
# two = make_dict()
# print one.size,len(two)
#
# def run(one, two):
#     #test(one)
#     #test(two)
#     return test_matrix(one),test_dict(two)
#
# # matrix, dictionary = run(one, two)
# # print matrix[10,10]
# # print dictionary[10,10]
# profile = cProfile.run('run(one, two)','structurespeed.stats')
# p = pstats.Stats('structurespeed.stats')
# p.sort_stats('tottime').print_stats(30)


myarray = np.zeros((100),dtype=int)