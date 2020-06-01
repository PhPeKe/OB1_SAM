# OB1 reader
OB1 is a reading-model that simulates the processes behind reading in the brain. 

For more information about the theoretical aspects of OB1 and a validation of it's reading capabilities 
see: 

https://www.ncbi.nlm.nih.gov/pubmed/30080066

### parameters.py
This is the most important function for controlling the behavior of *main.py*. Here the user can specify which parts of the programm should be run and also set the initial parameters when tuning. Furthermore the user can define which measures are used as error-function for the tuning process. 

N.B. To change the language, you need a text file and a lexicon file. Simulations currently run on the German Potsdam corpus. For Dutch a lexicon with most frequent words is provided, but there is no coprus with correctly formatted eye-tracking data available yet to compare the performance of the reading simulation to.

### main.py
In this file the main programm flow is defined. It has calls to the reading function, which simulates the actual reading, as imported from *reading_simulation.py*, the analyze function as imported from *analyse_data_pandas.py* and the optimize function, which is **scipy's** *L-BFGS-B* optimizing method. The function called by this optimizing method is a wrapper that takes the parameters called in *parameters.py* and feeds them to the reading simulation. The optimize function makes use of a slightly adapted version of the analyzing function that can be found in *get_scores.py*.

### reading_simulation.py
This file embodies the heart of the whole programm, the reading simulation. Here the input text is fed into the visuo-spatial representation which is activating bigramm-matrices, which in turn are activating words that are recognized. The resulting (correctly or incorrectly) recognized words are saved in **all_data**, together with a set of descriptive variables. At the end of the simulation this data-representation of the reading process is saved as a pickle file ( *all_data_INPUT_LANGUAGE.pkl* ) for analysis in a later stage together with all **unrecognized_words** ( *unrecognized_INPUT_LANGUAGE.pkl* ).

### reading_common.py
Helper-functions for the reading simulation in *reading_simulation.py* 

### read_saccade_data.py
This file provides functions to read in the eye-tracking data collected during the experiment where participants had to read the same text that is presented to the OB1-reader.

### analyse_data_plot.py / analyse_data_plot_qualitative.py
In this files the result of a single experiment is analyzed and plots as seen in the publication are produced.

### analyse_data_transformation / analyse_data_pandas.py
These files are providing various functions to analyze the data used in *analyse_data_pandas.py*

## Modes
OB1 can be used for different purposes. 
### Experiment
In the standard version it reads a german text and uses word frequency as well as
word predictability (cloze probability) to recognize words presented in its visual field.

Plots are produced and saved in "/plots"

### Parameter-tuning
In this version the model is executed multiple times in order to find the set of parameters that enables the model to 
read in a way that is similar to how a human would read the text. The optimization is done by using the *L-BFGS-B* 
optimization method from *scipy*.

## How to use OB1

**Running an experiment**:

In order to run a "normal" (Which means reading the input text-file once and comparing the results to an eye-tracking 
experiment) experiment one should set "run_exp" and "analyze_results" in *parameters.py* to True and "optimize" to False.

**Parameter-tuning**

For parameter-tuning define the parameters you wish to change and their bounds in *get_parameters.py*. Then go to 
*reading_simulation.py* where you have to unpack these values again based on the order in which they have been packed.
 
Next go to *parameters.py* and change "optimize" to True. Don't forget to set "run_exp" as well as "analyze_results" to
  False if you want to **just optimize**.
  
The parameters are saved if they are better than the parameters from the previous iteration. They are saved
as a text file named after the tuning measure and the distance between experiment and simulation. 

**adding a new language**

To add a new language there has to be the plain text as input data for the reading simulation (see *PSC_ALL.txt* as an example for the format), a lexicon (see word_freq.pkl as an example) as well as the preprocessed eyetracking-data recorded during an experiment where participants had to read the text that is presented to OB1. For an example of the input data derived from an eye-tracking experiment see the table stored in *Fixation_durations_german.pkl*.

