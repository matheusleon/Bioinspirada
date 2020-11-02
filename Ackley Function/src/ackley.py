import random
import numpy as np
import itertools
from lib.population import Population
from lib.individual import Individual

def main():
    params = {'population_size': 100, 'crossover': 'mid_fixed_parents', 'mutation': 'individual_std', 'survival_selection': 'mi,lambda', 'mutation_prob' : 0.8}
    population = Population(params)
    population.evolve()

if __name__ == "__main__":
    main()
