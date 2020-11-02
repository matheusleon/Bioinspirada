import random
import numpy as np
from .individual import Individual
import concurrent.futures

class Population:
    def __init__(self, params):
        self.params = params
        self.population_size = params['population_size']
        self.population = [Individual(mutation=params['mutation']) for i in range(params['population_size'])]
        self.mi = 10
        self.lamb = 50

    def print_population(self):
        for individual in self.population:
            print(individual.x)

    def parent_selection(self):
        return list(random.sample(self.population, self.mi))

    def crossover_parent(self, p1, p2):
        n = len(p1.x)
        x_child = []
        nxt_sigma = []
        if self.params['crossover'] == 'mid_fixed_parents':
            for i in range(n):
                x_child.append((p1.x[i] + p2.x[i]) / 2.0)
                nxt_sigma.append((p1.sigma[i] + p2.sigma[i]) / 2.0)
        return Individual(x = x_child, sigma = nxt_sigma, mutation = self.params['mutation'])
        
    def one_child(self, parents):
        p1, p2 = random.sample(parents, 2)
        return self.crossover_parent(p1, p2)

    def crossover(self, parents):
        children_submit = [concurrent.futures.ThreadPoolExecutor(max_workers=8).submit(self.one_child, parents) for x in range(0, self.lamb)]
        children = [cs.result() for cs in children_submit]
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
        vals = [(x.fitness(), x.sigma) for x in self.population]
        true_vals = [x.fitness() for x in self.population] 
        return {"best" : min(vals), "mean" : np.mean(true_vals), "std" : np.std(true_vals)}

    def evolve(self, verbose = False):
        
        params = self.params
        curr_iter = 0
        stats = self.metrics()
        
        print(stats)

        while stats['best'] != 0 and curr_iter < 10000:
            curr_iter += 1
            
            if curr_iter % 2000 == 1000:
                self.params['survival_selection'] = 'mi+lambda'
                self.population = [x.update_sigma(2.0 / 3) for x in self.population]
            elif curr_iter % 2000 == 0:
                self.params['survival_selection'] = 'mi,lambda'
                self.population = [x.update_sigma(1.5) for x in self.population]

            # select mi parents
            parents = self.parent_selection()

            # generate lambda children
            offspring_crossover = self.crossover(parents)
            
            # possibly mutate children
            offspring_mutation = [(x.mutate(params['mutation']) if np.random.uniform(0, 1) < self.params['mutation_prob'] else x) for x in offspring_crossover]

            new_pop = []
            for ind in self.population:
                if ind not in parents:
                    new_pop.append(ind)

            new_pop.extend(self.survival_selection(parents, offspring_mutation))
            
            self.population = new_pop

            
            if curr_iter % 50 == 0:
                stats = self.metrics()
                print(curr_iter, self.mi, len(self.population), stats['best'], self.params['survival_selection'])
            
            #if curr_iter % 300 == 0:
                #self.mi -= 1
                #self.lamb += 5

        print('CHEGOUUUU ', self.metrics()['best'])
            
        return self
