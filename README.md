# OB1_SAM
OB1 is a reading-model that simulates the processes behind reading in the brain. 

For more information about the theoretical aspects of OB1 and a validation of its reading capabilities see: https://www.ncbi.nlm.nih.gov/pubmed/30080066

##Modes
OB1 can be used for different purposes. 
###Experiment
In the standard version it reads a german text and uses word frequency as well as
word predictability (cloze probability) to recognize words presented in its visual field.

Plots are produced and saved in "/plots"

###Parameter-tuning
In this version the model is executed multiple times in order to find the set of parameters that enables the model to 
read in a way that is similar to how a human would read the text. The optimization is done by using the *L-BFGS-B* 
optimization method from *scipy*.


##How to use OB1

**Running an experiment**:

In order to run a "normal" experiment one should set "run_exp" and "analyze_results" to True.

**Parameter-tuning**

For parameter-tuning set the parameters you wish to change in "get_parameters.py" and then 

OB1 is a reading-model that simulates the processes behind reading in the brain. For more information about the theoretical aspects of OB1 and a validation of its reading capabilities see: https://www.ncbi.nlm.nih.gov/pubmed/30080066

