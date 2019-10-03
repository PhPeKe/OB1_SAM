# CHANGED
from reading_simulation import reading_simulation
from reading_simulation_BT import reading_simulation_BT
from analyse_data_pandas import get_results
from create_name import create_name_josh
import pickle
import cProfile
import pstats
import time
from get_scores import get_scores

run_exp = True # Should be "run" or "test"
analyze_results = False
save_results = True
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
	distance = get_scores(filename,output_file_all_data,output_file_unrecognized_words)
time_elapsed = time.time()-start_time
print("Time elapsed: "+str(time_elapsed))
print("Total distance: "+str(distance))
