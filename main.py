# CHANGED

from reading_simulation import reading_simulation
from reading_simulation_BT import reading_simulation_BT
from analyse_data_pandas import get_results
from create_name import create_name_josh
import pickle
import cProfile
import pstats

filename = "PSC_ALL"
filepath_psc = "PSC/" + filename + ".txt"

# profile_save = 'Profile_stats/myprofile_monogramactivations.stats'
# profile = cProfile.run('reading_simulation(filepath_psc)',profile_save)
# p = pstats.Stats(profile_save)
# p.sort_stats('cumtime').print_stats(50)

(lexicon,all_data, unrecognized_words) = reading_simulation(filepath_psc)

output_file_all_data, output_file_unrecognized_words = create_name_josh(filename)
with open(output_file_all_data,"w") as f:
    pickle.dump(all_data,f)
f.close()
with open(output_file_unrecognized_words,"w") as f:
    pickle.dump(unrecognized_words,f)


with open(r"C:\Users\Josh\Desktop\Josh work\Experiments\BOB\sam reading model july15\sam reading model july15\Results.dat") as f:
    actual_data = pickle.load(f)
f.close()

#with open("C:\Users\Josh\Desktop\josh work\Experiments\BOB\sam reading model july15\sam reading model july15\unrecognized.txt") as f:
#    for i in range(0,len(unrecognized_words)):
#        f.write(str(unrecognized_words[i]))
#f.close()
with open("C:\\Users\\Josh\\Desktop\\Josh work\\Experiments\\BOB\\sam reading model july15\\sam reading model july15\\Raw_BT_data\\new_normal_data.txt", "w") as g:
   for i in range(0,len(actual_data)):
       g.write(str(actual_data[i]))
g.close()

get_results(filename,output_file_all_data,output_file_unrecognized_words)


#with open("C:\\Users\\Josh\\Desktop\\josh work\\Experiments\\BOB\\sam reading model july15\\sam reading model july15\\Raw_BT_data\\boundary_data.txt", "w") as g:
#   g.write(df_GD_boundary_task_POF)
#g.close()
       