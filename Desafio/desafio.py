import random

class Individual:
    def __init__(self, x = None, n = 2):
        self.left_range = -100
        self.right_range = 100
        if x is None:
            self.x = list(random.randrange(self.left_range, self.right_range) for i in range(n))
        else:
            self.x = x

    def fitness(self):
        value = 0
        for i in range(len(self.x) - 1):
            value = value + 100*(self.x[i + 1] - self.x[i]**2)**2 + (self.x[i] - 1)**2
        return value

    def __lt__(self, other):
        return self.fitness() < other.fitness()

    def mutation(self):
        for i in range(len(self.x)):
            prob = random.uniform(0, 1)
            if prob <= 0.8:
                self.x[i] = random.randrange(self.left_range, self.right_range)


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
        x1 = [parents[0][0], parents[1][1]]
        x2 = [parents[1][0], parents[0][1]]
        return (Individual(x=x1), Individual(x=x2))

    def survival_selection(self, offspring):
        population_size = len(self.population)
        for x in offspring:
            self.population.append(x)
        
        # select the fittest individuals
        self.population.sort(reverse=True)
        self.population = self.population[:population_size]


def main():
    population = Population(5)


if __name__ == "__main__":
    main()