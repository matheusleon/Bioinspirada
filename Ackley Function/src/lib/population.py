import random
import numpy as np
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
        self.mi = 20
        self.lamb = 100
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
            aux = parents.copy()
            aux.extend(offspring)
        if self.params['survival_selection'] == 'mi,lambda':
            aux = offspring
        aux.sort()
        return aux[:len(parents)]

    def metrics(self):
        vals = [x.fitness() for x in self.population]
        return {"best" : np.min(vals), "mean" : np.mean(vals)}

    def stale(self, means):
        if len(means) < 200:
            return False
        vals = means[-200:]
        return np.std(vals) < 0.1

    def evolve(self, verbose = False):
        
        params = self.params
        curr_iter = 0
        stats = self.metrics()
        means = []

        while stats['best'] != 0 and curr_iter < 1000:
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
            
            self.population = new_pop

            stats = self.metrics()
            means.append(stats['mean'])

            print(curr_iter, self.mi, len(self.population), stats['mean'])

            if self.stale(means):
                print('population is stuck in local minimum')
                for ind in self.population:
                    ind.sigma = [random.uniform(0.1, 0.25) for sig in ind.sigma]
                    means.clear()


        print('CHEGOUUUU ', self.metrics()['best'])
            
        return self