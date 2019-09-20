import matplotlib
#matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import pickle
from reading_common import get_stimulus_text_from_file
import pdb
import pandas as pd

#function to get all indices of a value from a list
def all_indices(value, qlist):
    indices = []
    idx = -1
    while True:
        try:
            idx = qlist.index(value, idx+1)
            indices.append(idx)
        except ValueError:
            break
    return indices

#deletes from a list values at specified indexes indices
def multi_delete(list_, indexes_to_delete):
    indexes = sorted(indexes_to_delete, reverse=True)
    for index in indexes:
        del list_[index]
    return list_

def draw_boxplot(classes_array,values_array):
    unique_classes = np.unique(classes_array)

    boxplot_values_list = []
    for class_name in unique_classes:
        indexes = all_indices(class_name,classes_array)
        values = []
        for value_index in indexes:
            values.append(values_array[value_index])

        boxplot_values_list.append(values)

    # pdb.set_trace()
    plt.boxplot(boxplot_values_list)
    plt.xticks(unique_classes)
    plt.ylim(max( min(values_array) *0.8, 0), max(values_array)*1.25)

def get_results(input_text_filename,input_file_all_data,input_file_unrecognized_words):
    textfile=get_stimulus_text_from_file('PSC/'+input_text_filename + '.txt')

    individual_words = []
    textsplitbyspace = textfile.split(" ")
    for word in textsplitbyspace:
        if word.strip()!="":
            individual_words.append(word.strip())

    #this vector stores the total fixation time at each position
    fixation_position_durations = [0] * len(individual_words)
    #this vector stores the number of fixations at each position
    fixation_position_counts = [0] * len(individual_words)
    #this vector stores the word lengths at each position
    fixation_position_lengths = [0] * len(individual_words)

    #this vector stores the fixation times for all fixations
    iteration_durations = []
    #this vector stores the word lengths for all fixations
    iteration_lengths = []

    crt_fixation_position = 0

    with open(input_file_all_data,"r") as f:
        with open(input_file_unrecognized_words,"r") as g:
            all_data = pickle.load(f)
            unrecognized_words = pickle.load(g)
            regressions = 0
            wordskips = 0
            refixations = 0
            fixation_durations = []

            regressions_words = []
            refixations_words = []
            wordskips_words = []

            #use this to check again for all positions
            recognized_positions = []

            number_of_nonneighboring_words_recognized = 0
            inp_bigr = []
            inp_bigr_inh = []
            inp_w_inh = []
            total_act = []
            fixation_act = []
            nonneighboring_words = []

            counter = 0

            for iteration_data in all_data:

                if iteration_data['refixated']==True:
                    refixations+=1
                    refixations_words.append( (iteration_data['foveal word'] , iteration_data['foveal word text index']))
                if iteration_data['wordskipped']==True:
                    wordskips+=1
                    wordskips_words.append( (individual_words[ iteration_data['foveal word text index']-1] ,iteration_data['foveal word text index']-1) )
                if iteration_data['regressed']==True:
                    regressions+=1
                    regressions_words.append( (iteration_data['foveal word'],iteration_data['foveal word text index']) )

                crt_neighboring_words_recognized = []

                nonneighboring_words_recognized = []
                position_counter = 0
                for position in iteration_data['recognized words positions']:
                    recognized_word = iteration_data['recognized words'][position_counter]

                    if position not in recognized_positions:
                        recognized_positions.append(position)
                    if position == -1:
                        number_of_nonneighboring_words_recognized+=1

                        nonneighboring_words_recognized.append(recognized_word)
                    else:
                        crt_neighboring_words_recognized.append(recognized_word)
                    position_counter += 1
                if(len(nonneighboring_words_recognized)>0):
                    nonneighboring_words.append((iteration_data['foveal word text index'],iteration_data['stimulus'],crt_neighboring_words_recognized,nonneighboring_words_recognized) )

                # create time series for word related activity
                if 'fixation word activities' in iteration_data.keys():
                    for iteration in iteration_data['fixation word activities']:
                        #total fixation word excitatory bigram input activity
                        inp_bigr.append(iteration[0])
                        #total fixation word inhibitory bigram input activity
                        inp_bigr_inh.append(iteration[1])
                        #total fixation word to word inhibition
                        inp_w_inh.append(iteration[2])
                        #activation of the fixation word
                        fixation_act.append(iteration[3])
                        #total activity
                        total_act.append(iteration[4])

                iteration_durations.append(iteration_data['fixation duration'])
                iteration_lengths.append(len(iteration_data['foveal word']))

                # for multiple fixations on same word
                if 'foveal word text index' in iteration_data.keys():
                    crt_fixation_position = iteration_data['foveal word text index']
                    fixation_position_durations[crt_fixation_position]+=iteration_data['fixation duration']
                    fixation_position_counts[crt_fixation_position]+=1
                    fixation_position_lengths[crt_fixation_position] = len(iteration_data['foveal word'])
                counter = counter+1

            # print 'Regressions:', regressions, regressions_words
            # print 'Refixations:', refixations, refixations_words
            # print 'Wordskips:', wordskips, wordskips_words
            # print 'Unrecognized: ', len(unrecognized_words),unrecognized_words
            # print 'Number of nonneighboring_words_recognized',number_of_nonneighboring_words_recognized
            neighboring_csv_string = ""
            for nonneighboring_word_data in nonneighboring_words:
                #print nonneighboring_word_data[0],":",nonneighboring_word_data[1],"->",nonneighboring_word_data[2],nonneighboring_word_data[3]
                neighboring_csv_string+=unicode(nonneighboring_word_data[0])+ ","+nonneighboring_word_data[1]+',"'+ ( ','.join(nonneighboring_word_data[2]) )+'","'+ ( ','.join(nonneighboring_word_data[3] ) ) +'"\n'

            textfile = open("neighboring.csv","w")
            textfile.write(neighboring_csv_string.encode('utf8'))
            textfile.close()

            plt.figure(1,figsize = (12,10))

            ax = plt.subplot(321)
            ax.set_title("Average fixation duration")
            density = stats.kde.gaussian_kde(iteration_durations)
            x = np.arange(min(iteration_durations)-100, max(iteration_durations)+100,1)
            x = np.arange(0,600)
            #plt.plot(x, density(x))
            plt.hist(iteration_durations,bins=15, range=(0,max(iteration_durations)+100))

            ax = plt.subplot(322)
            ax.set_title("Total fixation duration per word")
            density = stats.kde.gaussian_kde(fixation_position_durations)
            x = np.arange(0, max(fixation_position_durations)+100,1)
            plt.plot(x, density(x))
            #plt.hist(fixation_position_durations,bins=15)

            iteration_durations0 = all_indices(0,iteration_durations)
            #print('those with iteration dur 0',iteration_durations0)

            ax = plt.subplot(323)
            ax.set_title("Average fixation durations / word length")
            draw_boxplot(iteration_lengths,iteration_durations)

            #remove all positions which were wordksipped (and hence have fixation position duration 0) here
            fixation_position_durations0 = all_indices(0,fixation_position_durations)
            fixation_position_durations_no0 = multi_delete(fixation_position_durations,fixation_position_durations0)
            fixation_position_lengths_no0 = multi_delete(fixation_position_lengths,fixation_position_durations0)
            fixation_position_counts_no0 = multi_delete(fixation_position_counts,fixation_position_durations0)

            ax = plt.subplot(324)
            ax.set_title("Gaze durations / word lengths")
            draw_boxplot(fixation_position_lengths_no0,fixation_position_durations_no0)

            ax = plt.subplot(326)
            ax.set_title("Fixation counts per position")
            draw_boxplot(fixation_position_lengths_no0,fixation_position_counts_no0)

            plt.show()
            plt.savefig('plots/plot_RTandCounts.png')

            plt.figure(2,figsize = (7,4))
            plt.title('input')
            x = np.arange(1,len(inp_bigr)+1,1)

            sumarray = np.array(inp_bigr) + np.array(inp_w_inh)+np.array(inp_bigr_inh)
            plt.plot(x,np.array(inp_bigr),'b',x,np.array(inp_w_inh),'r',x,np.array(inp_bigr_inh),'g')
            plt.show()
            plt.savefig('plots/plot_activity.png')