import numpy as np
from ackley import ackley

class Firefly:
    def __init__(self):
        self.n = 30
        self.x = [np.random.uniform(-5, 5) for i in range(self.n)]
        self.cur_brightness = self.brightness()

    def brightness(self):
        return ackley(self.x)

    def __lt__(self, other):
        return self.brightness() < other.brightness()