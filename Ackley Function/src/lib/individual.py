import random
import numpy as np

class Individual:
    def __init__(self, n = 30, c1 = 20, c2 = 0.2, c3 = 2*np.pi, x = None):
        self.n = n
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.sigma = [1 for i in range(n)]
        self.t1 = 1 / np.sqrt(n)
        self.t2 = 1 / np.sqrt(np.sqrt(n))
        self.eps = 1e-6
        if x == None:
            self.x = [random.uniform(-15.0, 15.0) for i in range(n)]
        else:
            self.x = x

    def fitness(self):
        n, x, c1, c2, c3 = self. n, self.x, self.c1, self.c2, self.c3

        a = -c1 * np.exp(-c2 * np.sqrt((1 / n) * sum(map(lambda y: y*y, x))))
        b = -np.exp(1 / n * sum(map(lambda y : np.cos(c3 * y), x))) + c1 + np.exp(1)
        return a + b

    def __lt__(self, other):
        return self.fitness() < other.fitness()

    def mutate(self, method):
        if (method == 'individual_std'):
            self.sigma = [max(s * np.exp(self.t1 * np.random.normal(0, 1) + self.t2 * np.random.normal(0, 1)), self.eps) for s in self.sigma]
            self.x = [x + sigma * np.random.normal(0, 1) for (x, sigma) in zip(self.x, self.sigma)]
            self.x = [min(15, max(x, -15)) for x in self.x]
        
        return self