import random
import numpy as np
from lib.helper import translate_to_bin, translate_to_perm

class Individual:
    def __init__(self, x = None):
        if x is None:
            pop_sample = [0, 1, 2, 3, 4, 5, 6, 7]
            random.shuffle(pop_sample)
            self.x = translate_to_bin(pop_sample)
        else:
            self.x = translate_to_bin(x)
            
    def fitness(self):
        perm = translate_to_perm(self.x)
        fitness_val = 0
        for y1, x1 in enumerate(perm):
            for y2, x2 in enumerate(perm):
                if y1 != y2:
                    dx = abs(x1 - x2)
                    dy = abs(y1 - y2)
                    if (x1 == x2 or y1 == y2 or dx == dy):
                        fitness_val += 1
        return -fitness_val

    def __lt__(self, other):
        return self.fitness() < other.fitness()

    # TODO: troca de genes
    def mutation(self, method):
        mutation_prob = 0.4
        prob = random.uniform(0, 1)
        if prob <= mutation_prob:
            if method == 'shuffle':
                perm = translate_to_perm(self.x)
                random.shuffle(perm)
                self.x = translate_to_bin(perm)
            elif method == 'swap':
                perm = [0, 1, 2, 3, 4, 5, 6, 7]
                change = random.sample(perm, 2)
                pop = translate_to_perm(self.x)
                pop[change[0]], pop[change[1]] = pop[change[1]], pop[change[0]]
                self.x = translate_to_bin(pop)
            elif method == 'shuffle_subarray':
                perm_or = [0, 1, 2, 3, 4, 5, 6, 7]
                change = random.sample(perm_or, 2)
                if change[0] > change[1]:
                  swap(change[0], change[1])
                cur_perm = translate_to_perm(self.x)
                cur_perm[change[0] : change[1]] = random.shuffle(cur_perm[change[0] : change[1]])
                self.x = translate_to_bin(cur_perm)
        return self
