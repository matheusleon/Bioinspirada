import random
import numpy as np
from src.helper import translate_to_bin

class Individual:
    def __init__(self, x = None):
        pop_sample = [0, 1, 2, 3, 4, 5, 6, 7]
        random.shuffle(pop_sample)
        self.x = translate_to_bin(pop_sample)

    # TODO: ? 
    def fitness(self):
        return 0

    def __lt__(self, other):
        return self.fitness() < other.fitness()

    # TODO: troca de genes
    def mutation(self):
        mutation_prob = 0.4
        return self
