import random
import numpy as np

class Individual:
    def __init__(self, x = None, n = 2):
        self.left_range = -2048
        self.right_range = 2048
        if x is None:
            self.x = list(random.randrange(self.left_range, self.right_range) for i in range(n))
        else:
            self.x = x

    def fitness(self):
        value = 0
        for i in range(len(self.x) - 1):
            value = value + 100*(self.x[i + 1] - self.x[i]**2)**2 + (self.x[i] - 1)**2
        return -value

    def __lt__(self, other):
        return self.fitness() < other.fitness()

    def mutation(self):
        for i in range(len(self.x)):
            prob = random.uniform(0, 1)
            if prob <= 0.8:
                self.x[i] = random.randrange(self.left_range, self.right_range)
        return self


class Population:
    def __init__(self, size):
        self.population = list(Individual() for i in range(size))

    def print_population(self):
        print('Population:')
        for i in range(len(self.population)):
            print(self.population[i].x, 'fitness =', self.population[i].fitness())

    def parent_selection(self):
        self.population.sort(reverse=True)
        return [self.population[0], self.population[1]]

    def crossover(self, parents):
        parent1 = parents[0].x
        parent2 = parents[1].x
        x1 = [parent1[0], parent2[1]]
        x2 = [parent2[0], parent1[1]]
        return (Individual(x=x1), Individual(x=x2))

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



def f(x):
    value = 0
    for i in range(len(x) - 1):
        value = value + 100*(x[i + 1] - x[i]**2)**2 + (x[i] - 1)**2
    return value

def brute_force():
    minimum = (1e100, (-1, -1))
    for i in range(-2048, 2049):
        for j in range(-2048, 2049):
            curr = [i, j]
            minimum = min(minimum, (f(curr), (i, j)))

    return minimum

def main():
    #print(brute_force())
    # best solution: (0, (1, 1))

    num_generation = 100000
    population = Population(10)
    #population.print_population()
    
    n_generation = 0
    #for i in range(num_generation):
    while population.get_fittest_individual().fitness() != 0:
        n_generation += 1
        #print('\nn_generation =', n_generation)
        #print('fittest =', population.get_fittest_individual().x, population.get_fittest_individual().fitness())
        #print('population fitness mean =', population.population_fitness())

        # select the 2 fittest individuals 
        parents = population.parent_selection()
        #print('\nParents\n', parents[0].x, parents[1].x)

        offspring_crossover = population.crossover(parents)
        #print('\nOffpring Crossover\n', offspring_crossover[0].x, offspring_crossover[1].x)

        offspring_mutation = [x.mutation() for x in offspring_crossover]
        #print('\nOffpring Mutation\n', offspring_mutation[0].x, offspring_mutation[1].x)

        population.survival_selection(offspring_mutation)

    ans = population.get_fittest_individual()
    print('n_generation =', n_generation)
    print('best individual =', ans.x)
    print('minimum value =', -ans.fitness())


if __name__ == "__main__":
    main()