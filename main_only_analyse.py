from analyse_data_pandas import get_results
from analyse_data_old import get_results as get_results2
from create_name import create_name
import glob
import os

filename = "PSC"
filepath = "Results/"

## Get most recent results
dated_files = [(os.path.getmtime(fn), os.path.basename(fn))
               for fn in glob.iglob('Results/*.dat')]
dated_files.sort()
dated_files.reverse()
psc_results = dated_files[1][1]
unrecognized_results = dated_files[0][1]
input_file_all_data = filepath + str(psc_results)
input_file_unrecognized_words = filepath + str(unrecognized_results)
print psc_results

get_results(filename,input_file_all_data,input_file_unrecognized_words)