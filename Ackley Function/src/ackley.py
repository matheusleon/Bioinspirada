import random
import numpy as np
import itertools
from lib.population import Population
from lib.individual import Individual

def main():
    #params = {'population_size': 2}
    #population = Population(params)
    #population.print_population()
    #n_generation = 0

    ind = Individual()

    print(ind.x[:5], ind.sigma[:5])
    ind.mutate()
    print(ind.x[:5], ind.sigma[:5])
    
    """
    while population.get_fittest_individual().fitness() != 0:
        n_generation += 1
        parents = population.parent_selection()

        offspring_crossover = population.crossover(parents)

        offspring_mutation = [x.mutation() for x in offspring_crossover]

        population.survival_selection(offspring_mutation)

    print('Found solution in', n_generation, 'generation')
    """

if __name__ == "__main__":
    main()
