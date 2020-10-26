import random
import numpy as numpy
from .individual import Individual

class Population:
    def __init__(self, params):
        self.population_size = params['population_size']
        self.population = [Individual() for i in range(params['population_size'])]

    def print_population(self):
        for individual in self.population:
            print(individual.x)

    def parent_selection(self):
        return self

    def crossover(self, p1, p2):
        return self

    def survival_selection(self):
        return self

    def get_fittest_individual(self):
        return self.population[0]

    def get_worst_individual(self):
        return self

    def evolve(self, verbose = False):
        return self