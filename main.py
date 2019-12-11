# -*- coding: utf-8 -*-
# CHANGED
from reading_simulation import reading_simulation
from reading_simulation_BT import reading_simulation_BT
from analyse_data_pandas import get_results
from create_name import create_name_josh
import multiprocessing as mp
import pickle
import cProfile
import pstats
import scipy
import time
import numpy as np
from get_scores import get_scores
import parameters as pm
import pandas as pd

parameters = []
bounds = []
names = []

#parameters.append(pm.decay)
#bounds.append((-0.95,-0.01))
#names.append("decay")

#parameters.append(pm.bigram_to_word_excitation)
#bounds.append((0, None))
#names.append("bigram_to_word_excitation")

#parameters.append(pm.bigram_to_word_inhibition)
#bounds.append((None, 0))
#names.append("bigram_to_word_inhibition")

#parameters.append(pm.word_inhibition)
#bounds.append((None, 0))
#names.append("word_inhibition")

#parameters.append(pm.max_activity)
#bounds.append((0, 5))
#names.append("max_activity")

#parameters.append(pm.max_attend_width)
#bounds.append((3, 9))
#names.append("max_attend_width")

#parameters.append(pm.min_attend_width)
#bounds.append((1,3))
#names.append("min_attend_width")

#parameters.append(pm.attention_skew)
#bounds.append((1, 8))
#names.append("attention_skew")

#parameters.append(pm.bigram_gap)
#bounds.append((2, 10))
#names.append("bigram_gap")

#parameters.append(pm.min_overlap)
#bounds.append((1, 10))
#names.append("min_overlap")

#parameters.append(pm.refix_size)
#bounds.append((0, 2))
#names.append("refix_size")

#parameters.append(pm.salience_position)
#bounds.append((0, 5))
#names.append("salience_position")

#parameters.append(pm.sacc_optimal_distance)
#bounds.append((3, 10))
#names.append("sacc_optimal_distance")

#parameters.append(pm.saccErr_scaler)
#bounds.append((0, 3))
#names.append("sacc_err_scaler")

parameters.append(pm.saccErr_sigma)
bounds.append((0, 1))
names.append("sacc_err_sigma")

parameters.append(pm.saccErr_sigma_scaler)
bounds.append((0, 1))
names.append("sacc_err_sigma_scaler")

#parameters.append(pm.mu)
#bounds.append((2, 16))
names.append("mu")
parameters.append(pm.mu)
bounds.append((2, 10))

parameters.append(pm.sigma)
bounds.append((0.5, 4))
names.append("sigma")
#parameters.append(pm.sigma)
#bounds.append((0.5, 4))

#parameters.append(pm.distribution_param)
#bounds.append((0.5, 5))
#names.append("distribution_param")

#parameters.append(pm.wordfreq_p)
#bounds.append((1,15))
#names.append("wordfreq_p")

#parameters.append(pm.wordpred_p)
#bounds.append((1,15))
#names.append("wordpred_p")

OLD_DISTANCE = np.inf
N_RUNS = 0

def reading_function(parameters):
	global OLD_DISTANCE
	global N_RUNS
	filename = "PSC_ALL"
	filepath_psc = "PSC/" + filename + ".txt"
### For testing (loading past results instead of running simulation)
#	with open("Results/all_data.pkl","r") as f:
#		all_data = pickle.load(f)
#	with open("Results/unrecognized.pkl","r") as f:
#		unrecognized_words = pickle.load(f)
###
	(lexicon,all_data, unrecognized_words) = reading_simulation(filepath_psc, parameters)
	distance = get_scores(filename,all_data,unrecognized_words)

	write_out = pd.DataFrame(np.array([names,parameters]).T)

	if distance < OLD_DISTANCE:
		write_out.to_csv(str(distance)+"_"+pm.tuning_measure+"parameters.txt", index=False, header=["name","value"])
		OLD_DISTANCE = distance

	with open("dist.txt","a") as f:
		f.write("run "+str(N_RUNS)+": "+str(distance)+"\n")
	N_RUNS += 1
	return distance

run_exp = True
analyze_results = True
save_results = True
optimize = False

if pm.language == "german":
	filename = "PSC_ALL"
	filepath_psc = "PSC/" + filename + ".txt"
if pm.language == "dutch":
	filename = "PSC/words_dutch.pkl"
output_file_all_data, output_file_unrecognized_words = ("Results/all_data"+pm.language+".pkl","Results/unrecognized"+pm.language+".pkl")
start_time = time.time()

if run_exp:
	(lexicon,all_data, unrecognized_words) = reading_simulation(filepath_psc, parameters=[])
	if save_results:
		all_data_file = open(output_file_all_data,"w")
		pickle.dump(all_data, all_data_file)
		all_data_file.close()

		unrecognized_file = open(output_file_unrecognized_words, "w")
		pickle.dump(unrecognized_words, unrecognized_file)
		unrecognized_file.close()

if analyze_results:
	get_results(filepath_psc,output_file_all_data,output_file_unrecognized_words)
if optimize:
	epsilon = pm.epsilon
	results = scipy.optimize.fmin_l_bfgs_b(func=reading_function, x0=np.array(parameters), bounds=bounds, approx_grad=True , disp=True, epsilon=epsilon)
	with open("results_optimization.pkl","wb") as f:
		pickle.dump(results, f)


time_elapsed = time.time()-start_time
print("Time elapsed: "+str(time_elapsed))
