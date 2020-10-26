import random
import numpy as np

class Individual:
    def __init__(self, n = 30, c1 = 20, c2 = 0.2, c3 = 2*np.pi):
        self.n = n
        self.x = [random.uniform(-15.0, 15.0) for i in range(n)]
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
            
    def fitness(self):
        n, x, c1, c2, c3 = self. n, self.x, self.c1, self.c2, self.c3

        a = -c1 * np.exp(-c2 * np.sqrt((1 / n) * sum(map(lambda y: y*y, x))))
        b = -np.exp(1 / n * sum(map(lambda y : np.cos(c3 * y), x))) + c1 + 1
        return a + b

    def __lt__(self, other):
        return self.fitness() < other.fitness()

    def mutation(self, method):
        return self
