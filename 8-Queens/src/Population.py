import random
import numpy as np
from Individual import Individual
from helper import translate_to_perm, crossover

class Population:
    def __init__(self, size):
        self.population = list(Individual() for i in range(size))

    def print_population(self):
        print('Population:')
        for person in self.population:
            print(person.x, translate_to_perm(person.x))

    # TODO: Melhor de 2 de 5 escolhidos aleatoriamente
    def parent_selection(self):
        random_parents = random.sample(self.population, 5)
        random_parents.sort(reverse=True)
        return [random_parents[0], random_parents[1]]

    # TODO: Recombinação: “cut-and-crossfill” crossover

    def survival_selection(self, offspring):
        population_size = len(self.population)
        for x in offspring:
            self.population.append(x)
        
        # select the fittest individuals
        self.population.sort(reverse=True)
        self.population = self.population[:population_size]

    def population_fitness(self):
        fitness = [x.fitness() for x in self.population]
        return np.mean(fitness)

    def get_fittest_individual(self):
        self.population.sort(reverse=True)
        return self.population[0]

    def train(self, n_iter):
        n_generation = 0
        population = self.population
        while population.get_fittest_individual().fitness() != 0 and n_generation < n_iter:
            n_generation += 1
            #print('\nn_generation =', n_generation)
            #print('fittest =', population.get_fittest_individual().x, population.get_fittest_individual().fitness())
            #print('population fitness mean =', population.population_fitness())

            # select the 2 fittest individuals 
            parents = population.parent_selection()
            #print('\nParents\n', parents[0].x, parents[1].x)

            offspring_crossover = crossover(parents[0], parents[1])
            #print('\nOffpring Crossover\n', offspring_crossover[0].x, offspring_crossover[1].x)

            offspring_mutation = [x.mutation() for x in offspring_crossover]
            #print('\nOffpring Mutation\n', offspring_mutation[0].x, offspring_mutation[1].x)
            
            population.survival_selection(offspring_mutation)