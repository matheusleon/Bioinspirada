import numpy as np

c1 = 20
c2 = 0.2
c3 = 2 * np.pi


def ackley(x):
    n = len(x)
    a = -c1 * np.exp(-c2 * np.sqrt((1 / n) * sum(map(lambda y: y*y, x))))
    b = -np.exp(1 / n * sum(map(lambda y : np.cos(c3 * y), x))) + c1 + np.exp(1)
    return a + b