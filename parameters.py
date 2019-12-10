# CHANGED
# -*- coding: UTF-8 -*-
import time

__author__ = 'Sam van Leipsig'
print("Parameters Initialised")

# Control-flow parameters
run_exp = True  # Should the reading simulation run?
analyze_results = True  # Should the results be analyzed?
optimize = False  # Should the parameters be optimized?

language = "german"  # german, dutch
use_grammar_prob = True  # True for using grammar probabilities, False for using cloze
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
    print("Step-size: "+str(epsilon))
print("-------------------")

## Monoweight = 1
decay = -0.05
bigram_to_word_excitation = 0.0044
bigram_to_word_inhibition = -0.0
word_inhibition = -0.0018

letPerDeg = .3
min_activity = 0.0
max_activity = 1.3

## Attentional width
max_attend_width = 5.0
min_attend_width = 3.0
attention_skew = 2.39  #4 # 1 equals symmetrical distribution
bigram_gap = 6
min_overlap = 2
refix_size = 0.2
salience_position = 5  #1.29
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
sacc_optimal_distance = 8.0
saccErr_scaler = 0.2  # to determine avg error for distance difference
saccErr_sigma = 0.17 # basic sigma
saccErr_sigma_scaler = 0.06 # effect of distance on sigma

## Fixation duration# s
mu, sigma = 5.46258, 4  # 4.9, 2.2
distribution_param = 1.1

## Threshold parameters
linear = False
wordfreq_p = 15  # 9
wordpred_p = 5.5

#linear
start_lin = 0.057
wordlen_lin = 0.006

## Monoweight = 1
start_nonlin = 0.134
nonlin_scaler = 0.22
wordlen_nonlin = -0.4

#Nonlinear
## Monoweight = 2
# start_nonlin = 0.143
# nonlin_scaler = 0.21
# wordlen_nonlin = -0.8

## Word activation
## Monoweight = 2
# decay = -0.047
# bigram_to_word_excitation = 0.004
# bigram_to_word_inhibition = -0.0001
# word_inhibition = -0.0014