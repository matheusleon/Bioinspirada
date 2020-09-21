import random
import numpy as np

class Individual:
    def __init__(self, x = None):
        self.x = random.randrange(0, 1 << 24)

    # TODO: ? 
    def fitness(self):
        return 0

    def __lt__(self, other):
        return self.fitness() < other.fitness()

    # TODO: troca de genes
    def mutation(self):
        mutation_prob = 0.4
        return self


class Population:
    def __init__(self, size):
        self.population = list(Individual() for i in range(size))

    def print_population(self):
        print('Population:')
        for i in range(len(self.population)):
            print(self.population[i].x, 'fitness =', self.population[i].fitness())

    # TODO: Melhor de 2 de 5 escolhidos aleatoriamente
    def parent_selection(self):
        return self

    # TODO: Recombinação: “cut-and-crossfill” crossover
    def crossover(self, parents):
        parent1 = parents[0].x
        parent2 = parents[1].x
        prob = random.uniform(0, 1)
        if prob <= 0.9:
            x1 = [parent1[0], parent2[1]]
            x2 = [parent2[0], parent1[1]]
        else:
            x1 = parent1
            x2 = parent2
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

def main():
    population = Population(100)
    #population.print_population()
    
    n_generation = 0
    while population.get_fittest_individual().fitness() != 0 and n_generation < 10000:
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