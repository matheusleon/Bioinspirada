import random
import numpy as np
from lib.Population import Population

def main():
    population = Population(10)

    population.train(1000)
    
    #ans = population.get_fittest_individual()
    #print('n_generation =', n_generation)
    #print('best individual =', ans.x)
    #print('minimum value =', -ans.fitness())


if __name__ == "__main__":
    main()