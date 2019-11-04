# CHANGED
from reading_simulation_cycle import reading_simulation
from reading_simulation_BT import reading_simulation_BT
from analyse_data_pandas import get_results
from create_name import create_name_josh
import pickle
import cProfile
import pstats
import scipy
import time
import numpy as np
from get_scores import get_scores
import parameters as pm

CYCLE_SIZE = 25
parameters = [CYCLE_SIZE]
bounds = [(1,50)]

OLD_DISTANCE = 999

def reading_function(parameters):
	global OLD_DISTANCE
	filename = "PSC_ALL"
	filepath_psc = "PSC/" + filename + ".txt"
	(lexicon,all_data, unrecognized_words) = reading_simulation(filepath_psc, parameters)
### For testing
#	with open("Results/all_data.pkl","r") as f:
#		all_data = pickle.load(f)
#	with open("Results/unrecognized.pkl","r") as f:
#		unrecognized_words = pickle.load(f)
###
	distance = get_scores(filename,all_data,unrecognized_words)
	if distance < OLD_DISTANCE:
		np.savetxt(str(distance)+"_parameters.txt",parameters)
		OLD_DISTANCE = distance

	with open("dist.txt","a") as f:
		f.write("Distance:"+str(distance)+"\n")
	return distance

run_exp = False
analyze_results = False
save_results = False
optimize = True

filename = "PSC_ALL"
filepath_psc = "PSC/" + filename + ".txt"
output_file_all_data, output_file_unrecognized_words = ("Results/all_data.pkl","Results/unrecognized.pkl")
start_time = time.time()

if run_exp:
	(lexicon,all_data, unrecognized_words) = reading_simulation(filepath_psc)
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
	results = scipy.optimize.fmin_l_bfgs_b(func=reading_function, x0=np.array(parameters), bounds=bounds, approx_grad=True , disp=True)
time_elapsed = time.time()-start_time
with open("results_optimization.pkl","wb") as file:
	pickle.dump(results, file)
print("Time elapsed: "+str(time_elapsed))
print("Total distance: "+str(distance))
