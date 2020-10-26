import random
import numpy as numpy
from .individual import Individual

class Population:
    def __init__(self, params):
        self.params = params
        self.population_size = params['population_size']
        self.population = [Individual() for i in range(params['population_size'])]
        self.mi = random.randint(2, self.population_size)
        self.lamb = 7 * self.mi

    def print_population(self):
        for individual in self.population:
            print(individual.x)

    def parent_selection(self):
        return list(random.sample(self.population, self.mi))

    def crossover_parent(self, p1, p2):
        n = len(p1.x)
        x_child = []
        if self.params['crossover'] == 'mid_fixed_parents':
            for i in range(n):
                x_child.append((p1.x[i] + p2.x[i]) / 2.0)
        return Individual(x = x_child)

    def crossover(self, parents):
        children = []
        while len(children) != self.lamb:
            p1, p2 = random.sample(parents, 2)
            children.append(self.crossover_parent(p1, p2))
        return children

    def survival_selection(self, parents, offspring):
        aux = []
        if self.params['survival_selection'] == 'mi+lambda':
            aux = parents
            aux.extend(offspring)
        if self.params['survival_selection'] == 'mi,lambda':
            aux = offspring
        aux.sort()
        return aux[:len(parents)]

    def get_fittest_individual(self):
        self.population.sort()
        return self.population[0]

    def evolve(self, verbose = False):
        
        params = self.params
        curr_iter = 0
        while (self.get_fittest_individual().fitness != 0):
            curr_iter += 1

            # select mi parents
            parents = self.parent_selection()

            # generate lambda children
            offspring_crossover = self.crossover(parents)
            
            # possibly mutate children
            offspring_mutation = [x.mutate(params['mutation']) for x in offspring_crossover]

            new_pop = []
            for ind in self.population:
                if ind not in parents:
                    new_pop.append(ind)

            new_pop.extend(self.survival_selection(parents, offspring_mutation))

            print(curr_iter, len(self.population), self.get_fittest_individual().fitness())
            
        return self