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
from copy import copy
import itertools

import random
from deap import creator, base, tools, algorithms
from codecs import decode
import struct

# Init distance variables for the reading function used in tuning
OLD_DISTANCE = np.inf
N_RUNS = 0
testing = False  # If this is true the reading function is not carried out and returns random numbers (intended for testing the EA)
fname = ""  # File name specifying the location of the last saved generation from which should be started, if empty evaluation starts from beginning
generation = 0
#start_params = [0.10111091566085817, 0.7605561652753674, 15.361500000000003, 10.6993519565625, 6.3890415969187515]

def main():
	# Reading function for tuning (called by the EA)
	def reading_function(parameters_rf):
		global OLD_DISTANCE
		global N_RUNS
		filename = "PSC_ALL"
		filepath_psc = "PSC/" + filename + ".txt"
		if testing:
			distance = random.randint(1000000, 5000000)
			N_RUNS += 1
			print("TESTING, READING FUNCTION IS NOT BEING EXECUTED")
			print("Returning: "+str(distance))
			return (distance,)
		try:
			# Run the simulation
			(lexicon, all_data, unrecognized_words) = reading_simulation(filepath_psc, parameters_rf)
			# Evaluate run and retrieve error-metric
			distance = get_scores(filename, all_data, unrecognized_words)
		except:
			print("Reading function error: returning distance=99999999")
			distance = 99999999.0
			N_RUNS += 1
			return (distance,)
		N_RUNS += 1
		global generation
		with open("result_EA.txt","a") as f:
			f.write(str(generation) + " " + str(distance) + "\n" + str(parameters_rf) + "\n\n")
		return (distance,)

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
		pop_size = 15
		multi_processing = True
		gens = 7
		tournament_size = 5
		cx_prob = 0.2
		if testing:
			cx_prob = 1
		# Mutation = +-10%
		mut_size = 0.1
		mut_prob = 0.2
		if testing:
			mut_prob = 1
		global generation

		# Create fitness
		creator.create("FitnessMin", base.Fitness, weights=(-1.0,))

		# Create Individual
		creator.create("Individual", list, fitness=creator.FitnessMin)

		def high(x):
#			return x*2
			return x*1.33

		def low(x):
#			return x/2
			return x*0.75

		def same(x):
			return x

		def mutate(gen, p):
			print("-----------------------\nGene before\n"+str(gen))
			for i, allele in enumerate(gen):
				# Mutation takes place
				if random.uniform(0,1) < p:
					print("Mutation of gene "+str(gen[i]))
					# Either + or - 10% of the original value
					gen[i] = allele + (allele * mut_size) if random.randint(0, 1) else allele - (allele * mut_size)
					print("to: "+str(gen[i]))
			print("Gene after\n"+str(gen)+"\n-----------------------")
			return gen,

		def initIndividual(icls, content):
			return icls(content)

		def initPopulation(pcls, ind_init):
			global start_params
			print("Initializing pop with "+str(start_params))
			n_params = 5
			combinaties = [list(x) for x in list(itertools.product([same, high, low], repeat=n_params))]
#			start_params = [4.0, 1.29, 7.0, 4.9, 2.2]
			contents = [[y(z) for y, z in zip(x, start_params)] for x in combinaties]
			return pcls(ind_init(c) for c in contents)

		def load_pop(pcls, ind_init):
			global fname
			print("Loading: "+str(fname))
			contents = np.loadtxt(fname)
			return pcls(ind_init(c) for c in contents)

		def initPopulationSingle(pcls, ind_init):
			contents = [[float(x)] for x in list(range(1,16))]
			print("Initiating with: "+str(contents))
			return pcls(ind_init(c) for c in contents)

		def mateSingle(ind1, ind2):
			print("Mating: "+str(ind1)+" and "+str(ind2))
			difference = abs(ind1[0]-ind2[0])
			if ind1 > ind2:
				higher = ind1
				lower = ind2
			else:
				higher = ind2
				lower = ind1
			print("Difference: "+str(difference))
			print("Result: "+str(higher[0]-difference/3)+" and "+str(lower[0]+difference/3))
			higher[0] = higher[0]-difference/3
			lower[0] = lower[0]+difference/3
			return higher, lower

		toolbox = base.Toolbox()

		toolbox.register("individual_guess", initIndividual, creator.Individual)

#		if not fname:
#			toolbox.register("population_guess", initPopulation, list, toolbox.individual_guess)
#		else:
#			print("STARTING FROM "+str(fname)+" AS STARTING POPULATION")
#			toolbox.register("population_guess", load_pop, list, toolbox.individual_guess)

		toolbox.register("population_guess", initPopulationSingle, list, toolbox.individual_guess)
		population = toolbox.population_guess()

		print(population)

		# Define operators
#		toolbox.register("mate", tools.cxOnePoint)
		toolbox.register("mate", mateSingle)
		toolbox.register("mutate", mutate, p=mut_prob)
		toolbox.register("select", tools.selTournament, tournsize=tournament_size)
		toolbox.register("evaluate", reading_function)

		if not fname:
			# Evaluate first population
			print("Start evaluation gen 0")
#			fits = Parallel(n_jobs=8)(delayed(toolbox.evaluate)(ind) for ind in population)
			fits = [toolbox.evaluate(ind) for ind in population]
			print("Finished evaluation")
			#toolbox.map(toolbox.evaluate, population)
			for ind, fit in zip(population, fits):
				ind.fitness.values = fit
			np.savetxt("gen_0.txt", population)
			start_gen = 0
		else:
			start_gen = int(fname.split("_")[1].split(".")[0])
			print("Starting from generation "+str(start_gen))
		# Main evolution loop
		for gen in range(gens):
			generation += 1
			#pop_size /= 2
			print("Gen:"+str(gen+1))
			print("Pop-size:"+str(pop_size))
			# If generation is restarted we skip past generations and load the fitness from the output-file
			if gen < start_gen:
				continue
			if gen == start_gen:
				if fname:
					with open("result_EA.txt","r") as f:
						print("Reading fitness fom file...")
						fits = [float(x.replace("\n","").split(" ")[1]) for x in f.readlines() if str(start_gen)+" " in x]
					pop_size = len(fits) / 2
					print("Updated pop_size to: "+str(pop_size))
					for ind, fit in zip(population, fits):
						print("Reinitializing:\n"+str(ind)+"\nwith fitness\n"+str(fit))
						ind.fitness.value = fit
			# Select fittest individuals
			offspring = map(toolbox.clone, toolbox.select(population, pop_size))
			# Apply crossover and mutation
			offspring = algorithms.varAnd(offspring, toolbox, cx_prob, mut_prob)
			print("Offspring: "+str(offspring))
#			offspring += elite
			# Evaluate individuals
#			offspring = toolbox.population_guess()
			print("Starting evaluation "+str(gen+1))
#			fits = Parallel(n_jobs=8)(delayed(toolbox.evaluate)(ind) for ind in offspring)
			fits = [toolbox.evaluate(ind) for ind in offspring]
			print("Finished evaluation")
			# toolbox.map(toolbox.evaluate, population)
			save=""
			for ind, fit in zip(offspring, fits):
				ind.fitness.values = fit
			population[:] = offspring
			np.savetxt("gen_"+str(gen+1)+".txt", population)

	time_elapsed = time.time()-start_time
	print("Time elapsed: "+str(time_elapsed))

if __name__ == '__main__':
	main()
