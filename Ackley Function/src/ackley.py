import random
import numpy as np
import itertools
from lib.population import Population
from lib.individual import Individual

def main():
    params = {'population_size': 200, 'crossover': 'mid_fixed_parents', 'mutation': 'individual_std', 'survival_selection': 'mi+lambda'}
    population = Population(params)
    #population.print_population()
    n_generation = 0

    """
    ind = Individual()
    print(ind.x[:5], ind.sigma[:5])
    ind.mutate()
    print(ind.x[:5], ind.sigma[:5])
    """
    population.evolve()

if __name__ == "__main__":
    main()
