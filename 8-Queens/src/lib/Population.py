import random
import numpy as np
from lib.Individual import Individual
from lib.helper import translate_to_perm

class Population:
    def __init__(self, params):
        self.params = params
        self.population = list(Individual(fitness_method = params['fitness']) for i in range(params['population_size']))
        #self.population_fitness = [x.fitness() for x in self.population]
        if params['fitness'] == 'cnt_clash':
            self.fitness_max = 8 * 8 + 1
        elif params['fitness'] == 'inv_cnt_clash':
            self.fitness_max = 1
            

    def print_population(self):
        print('Population:')
        for person in self.population:
            print(person.x, translate_to_perm(person.x), person.fitness())
            
    def get_roullete(self):
        fitness_sum = sum([x.fitness() for x in self.population])
        rand_id = random.uniform(0, fitness_sum)
        for i in range(self.params['population_size']):
            fitness_sum -= self.population[i].fitness()
            if fitness_sum <= 1e-5:
                return (i, self.population[i])
        return (self.params['population_size'] - 1, self.population[-1])

    # TODO: Melhor de 2 de 5 escolhidos aleatoriamente
    def parent_selection(self):
        if self.params['parent_selection'] == 'Tournament Selection':
            all = list(zip(self.population, range(self.params['population_size'])))
            random_parents = random.sample(all, 5)
            random_parents.sort(reverse=True)
            return [random_parents[0][0], random_parents[1][0], random_parents[0][1], random_parents[1][1]]
        elif self.params['parent_selection'] == 'Roulette':
            first = self.get_roullete()
            second = self.get_roullete()
            return [first[1], second[1], first[0], second[0]]
        

    # TODO: Recombinação: “cut-and-crossfill” crossover
    #implement cut and crossfill with p1 and p2
    def crossover(self, p1, p2):
        if self.params['crossover'] == 'Cut and Crossfill':
            perm1 = translate_to_perm(p1.x)
            perm2 = translate_to_perm(p2.x)
            
            crossfill_pt = random.randint(0, 7)
            
            son1, son2 = perm1[:crossfill_pt], perm2[:crossfill_pt]
            
            pos = crossfill_pt
            while len(son1) != len(perm1):
                if perm2[pos] not in son1:
                    son1.append(perm2[pos])
                pos = (pos + 1) % len(perm2)

            pos = crossfill_pt
            while len(son2) != len(perm2):
                if perm1[pos] not in son2:
                    son2.append(perm1[pos])
                pos = (pos + 1) % len(perm1)

            r = random.uniform(0, 1)
            if r <= 0.9:
                return [Individual(self.params['fitness'], son1), Individual(self.params['fitness'], x = son2)]
            else:
                return [p1, p2]
        elif self.params['crossover'] == 'Cyclic':
            perm = [translate_to_perm(p1.x), translate_to_perm(p2.x)]
            inv_perm = perm[0].copy()
            for (id, x) in enumerate(perm[0]):
                inv_perm[x] = id
            mark = [[False for x in perm[0]], [False for x in perm[1]]]
            cur_par = 0
            cur_pos = random.randint(0, len(perm[0]) - 1)
            flag = True
            #print(cur_pos)
            #print(perm)
            while flag:
                mark[cur_par][cur_pos] = True
                if cur_par == 0:
                    nxt_pos = cur_pos
                else:
                    nxt_pos = inv_perm[perm[1][cur_pos]]
                if mark[1 - cur_par][nxt_pos]:
                    flag = False
                else:
                    cur_pos = nxt_pos
                    cur_par = 1 - cur_par
            nxt = perm
            for i in range(len(perm[0])):
                if mark[0][i]:
                    assert mark[1][i]
                    perm[0][i], perm[1][i] = perm[1][i], perm[0][i]
            
            #print(perm)
                    
            r = random.uniform(0, 1)
            if r <= 0.9:
                return [Individual(self.params['fitness'], perm[0]), Individual(self.params['fitness'], x = perm[1])]
            else:
                return [p1, p2]

    # select the fittest individuals
    def survival_selection(self, par_id1, par_id2):
        if self.params['survival_selection'] == 'worst replacement':
            self.population.sort(reverse=True)
            self.population = self.population[:self.params['population_size']]
        elif self.params['survival_selection'] == 'Generation':
            if par_id1 == par_id2:
                self.population[par_id1] = self.population[-1]
            else:
                self.population[par_id1], self.population[par_id2] = self.population[-1], self.population[-2]

    def population_fitness_analysis(self):
        fitness = [x.fitness() for x in self.population]
        # (np.mean(fitness), np.std(fitness), np.min(fitness), np.max(fitness))
        return np.mean(fitness)

    def get_fittest_individual(self):
        self.population.sort(reverse=True)
        return self.population[0]

    def evolve(self, verbose = False):
        #self.print_population()
        params = self.params
        n_generation = 0
        n_iter = 1000
        #ans_mean, ans_std, ans_min, ans_max = [], [], [], []
        #mean, std, min_val, max_val = self.population_fitness_analysis()
        ans_mean = []
        mean = self.population_fitness_analysis()
        ans_mean.append(mean)
        #ans_std.append(std)
        #ans_min.append(min_val)
        #ans_max.append(max_val)        
        number_converged = sum([x.fitness() == self.fitness_max for x in self.population])
        
        #sum([x.fitness() == self.fitness_max for x in self.population]) < self.params['population_size']
        
        cnt = 0
        
        while self.get_fittest_individual().fitness() != self.fitness_max and n_generation < n_iter:
            #self.print_population()
            
            #print(number_converged)
            
            cnt += 1
            #print(cnt)
            
            cur_flag = (self.get_fittest_individual().fitness() != self.fitness_max and n_generation < n_iter)

            n_generation += 1

            # select the 2 fittest individuals 
            parent1, parent2, id1, id2 = self.parent_selection()

            #create children
            offspring_crossover = self.crossover(parent1, parent2)

            #possibly mutate children
            offspring_mutation = [x.mutation(params['mutation']) for x in offspring_crossover]
            
            #add children to the population
            self.population.extend(offspring_mutation)
            
            #self.print_population()

            #select new generation
            self.survival_selection(id1, id2)            

            if cur_flag:
                #mean, std, min_val, max_val = self.population_fitness_analysis()
                mean = self.population_fitness_analysis()
                ans_mean.append(mean)
                #ans_std.append(std)
                #ans_min.append(min_val)
                #ans_max.append(max_val)
                number_converged = np.sum([x.fitness() == self.fitness_max for x in self.population])            

        if verbose:
            #print('----------------')
            print('Generation number {}:\nBest individual has fitness {}.\nWorst individual has fitness {}.\nMean fitness is {}.\nStd is {}.'.format(n_generation, max_val, min_val, mean, std))
            #print('----------------')

        converged = self.get_fittest_individual().fitness() == self.fitness_max
        return {"n_generations" : n_generation, "mean" : ans_mean, "converged" : converged, "number_converged": number_converged}
