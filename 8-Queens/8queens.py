import random
import numpy as np
from src.Population import Population

def main():
    population = Population(100)

    population.print_population()
    
    #population.train(10000)
    
    #ans = population.get_fittest_individual()
    #print('n_generation =', n_generation)
    #print('best individual =', ans.x)
    #print('minimum value =', -ans.fitness())


if __name__ == "__main__":
    main()