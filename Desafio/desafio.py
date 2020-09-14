import random

class Individual:
    def __init__(self, n = 2):
        self.x = list(random.randrange(-100, 100) for i in range(n))

    def fitness(self):
        value = 0
        for i in range(len(self.x) - 1):
            value = value + 100*(self.x[i + 1] - self.x[i]**2)**2 + (self.x[i] - 1)**2
        return value

    def __lt__(self, other):
        return self.fitness() < other.fitness()

    #def mutation(self):

class Population:
    def __init__(self, size):
        self.population = list(Individual() for i in range(size))

    def printPopulation(self):
        print('Population:')
        for i in range(len(self.population)):
            print(self.population[i].x, 'fitness =', self.population[i].fitness())

    def parentSelection(self):
        self.population.sort(reverse=True)
        self.printPopulation()
        return [(self.population[0], self.population[1]), (self.population[2], self.population[3])]

    #def survivalSelection(self, offspring):



def main():
    p = Population(5)
    


if __name__ == "__main__":
    main()