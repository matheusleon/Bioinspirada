import random
import numpy as np
import itertools
from lib.Population import Population
from lib.helper import plot_one_curve, plot_all_curves, bar_graph

class Result:
    def __init__(self, crossover, mutation, parent_selection, survival_selection, population_size, fitness, a, b, c, d, all_means, all_iter_converged, all_number_converged):
        self.crossover = crossover
        self.mutation = mutation
        self.parent_selection = parent_selection
        self.survival_selection = survival_selection
        self.population_size = population_size
        self.fitness = fitness

        self.cnt_converged = a 
        self.iter_converged = b 
        self.individuals_converged = c 
        self.mean_fitness = d
        self.all_means = all_means
        self.all_iter_converged = all_iter_converged
        self.all_number_converged = all_number_converged

    def print_result(self, number):
        print('----------------', flush=True)
        print('Representation:')
        print('Crossover:', self.crossover)
        print('Mutation:', self.mutation)
        print('Parent Selection:', self.parent_selection)
        print('Survival Selection:', self.survival_selection)
        print('Population Size:', self.population_size)
        print('Fitness:', self.fitness)
        print('')
        print('Results:')
        print('Em quantas execuções o algoritmo convergiu (n o /30 execuções)')
        print(self.cnt_converged)
        print('Em que iteração o algoritmo convergiu (média e desvio padrão)')
        print(self.iter_converged)
        print('Número de indivíduos que convergiram por execução')
        print(self.individuals_converged)
        print('Fitness médio alcançado nas 30 execuções (média e desvio padrão)')
        print(self.mean_fitness)
        ids = 0
        for i in range(len(self.all_means)):
            if len(self.all_means[i]) > len(self.all_means[ids]):
                ids = i
        plot_one_curve(self.all_means[ids], "Mean fitness", "", str(number) + ' fitness')
        #print(self.all_iter_converged)
        bar_graph(self.all_iter_converged, 'Iteration', '', str(number) + ' iteration')
        #print(self.all_number_converged)
        bar_graph(self.all_number_converged, 'Number of individuals who converged', '', str(number) + 'individuals')
        print('----------------', flush=True)
        

def sort_cnt_converged(a):
    return a.cnt_converged

def sort_iter_converged(a):
    return a.iter_converged

def sort_individuals_converged(a):
    return a.individuals_converged

def sort_mean_fitness(a):
    return a.mean_fitness

def print_best_results(results):
    
    print('Combinação que mais convergiu nas execuções')
    x = sorted(results, key=sort_cnt_converged, reverse=True)
    x[0].print_result(1)

    print('\n\nCombinação que convergiu mais rapidamente em média')
    x = sorted(results, key=sort_iter_converged)
    x[0].print_result(2)

    print('\n\nCombinação que mais individuos convergiram na ultima iteração em média')
    x = sorted(results, key=sort_individuals_converged, reverse=True)
    x[0].print_result(3)

    print('\n\nCombinação que teve o maior fitness médio nas execuções')
    x = sorted(results, key=sort_mean_fitness, reverse=True)
    x[0].print_result(4)

def main():
    crossover_params = ['Cut and Crossfill']
    mutation_params = ['swap']
    parent_selection_params = ['Tournament Selection']
    survival_selection_params = ['Generation']
    population_size = [100]
    fitness_params = ['inv_cnt_clash']

    results = []
    number_executions = 30
    
    cnt = 0

    for x in itertools.product(crossover_params, mutation_params, parent_selection_params, survival_selection_params, population_size, fitness_params):
        params = {'crossover': x[0], 'mutation': x[1], 'parent_selection': x[2], 'survival_selection': x[3], 'population_size': x[4], 'fitness': x[5]}
        print(params)
        
        cnt += 1
        print(cnt)
        
        cnt_converged = 0
        iter_converged = []
        number_converged = []
        fitness_mean = []
        all_means = []
        for i in range(number_executions):
            population = Population(params)
            ans = population.evolve(verbose = False)

            cnt_converged += int(ans['converged'])
            iter_converged.append(ans['n_generations'])
            number_converged.append(ans['number_converged'])
            fitness_mean.append(ans['mean'])

        a = cnt_converged / number_executions
        b = (np.mean(iter_converged), np.std(iter_converged))
        c = (np.mean(number_converged), np.std(number_converged))
        d = (np.mean(fitness_mean[:][-1]), np.std(fitness_mean[:][-1]))

        results.append(Result(params['crossover'], params['mutation'], params['parent_selection'], params['survival_selection'], params['population_size'], params['fitness'], a, b, c, d, fitness_mean, iter_converged, number_converged))

    print('PRIMEIRA IMPLEMENTAÇÃO')
    results[0].print_result(0)
    print('\n\n')

    print_best_results(results)

if __name__ == "__main__":
    main()
