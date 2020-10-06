import random
import numpy as np
from lib.Individual import Individual
from lib.helper import translate_to_perm


class Population:
    def __init__(self, size):
        self.n = size
        self.population = list(Individual() for i in range(size))

    def print_population(self):
        print('Population:')
        for person in self.population:
            print(person.x, translate_to_perm(person.x))

    # TODO: Melhor de 2 de 5 escolhidos aleatoriamente
    
    def get_roullete(self):
        mn = min([x.fitness() for x in self.population]) - 1
        fitness_sum = sum([x.fitness() - mn for x in self.population])
        rand_id = random.randint(1, fitness_sum)
        for i in range(self.n):
            fitness_sum -= self.population[i].fitness() - mn
            if fitness_sum <= 0:
                return self.population[i]
      
    def parent_selection(self, method):
        if method == 'random':
            random_parents = random.sample(self.population, 5	)
            random_parents.sort(reverse=True)
            return [random_parents[0], random_parents[1]]
        elif method == 'roulette':
            return [self.get_roullete(), self.get_roullete()]

    # TODO: Recombinação: “cut-and-crossfill” crossover
    #implement cut and crossfill with p1 and p2
    def crossover(self, p1, p2):
        perm1 = translate_to_perm(p1.x)
        perm2 = translate_to_perm(p2.x)
        
        crossfill_pt = random.randint(0, 7)
        
        son1, son2 = perm1[:crossfill_pt], perm2[:crossfill_pt]
        
        pos = crossfill_pt
        while len(son1) != len(perm1):
            if perm2[pos] not in son1:
                son1.append(perm2[pos])
            pos = (pos + 1) % len(perm2)

        pos = crossfill_pt
        while len(son2) != len(perm2):
            if perm1[pos] not in son2:
                son2.append(perm1[pos])
            pos = (pos + 1) % len(perm1)

        r = random.uniform(0, 1)
        if r <= 0.9:
            return [Individual(son1), Individual(son2)]
        else:
            return [p1, p2]

    # select the fittest individuals
    def survival_selection(self):
        self.population.sort(reverse=True)
        self.population = self.population[:self.n]

    def population_fitness_analysis(self):
        fitness = [x.fitness() for x in self.population]
        return (np.mean(fitness), np.std(fitness), np.min(fitness), np.max(fitness))

    def get_fittest_individual(self):
        self.population.sort(reverse=True)
        return self.population[0]

    def evolve(self, n_iter, recombination_method = 'crossover', mutation_method = 'swap', parent_selection_method = 'random', survival_selection_method = 'worst', verbose = False):
        n_iteration = 0
        ans_mean, ans_std, ans_min, ans_max, individuals_converged = [], [], [], [], 0
        while self.get_fittest_individual().fitness() != 0 and n_iteration < n_iter:
            #self.print_population()

            n_iteration += 1

            # select the 2 fittest individuals 
            parents = self.parent_selection(parent_selection_method)

            #create children
            offspring_crossover = self.crossover(parents[0], parents[1])

            #possibly mutate children
            offspring_mutation = [x.mutation(method = 'swap') for x in offspring_crossover]
            
            #add children to the population
            self.population.extend(offspring_mutation)
            
            #self.print_population()

            #select new generation
            self.survival_selection()

            mean, std, min_val, max_val = self.population_fitness_analysis()

            ans_mean.append(mean)
            ans_std.append(std)
            ans_min.append(min_val)
            ans_max.append(max_val)

            if verbose:
                print('----------------')
                print('Generation number {}:\nBest individual has fitness {}.\nWorst individual has fitness {}.\nMean fitness is {}.\nStd is {}.'.format(n_iteration, max_val, min_val, mean, std))
                print('----------------')
                
        individuals_converged = sum([x.fitness() == 0 for x in self.population])

        return {"n_iterations" : n_iteration, "number_of_individuals_who_converged": individuals_converged, "mean" : ans_mean, "std" : ans_std, "min" : ans_min, "max" : ans_max}
