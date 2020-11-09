from firefly import Firefly
import numpy as np

#self.alfa = 0.4      self.g = 0.02
class Population:
    def __init__(self, tam, max_iter):
        self.n = tam
        self.pop = [Firefly() for i in range(tam)]
        self.max_iter = max_iter
        self.alfa = 0.003
        self.alfa2 = 0.002
        self.g = 0.3

    def distance(self, f1, f2):
        sum = 0
        step = []
        for i in range(len(f1.x)):
            sum += np.square(f1.x[i] - f2.x[i])
            step += [f2.x[i] - f1.x[i]]
        return np.sqrt(sum), step

    def metrics(self):
        vals = [x.cur_brightness for x in self.pop]
        return {"mean" : np.mean(vals), "best" : np.min(vals), "std" : np.std(vals)}

    def evolve(self):
        for gen in range(self.max_iter):            
            self.pop.sort()
            self.alfa = np.power(1.11 * 1e-4, 5 / self.max_iter) * self.alfa

            for i in range(len(self.pop)):
                f1 = self.pop[i]
                for j in range(len(self.pop)):
                    f2 = self.pop[j]

                    if f1.cur_brightness > f2.cur_brightness:
                        r, step = self.distance(f1, f2)
                        beta = np.exp(-self.g * r)
                        init = [x * (1 - beta) for x in f1.x]
                        step = [ x * beta for x in step]
                        random_step = [self.alfa * (np.random.uniform(0, 1) - 0.5) for i in range(len(f1.x))]             
                        f1.x = np.sum([init, step, random_step], axis = 0)
                        f1.cur_brightness = f1.brightness()

            if gen % 10 == 0:
                stats = self.metrics()     
                print(gen, stats["mean"], stats["std"], stats["best"], self.alfa)
        
        self.pop.sort()
        print(self.pop[0].x)              