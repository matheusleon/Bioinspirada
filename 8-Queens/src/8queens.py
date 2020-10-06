import random
import numpy as np
import itertools
from lib.Population import Population

def main():
    crossover_params = ['Cut and Crossfill']
    mutation_params = ['swap', 'shuffle']
    parent_selection_params = ['Tournament Selection']
    survival_selection_params = ['worst replacement']
    population_size = [100]
    fitness_params = ['cnt_clash']

    for x in itertools.product(crossover_params, mutation_params, parent_selection_params, survival_selection_params, population_size, fitness_params):
        params = {'crossover': x[0], 'mutation': x[1], 'parent_selection': x[2], 'survival_selection': x[3], 'population_size': x[4], 'fitness': x[5]}
        
        population = Population(params)
        ans = population.evolve(verbose = True)

        #print(ans['n_generations'], ans['mean'])


if __name__ == "__main__":
    main()