#!/usr/bin/python
# -*- coding: utf-8 -*-
# CHANGED

import os
import sys
sys.path.append(".")
sys.path.append(os.getcwd()) 

os.listdir(".")

import reading_simulation
from reading_simulation import reading_simulation
from analyse_data_pandas import get_results
from create_name import create_name_josh
import multiprocessing as mp
import pickle
import cProfile
import pstats
from analyse_data_pandas import get_results
import pickle
import scipy
import time
import numpy as np
from get_scores import get_scores
import parameters as pm
import pandas as pd
from get_parameters import get_params
from joblib import Parallel, delayed

import random
from deap import creator, base, tools
from scoop import futures

# Init distance variables for the reading function used in tuning
OLD_DISTANCE = np.inf
N_RUNS = 0


def main():
	# Get parameters for tuning
	parameters, bounds, names = get_params(pm)

	# Reading function for tuning (called by scipy's L-BFGS-B optimizing function)
	def reading_function(parameters_rf):
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
	        # Run the simulation
	        (lexicon, all_data, unrecognized_words) = reading_simulation(filepath_psc, parameters_rf)
	        # Evaluate run and retrieve error-metric
	        distance = get_scores(filename, all_data, unrecognized_words)

	        # Save parameters when distance is better than previous
	        write_out = pd.DataFrame(np.array([names, parameters_rf]).T)
#	        if distance < OLD_DISTANCE:
#	                write_out.to_csv(str(distance)+"_"+pm.tuning_measure+"parameters.txt", index=False, header=["name", "value"])
#	                OLD_DISTANCE = distance

#		p = ""

#		for param, name in zip(parameters_rf, names):
#			p += name +": "
#			p += str(param)
#			p += "\n"
#
#	        # Save distances for plotting convergence
#	        with open("dist.txt", "a") as f:
#	                f.write("run "+str(N_RUNS)+": "+str(int(distance))+"\n")
#			f.write(p)
#			f.write("\n")
	        N_RUNS += 1
#	        return distance

	if pm.language == "german":
		filename = "PSC_ALL"
		filepath_psc = "PSC/" + filename + ".txt"
	# The reading model reads dutch but there is no data to compare it to yet
	if pm.language == "dutch":
		raise NotImplementedError
		filename = "PSC/words_dutch.pkl"

	output_file_all_data, output_file_unrecognized_words = ("Results/all_data"+pm.language+".pkl","Results/unrecognized"+pm.language+".pkl")
	start_time = time.time()

	if pm.run_exp:
		# Run the reading model
		(lexicon, all_data, unrecognized_words) = reading_simulation(filepath_psc, parameters=[])
		# Save results: all_data...
		all_data_file = open(output_file_all_data,"w")
		pickle.dump(all_data, all_data_file)
		all_data_file.close()
		# ...and unrecognized words
		unrecognized_file = open(output_file_unrecognized_words, "w")
		pickle.dump(unrecognized_words, unrecognized_file)
		unrecognized_file.close()

	if pm.analyze_results:
		get_results(filepath_psc,output_file_all_data,output_file_unrecognized_words)

	if pm.optimize:
		# EA parameters
		pop_size = 32
		multi_processing = True
		gens = 10
		tournament_size = 5
		cx_prob = 0.6
		# Mutation = +-10%
		mut_size = 0.1
		mut_prob = 0.2

		# Create fitness
		creator.create("FitnessMin", base.Fitness, weights=(-1.0,))

		# Create Individual
		creator.create("Individual", list, fitness=creator.FitnessMin)

		# Register attributes with bounds
		# TODO: discrete initialization 50% low 100% high
		def get_param(param):
			init = random.randint(0,2)
			if init == 0:
				return param - (param/2.0)
			if init == 1:
				return param
			if init == 2:
				return param * 2.0

		def mutate(gen, p):
			mutated_gen = []
			for allele in gen:
				# Mutation takes place
				if random.uniform(0,1) > p:
					print("Mutation of gene"+str(allele))
					# Either + or - 10% of the original value
					mutated_gen.append(allele + (allele * mut_size) if random.randint(0,1) else allele - (allele * mut_size))
				# No mutation takes place
				else:
					# Append original value
					mutated_gen.append(allele)
			# Sanity check that mutation went right
			assert(len(mutated_gen) == len(gen))
			return mutated_gen


		toolbox = base.Toolbox()
		toolbox.register("attention_skew", get_param, 4.0)
		toolbox.register("salience_position", get_param, 1.29)
		toolbox.register("sacc_optimal_distance", get_param, 7.0)
		toolbox.register("mu", get_param, 4.9)
		toolbox.register("sigma", get_param, 2.2)
		toolbox.register("distribution_param", get_param, 1.1)

		# Register Individual
		toolbox.register("Individual", tools.initCycle, creator.Individual,
				(toolbox.attention_skew,
				 toolbox.salience_position,
				 toolbox.sacc_optimal_distance,
				 toolbox.mu,
				 toolbox.sigma,
				 toolbox.distribution_param),
				n=1)

		# Register population
		toolbox.register("population", tools.initRepeat, list, toolbox.Individual)

		# Enable parallel processing
#		if multi_processing:
#			toolbox.register("map", futures.map)

		# Define operators
		toolbox.register("mate", tools.cxOnePoint)
		toolbox.register("mutate", mutate, p=0.1)
		toolbox.register("select", tools.selTournament, tournsize=tournament_size)
		toolbox.register("evaluate", reading_function)

		# Initialize first population
		population = toolbox.population(n=pop_size)

		# Evaluate first population
		print("Start evaluation gen 0")
		fits = Parallel(n_jobs=14, prefer="threads")(delayed(toolbox.evaluate)(ind) for ind in population)
		print("Finished evaluation")
		#toolbox.map(toolbox.evaluate, population)
		save=""
		for ind, fit in zip(population, fits):
			ind.fitness.values = fit
			save += "0 " + fit + "\n"
		with open("result_EA.txt","a") as f:
			f.write(save)
		np.savetxt("gen_0.txt", population)

		# Main evolution loop
		for gen in range(gens):
			# Select fittest individuals
			offspring = map(toolbox.clone, toolbox.select(population, pop_size-1))
			elite = tools.selBest(population, n=1)
			offspring += elite
			# Apply crossover and mutation
			offspring = algorithms.varAnd(offspring, toolbox, cx_prob, mut_prob)
			population[:] = offspring
			# Evaluate individuals
			print("Starting evaluation "+str(gen+1))
			fits = Parallel(n_jobs=14, prefer="threads")(delayed(toolbox.evaluate)(ind) for ind in population)
			print("Finished evaluation")
			# toolbox.map(toolbox.evaluate, population)
			save=""
			for ind, fit in zip(population, fits):
				ind.fitness.values = fit
				save += str(gen+1) + " " + str(fit) + "\n"
			with open("result_EA.txt","a") as f:
				f.write(save)
			np.savetxt("gen_"+str(gen+1)+".txt", population)

	time_elapsed = time.time()-start_time
	print("Time elapsed: "+str(time_elapsed))

if __name__ == '__main__':
	main()
