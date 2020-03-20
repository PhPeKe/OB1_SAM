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

# Init distance variables for the reading function used in tuning
OLD_DISTANCE = np.inf
N_RUNS = 0
fname = "gen_1.txt"  # File name specifying the location of the last saved generation from which should be started, if empty evaluation starts from beginning

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
		try:
			(lexicon, all_data, unrecognized_words) = reading_simulation(filepath_psc, parameters_rf)
			# Evaluate run and retrieve error-metric
			distance = get_scores(filename, all_data, unrecognized_words)
		except:
			print("Reading function error: returning distance=99999999")
			distance = 99999999.0
			N_RUNS += 1
			return (distance,)
		# Save parameters when distance is better than previous
#		write_out = pd.DataFrame(np.array([names, parameters_rf]).T)
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
		pop_size = 243
		multi_processing = True
		gens = 7
		tournament_size = 5
		cx_prob = 0.2
		# Mutation = +-10%
		mut_size = 0.1
		mut_prob = 0.1

		# Create fitness
		creator.create("FitnessMin", base.Fitness, weights=(-1.0,))

		# Create Individual
		creator.create("Individual", list, fitness=creator.FitnessMin)

		def high(x):
			return x*2

		def low(x):
			return x/2

		def same(x):
			return x

		def mutate(gen, p):
			print("-----------------------\nGene before\n"+str(gen))
			for i, allele in enumerate(gen):
				# Mutation takes place
				if random.uniform(0,1) > p:
					print("Mutation of gene "+str(gen[i]))
					# Either + or - 10% of the original value
					gen[i] = allele + (allele * mut_size) if random.randint(0, 1) else allele - (allele * mut_size)
					print("to: "+str(gen[i]))
			print("Gene after\n"+str(gen)+"\n-----------------------")
			return gen,

		def initIndividual(icls, content):
			return icls(content)

		def initPopulation(pcls, ind_init):
			n_params = 5
			combinaties = [list(x) for x in list(itertools.product([same, high, low], repeat=n_params))]
			start_params = [4.0, 1.29, 7.0, 4.9, 2.2]
			contents = [[y(z) for y, z in zip(x, start_params)] for x in combinaties]
			return pcls(ind_init(c) for c in contents)

		def load_pop(pcls, ind_init):
			global fname
			print("Loading: "+str(fname))
			contents = np.loadtxt(fname)
			return pcls(ind_init(c) for c in contents)

		toolbox = base.Toolbox()

		toolbox.register("individual_guess", initIndividual, creator.Individual)
		if not fname:
			toolbox.register("population_guess", initPopulation, list, toolbox.individual_guess)
		else:
			print("STARTING FROM "+str(fname)+" AS STARTING POPULATION")
			toolbox.register("population_guess", load_pop, list, toolbox.individual_guess)

		population = toolbox.population_guess()

		print(population)

		# Define operators
		toolbox.register("mate", tools.cxOnePoint)
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
			save=""
			for ind, fit in zip(population, fits):
				ind.fitness.values = fit
				save += "0 " + str(fit[0]) + "\n"
			with open("result_EA.txt","a") as f:
				f.write(save)
			np.savetxt("gen_0.txt", population)
		else:
			start_gen = int(fname.split("_")[1].split(".")[0])
			print("Starting from generation "+str(start_gen))
		# Main evolution loop
		for gen in range(gens):
			pop_size /= 2
			print("Gen:"+str(gen+1))
			print("Pop-size:"+str(pop_size))
			# If generation is restarted we skip past generations and load the fitness from the output-file
			if gen+1 < start_gen:
				continue
			if gen+1 == start_gen:
				with open("result_EA.txt","r") as f:
					print("Reading fitness fom file...")
					fits = [float(x.replace("\n","").split(" ")[1]) for x in f.readlines() if str(start_gen) in x]
				pop_size = len(fits) / 2
				print("Updated pop_size to: "+str(pop_size))
				for ind, fit in zip(population, fits):
					print("Reinitializing:\n"+str(ind)+"\nwith fitness\n"+str(fit))
					ind.fitness.value = fit
			# Select fittest individuals
			offspring = map(toolbox.clone, toolbox.select(population, pop_size))
			elite = tools.selBest(population, k=1)
			# Apply crossover and mutation
			offspring = algorithms.varAnd(offspring, toolbox, cx_prob, mut_prob)
			offspring += elite
			# Evaluate individuals
			print("Starting evaluation "+str(gen+1))
#			fits = Parallel(n_jobs=8)(delayed(toolbox.evaluate)(ind) for ind in offspring)
			fits = [toolbox.evaluate(ind) for ind in offspring]
			print("Finished evaluation")
			# toolbox.map(toolbox.evaluate, population)
			save=""
			for ind, fit in zip(offspring, fits):
				ind.fitness.values = fit
				save += str(gen+1) + " " + str(fit[0]) + "\n"
			population[:] = offspring
			with open("result_EA.txt","a") as f:
				f.write(save)
			np.savetxt("gen_"+str(gen+1)+".txt", population)

	time_elapsed = time.time()-start_time
	print("Time elapsed: "+str(time_elapsed))

if __name__ == '__main__':
	main()
