import random
import numpy as np
from lib.Population import Population
from lib.helper import plot_curve

def main():
    population = Population(100)

    ans = population.evolve(1000, mutation_method = 'swap', verbose = False)
    
    print(ans['n_iterations'], ans['mean'])
    
    print(ans['max'])
    
    print(ans['number_of_individuals_who_converged'])
    
    plot_curve(ans['mean'], 'Mean fitness', '')

if __name__ == "__main__":
    main()
