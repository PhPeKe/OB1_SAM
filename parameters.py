# CHANGED
# -*- coding: UTF-8 -*-
import time

__author__ = 'Sam van Leipsig, Phillip Kersten'
print("Parameters Initialised")

# Control-flow parameters
run_exp = False  # Should the reading simulation run?
analyze_results = False  # Should the results be analyzed?
optimize = True  # Should the parameters be optimized?

language = "german"  # german, dutch
use_grammar_prob = False # True for using grammar probabilities, False for using cloze, overwritten by uniform_pred
uniform_pred = False  # Overwrites cloze/grammar probabilities with 0.25 for all words

include_sacc_type_sse = True  # Include the sse score based on the saccade type probability plot
sacc_type_objective = "total"  # If "total" all subplots will be included in the final sse,
                               #  single objectives can be "length", "freq" or "pred"

include_sacc_dist_sse = True  # Include the SSE score derived from the saccade_distance.png plot

tuning_measure = "SSE"  # can be "KL" or "SSE"
discretization = "bin"  # can be "bin" or "kde"
objective = []  # empty list for total SSE/KL, for single objectives: "total viewing time",
                # "Gaze durations", "Single fixations", "First fixation duration",
                # "Second fixation duration", "Regression"

output_dir = time.time()
epsilon = 0.1  # Step-size for approximation of the gradient


print("_----PARAMETERS----_")
print("reading in " + language)
if use_grammar_prob:
    print("Using syntax probabilities")
else:
    print("Using cloze probabilities")
if optimize:
    print("Using: "+tuning_measure)
    if any(objective):
        print("Single Objective: "+tuning_measure+" of "+objective)
    else:
        print("Using total "+tuning_measure)
#    print("Step-size: "+str(epsilon))
print("-------------------")


## Monoweight = 1
decay = -0.053
bigram_to_word_excitation = 0.0044
bigram_to_word_inhibition = -0.0001
word_inhibition = -0.002

letPerDeg = .3
min_activity = 0.0
max_activity = 1.3

## Attentional width
max_attend_width = 5.0
min_attend_width = 3.0
attention_skew = 7.9 # 4  #2.39 (optimal) # 1 equals symmetrical distribution # 4 (paper)
bigram_gap = 3 # 6 (optimal) # 3 (paper)
min_overlap = 2
refix_size = 0.2
salience_position = 4.99 # 1.29 # 5 (optimal) # 1.29 (paper)
corpora_repeats = 0


## Model settings
frequency_flag = True
prediction_flag = True
similarity_based_recognition = True
use_saccade_error = True
use_attendposition_change = True
visualise = False
slow_word_activity = False
print_all = False
pauze_allocation_errors = False
use_boundary_task = False

## Saccade error
sacc_optimal_distance = 9.99  # 3.1 # 7.0 # 8.0 (optimal) # 7.0 (paper)
saccErr_scaler = 0.2  # to determine avg error for distance difference
saccErr_sigma = 0.17 # basic sigma
saccErr_sigma_scaler = 0.06 # effect of distance on sigma

## Fixation duration# s
mu, sigma = 10.09 , 5.36 # 4.9, 2.2 # 5.46258 (optimal), 4 # 4.9, 2.2 (paper)
distribution_param = 5.0  #1.1

## Threshold parameters
linear = False
wordfreq_p = 1 # 5.5 # 9 (optimal) # 5.5 (paper)
wordpred_p = 1 # 9.0

#linear
start_lin = 0.057
wordlen_lin = 0.006

## Monoweight = 1
start_nonlin = 0.134
nonlin_scaler = 0.22
wordlen_nonlin = -0.44

#Nonlinear
## Monoweight = 2
# start_nonlin = 0.143
# nonlin_scaler = 0.21
# wordlen_nonlin = -0.8
# CHANGED
# -*- coding: UTF-8 -*-
import time

__author__ = 'Sam van Leipsig, Phillip Kersten'
print("Parameters Initialised")

# Control-flow parameters
run_exp = False  # Should the reading simulation run?
analyze_results = False  # Should the results be analyzed?
optimize = True  # Should the parameters be optimized?

language = "german"  # german, dutch
use_grammar_prob = False # True for using grammar probabilities, False for using cloze, overwritten by uniform_pred
uniform_pred = False  # Overwrites cloze/grammar probabilities with 0.25 for all words

include_sacc_type_sse = True  # Include the sse score based on the saccade type probability plot
sacc_type_objective = "total"  # If "total" all subplots will be included in the final sse,
                               #  single objectives can be "length", "freq" or "pred"

include_sacc_dist_sse = True  # Include the SSE score derived from the saccade_distance.png plot

tuning_measure = "SSE"  # can be "KL" or "SSE"
discretization = "bin"  # can be "bin" or "kde"
objective = []  # empty list for total SSE/KL, for single objectives: "total viewing time",
                # "Gaze durations", "Single fixations", "First fixation duration",
                # "Second fixation duration", "Regression"

output_dir = time.time()
epsilon = 0.1  # Step-size for approximation of the gradient


print("_----PARAMETERS----_")
print("reading in " + language)
if use_grammar_prob:
    print("Using syntax probabilities")
else:
    print("Using cloze probabilities")
if optimize:
    print("Using: "+tuning_measure)
    if any(objective):
        print("Single Objective: "+tuning_measure+" of "+objective)
    else:
        print("Using total "+tuning_measure)
#    print("Step-size: "+str(epsilon))
print("-------------------")


## Monoweight = 1
decay = -0.053
bigram_to_word_excitation = 0.0044
bigram_to_word_inhibition = -0.0001
word_inhibition = -0.002

letPerDeg = .3
min_activity = 0.0
max_activity = 1.3

## Attentional width
max_attend_width = 5.0
min_attend_width = 3.0
attention_skew = 4 # 4  #2.39 (optimal) # 1 equals symmetrical distribution # 4 (paper)
bigram_gap = 3 # 6 (optimal) # 3 (paper)
min_overlap = 2
refix_size = 0.2
salience_position = 1.29 # 1.29 # 5 (optimal) # 1.29 (paper)
corpora_repeats = 0


## Model settings
frequency_flag = True
prediction_flag = True
similarity_based_recognition = True
use_saccade_error = True
use_attendposition_change = True
visualise = False
slow_word_activity = False
print_all = False
pauze_allocation_errors = False
use_boundary_task = False

## Saccade error
sacc_optimal_distance = 7.0  # 3.1 # 7.0 # 8.0 (optimal) # 7.0 (paper)
saccErr_scaler = 0.2  # to determine avg error for distance difference
saccErr_sigma = 0.17 # basic sigma
saccErr_sigma_scaler = 0.06 # effect of distance on sigma

## Fixation duration# s
mu, sigma = 4.9, 2.2 # 10.09 , 5.36 # 4.9, 2.2 # 5.46258 (optimal), 4 # 4.9, 2.2 (paper)
distribution_param = 5.0  #1.1

## Threshold parameters
linear = False
wordfreq_p = 5.5 # 1 # 9 (optimal) # 5.5 (paper)
wordpred_p = 9.0 # 1.0

#linear
start_lin = 0.057
wordlen_lin = 0.006

## Monoweight = 1
start_nonlin = 0.134
nonlin_scaler = 0.22
wordlen_nonlin = -0.44

#Nonlinear
## Monoweight = 2
# start_nonlin = 0.143
# nonlin_scaler = 0.21
# wordlen_nonlin = -0.8
