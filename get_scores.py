__author__ = 'Phillip Kersten, adapted from Sam van Leipsig'

import matplotlib
from time import time
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import pickle
import pandas as pd
import analyse_data_plot_qualitative as mod2
from reading_common import get_stimulus_text_from_file
import read_saccade_data as exp
import analyse_data_transformation as trans
import parameters as pm



def get_scores(input_text_filename,all_data,unrecognized_words):
#    with open(input_file_all_data,"r") as f:
#        all_data = pickle.load(f)
#    with open(input_file_unrecognized_words,"r") as g:
#        unrecognized_words = pickle.load(g)
    ## Parameters
    freqbins  = np.arange(-0.0,8,2.0)
    predbins = np.arange(-0.0,1.01,0.333)
    distancebins = np.arange(-0.0,20,2.0)
    neighborbins = np.arange(0,10,3)


    ## Get complete psc (add freq and pred)
    textfile = get_stimulus_text_from_file("PSC/" + input_text_filename + '.txt')
    individual_words = []
    textsplitbyspace = textfile.split(" ")
    for word in textsplitbyspace:
        if word.strip()!="":
            individual_words.append(word.strip())
    df_individual_words = pd.DataFrame(individual_words)

    df_freq_pred = exp.get_freq_and_pred()


    df_freq_pred = df_freq_pred.iloc[0:len(df_individual_words),:]
    df_individual_words = pd.concat([df_individual_words,df_freq_pred],axis=1,join_axes=[df_individual_words.index])
    df_individual_words = df_individual_words.drop(['word'],1)
    df_individual_words.rename(columns={'0':'foveal word','f':'freq'}, inplace=True)
    df_individual_words_base = df_individual_words.copy()
    for i in range(0,pm.corpora_repeats):
        df_individual_words = pd.concat([df_individual_words,df_individual_words_base],axis=0, ignore_index=True)

    ## Init dataframe
    df_alldata = pd.DataFrame(all_data)
    df_alldata['word length'] = df_alldata['foveal word'].map(len)
    df_alldata = trans.correct_wordskips(df_alldata)
    df_alldata = trans.correct_offset(df_alldata)
    df_alldata_no_regr = df_alldata[(df_alldata['regressed']==False)]  ## There are no refixations after a regression!

    ## Word measures by cycle, grouped by word length
    # not necessary??  # word_measures_bylen_dict = trans.make_word_measures_bylength(df_alldata)
    df_alldata = df_alldata.drop(['fixation word activities np'],1)
    df_alldata_no_regr['foveal word text index2'] = df_alldata_no_regr['foveal word text index']
    df_SF = df_alldata_no_regr.groupby(['foveal word text index']).filter(lambda x: len(x)==1)

    ## Select first fixation and single fixations, use sequential to select first pass only
    df_fixations_sequential = df_alldata_no_regr.groupby(['foveal word text index']).filter(lambda x: trans.sequential(x))
    singlefirst_fixation_grouped =  df_fixations_sequential.groupby(['foveal word text index'])
    singlefirst_fixation_selection =  singlefirst_fixation_grouped.apply(lambda x: x.index[0]).values
    df_single_first_fixation = df_alldata_no_regr.loc[singlefirst_fixation_selection,:]


    ## Create complete dataset including wordskips
    df_individual_words.reset_index ## index is now the same as foveal word text index
    df_alldata_to_group = df_alldata.drop(['word length','foveal word','recognized words indices','fixation word activities', 'word activities per cycle', 'stimulus'],1)
    df_alldata_grouped_max = df_alldata_to_group.groupby('foveal word text index', as_index= True).max()
    df_alldata_grouped_all = pd.concat([df_individual_words,df_alldata_grouped_max], axis=1, join_axes=[df_individual_words.index])
    df_alldata_grouped_all['wordskipped'].fillna(True, inplace=True)
    replaceNA = {'regressed': False, 'refixated': False,'forward':False,'after wordskip':False,'before wordskip':False}
    df_alldata_grouped_all.fillna(replaceNA,inplace=True)
    df_alldata_grouped_all.rename(columns={0:'foveal word'}, inplace=True)
    df_alldata_grouped_all['word length'] = df_alldata_grouped_all['foveal word'].map(len)

    # print df_alldata.columns.values

    ## General fixation duration measures
    total_viewing_time = df_alldata.groupby(['foveal word text index'])[['fixation duration']].sum()
    gaze_durations = df_alldata_no_regr[['fixation duration','foveal word text index']].groupby(['foveal word text index']).sum()
    df_FD_only_regr = df_alldata[(df_alldata['regressed']==True)]['fixation duration']
    df_single_fixation, first_fixation, second_fixation = trans.make_number_fixations(df_alldata_no_regr)

    df_single_fixation = df_single_fixation.set_index('foveal word text index')

    ## General fixation duration measures
    total_viewing_time = df_alldata.groupby(['foveal word text index'])[['fixation duration']].sum()
    gaze_durations = df_alldata_no_regr[['fixation duration', 'foveal word text index']].groupby(
        ['foveal word text index']).sum()
    df_FD_only_regr = df_alldata[(df_alldata['regressed'] == True)]['fixation duration']
    df_single_fixations, first_fixation, second_fixation = trans.make_number_fixations(df_alldata_no_regr)
    ## Fixation durations histograms
    exp_FD_dict = exp.get_saccade_durations()

    ## Get distance between curves in plot
    total_distance = 0
    distances = {}
    simulation = [total_viewing_time["fixation duration"],
                  gaze_durations['fixation duration'],
                  df_single_fixations['fixation duration'],
                  first_fixation,
                  second_fixation,
                  df_FD_only_regr
                  ]
    experiment = [exp_FD_dict["TVT"],
                  exp_FD_dict['GZD'],
                  exp_FD_dict['SFD'],
                  exp_FD_dict['FFD'],
                  exp_FD_dict['SecondFD'],
                  exp_FD_dict['RD']
                  ]
    names = ["total viewing time",
             "Gaze duration",
             "Single fixations",
             "First fixation duration",
             "Second fixation duration",
             "Regression"
             ]
    plt.close()
    fig, ax = plt.subplots(2, 3, sharex='col', sharey='row')
    ax = ax.ravel()
    legends = []
    i = 0
    for sim_, exp_, name in zip(simulation,experiment, names):

        min_ = min([exp_.min(), sim_.min()])
        max_ = max([exp_.max(), sim_.max()])

        X = np.mgrid[min_:max_:500j]
        positions = X.ravel()
        values_x = sim_
        values_y = exp_
	print("-----------------Kernel x------------------")
	print(values_x)
	print("-----------------Kernel y------------------")
	print(values_y)
        kernel_x = stats.gaussian_kde(values_x)
        kernel_y = stats.gaussian_kde(values_y)
        # Set bandwidth like in the original plotting method
        band_width = 0.31
        kernel_x.set_bandwidth(band_width)
        kernel_y.set_bandwidth(band_width)
        Z_x = np.reshape(kernel_x(positions).T, X.shape)
        Z_y = np.reshape(kernel_y(positions).T, X.shape)
        total_distance += sum(map(lambda x: abs(x[0]-x[1]), zip(Z_x,Z_y)))
        distances[name] = sum(map(lambda x: abs(x[0]-x[1]), zip(Z_x,Z_y)))
        plot = True
	t = time()
        if plot:
            #plt.subplot(2, 3, i)
            ax[i].set_ylim(0,0.01)
            line_x = ax[i].plot(Z_x)
            line_y = ax[i].plot(Z_y)
            ax[i].set_title(name+": \n"+str(round(distances[name],3)))
            # ax[x,y].suptitle("KDE for: "+name)
            i += 1
    plt.figlegend(handles=[line_x, line_y], labels=["Simulation", "Experiment"], loc='upper-right')  # ["Simulation", "Experiment"])
    fig.suptitle("Total distance: "+str(total_distance))
    plt.savefig("test_density"+str(int(t))+".png", dpi=300)
    return total_distance
