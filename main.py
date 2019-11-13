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

parameters = []
bounds = []

#parameters.append(pm.decay)
#bounds.append((-0.95,-0.01))

#parameters.append(pm.bigram_to_word_excitation)
#bounds.append((0, None))

#parameters.append(pm.bigram_to_word_inhibition)
#bounds.append((None, 0))

#parameters.append(pm.word_inhibition)
#bounds.append((None, 0))

#parameters.append(pm.max_activity)
#bounds.append((0, 5))

#parameters.append(pm.max_attend_width)
#bounds.append((3, 9))

#parameters.append(pm.min_attend_width)
#bounds.append((1,3))

#parameters.append(pm.attention_skew)
#bounds.append((1, 8))

#parameters.append(pm.bigram_gap)
#bounds.append((2, 10))

#parameters.append(pm.min_overlap)
#bounds.append((1, 10))

#parameters.append(pm.refix_size)
#bounds.append((0, 2))

#parameters.append(pm.salience_position)
#bounds.append((0, 5))

#parameters.append(pm.sacc_optimal_distance)
#bounds.append((3, 10))

#parameters.append(pm.saccErr_scaler)
#bounds.append((0, 3))

#parameters.append(pm.saccErr_sigma)
#bounds.append((0, 1))

#parameters.append(pm.saccErr_sigma_scaler)
#bounds.append((0, 1))

parameters.append(15)
bounds.append((2, 16))
#parameters.append(pm.mu)
#bounds.append((2, 10))

#parameters.append(0.1)
#bounds.append((0.5, 4))
#parameters.append(pm.sigma)
#bounds.append((0.5, 4))

#parameters.append(pm.distribution_param)
#bounds.append((0.5, 5))

#parameters.append(pm.wordfreq_p)
#bounds.append((1,15))

#parameters.append(pm.wordpred_p)
#bounds.append((1,15))

OLD_DISTANCE = np.inf

def reading_function(parameters):
	global OLD_DISTANCE
	filename = "PSC_ALL"
	filepath_psc = "PSC/" + filename + ".txt"
### For testing
#	with open("Results/all_data.pkl","r") as f:
#		all_data = pickle.load(f)
#	with open("Results/unrecognized.pkl","r") as f:
#		unrecognized_words = pickle.load(f)
###
	(lexicon,all_data, unrecognized_words) = reading_simulation(filepath_psc, parameters)
	first_distance = get_scores(filename,all_data,unrecognized_words)

	(lexicon,all_data, unrecognized_words) = reading_simulation(filepath_psc, parameters)
	second_distance = get_scores(filename,all_data,unrecognized_words)

	distance = (first_distance + second_distance) / 2

	if distance < OLD_DISTANCE:
		np.savetxt(str(distance)+"_parameters.txt",parameters)
		OLD_DISTANCE = distance

	with open("dist.txt","a") as f:
		f.write(str(first_distance)+", "+str(second_distance)+": "+str(distance)+"\n")
	return distance


run_exp = False
analyze_results = False
save_results = False
optimize = True

if pm.language == "german":
	filename = "PSC_ALL"
	filepath_psc = "PSC/" + filename + ".txt"
if pm.language == "dutch":
	filename = "PSC/words_dutch.pkl"
output_file_all_data, output_file_unrecognized_words = ("Results/all_data"+pm.language+".pkl","Results/unrecognized"+pm.language+".pkl")
start_time = time.time()

if run_exp:
	(lexicon,all_data, unrecognized_words) = reading_simulation(filepath_psc, parameters=False)
	if save_results:
		all_data_file = open(output_file_all_data,"w")
		pickle.dump(all_data, all_data_file)
		all_data_file.close()

		unrecognized_file = open(output_file_unrecognized_words, "w")
		pickle.dump(unrecognized_words, unrecognized_file)
		unrecognized_file.close()

if analyze_results:
	get_results(filename,output_file_all_data,output_file_unrecognized_words)
if optimize:
	epsilon = pm.epsilon
	results = scipy.optimize.fmin_l_bfgs_b(func=reading_function, x0=np.array(parameters), bounds=bounds, approx_grad=True , disp=True, epsilon=epsilon)
	with open("results_optimization.pkl","wb") as f:
		pickle.dump(results, f)

time_elapsed = time.time()-start_time
print("Time elapsed: "+str(time_elapsed))
