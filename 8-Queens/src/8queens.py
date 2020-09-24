import random
import numpy as np
from lib.Population import Population

def main():
    population = Population(100)

    ans = population.evolve(1000, verbose = False)
    
    print(ans['n_generations'], ans['mean'])

if __name__ == "__main__":
    main()