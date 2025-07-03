import random
import bisect


class Solver:
    def __init__(self, max_generations, population_size,
                 p_crossover, p_mutation, mutation_type,
                 dimensions):
        self.max_generations = max_generations
        self.population_size = population_size

        self.p_crossover = p_crossover
        self.p_mutation = p_mutation
        self.mutation_type = mutation_type

        self.dimensions = dimensions.copy()

        self.matrix_number = len(dimensions) - 1

        self.mutations = {"swap": self.mutate_swap,
                          "reverse": self.mutate_reverse,
                          "shuffle": self.mutate_shuffle}
        
        self.generate_population()
        self.fitness_values = list(map(self.evaluate, self.population))

        self.generation_number = 0
        self.avg_all_gens = []
        self.best_all_gens = []

    def generate_individual(self, n = None):
        if n is None:
            n = self.matrix_number - 1

        order = [i + 1 for i in range(n)]

        return random.sample(order, n)

    def generate_population(self, n = None, size = None):
        if n is None:
            n = self.matrix_number - 1

        if size is None:
            size = self.population_size

        self.population = [self.generate_individual(n) for _ in range(size)]

        return None

    def evaluate(self, order):
        groups = [(i, i) for i in range(self.matrix_number)]
        total_cost = 0

        for op in order:
            for i in range(len(groups) - 1):
                left = groups[i]
                right = groups[i + 1]

                if left[1] == op - 1 and right[0] == op:

                    cost = self.dimensions[left[0]] * self.dimensions[op] * self.dimensions[right[1] + 1]
                    total_cost += cost

                    new_group = (left[0], right[1])
                    groups = groups[:i] + [new_group] + groups[i + 2:]

                    break

        return total_cost

    def ranked_selection(self, size = None):
        if size is None:
            size = self.population_size

        offspring = []

        sorted_population = sorted(list(zip(self.population, self.fitness_values)), key = lambda ind: ind[1], reverse = True)

        ranks = [i + 1 for i in range(len(sorted_population))]
        ranks_sum = sum(ranks)

        cumulative_probabilities = []
        cumulative = 0
        for r in ranks:
            cumulative += r / ranks_sum
            cumulative_probabilities.append(cumulative)

        for _ in range(size):
            pick = random.random()

            idx = bisect.bisect_left(cumulative_probabilities, pick)

            offspring.append(sorted_population[idx][0][:])

        return offspring

    @staticmethod
    def ordered_crossover(parent1, parent2):
        def fill_child(child, parent, a, b):
            size = len(child)
            parent_ptr = 0

            parent_elements = set(child[a:b])

            for child_ptr in range(a):
                while parent[parent_ptr] in parent_elements:
                    parent_ptr += 1

                child[child_ptr] = parent[parent_ptr]
                parent_ptr += 1

            for child_ptr in range(b, size):
                while parent[parent_ptr] in parent_elements:
                    parent_ptr += 1

                child[child_ptr] = parent[parent_ptr]
                parent_ptr += 1
            
            return None

        size = len(parent1)    
        a, b = sorted(random.sample(range(size), 2))

        child1 = [None for _ in range(size)]
        child2 = [None for _ in range(size)]

        child1[a:b] = parent1[a:b]
        child2[a:b] = parent2[a:b]

        fill_child(child1, parent2, a, b)
        fill_child(child2, parent1, a, b)

        parent1[:] = child2
        parent2[:] = child1

        return None

    @staticmethod
    def mutate_swap(individual):
        a, b = random.sample(range(len(individual)), 2)
        individual[a], individual[b] = individual[b], individual[a]

        return individual

    @staticmethod
    def mutate_reverse(individual):
        a, b = sorted(random.sample(range(len(individual)), 2))
        individual[a:b] = individual[a:b][::-1]

        return individual

    @staticmethod
    def mutate_shuffle(individual):
        a, b = sorted(random.sample(range(len(individual)), 2))
        segment = individual[a:b]
        random.shuffle(segment)
        individual[a:b] = segment

        return individual

    def set_gen(self, gen_number, population, avg_all_gens, best_all_gens):
        self.generation_number = gen_number

        self.population = population.copy()
        self.fitness_values = list(map(self.evaluate, self.population))

        self.avg_all_gens = avg_all_gens.copy()
        self.best_all_gens = best_all_gens.copy()

    def advance(self):
        self.generation_number += 1

        offspring = self.ranked_selection()

        random.shuffle(offspring)

        for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < self.p_crossover:
                self.ordered_crossover(ind1, ind2)

        for ind in offspring:
            if random.random() < self.p_mutation:
                self.mutations[self.mutation_type](ind)

        self.population[:] = offspring
        self.fitness_values = list(map(self.evaluate, self.population))
        self.avg_all_gens.append(self.get_avg())
        self.best_all_gens.append(self.get_best())


    def get_avg(self):
        return sum(self.fitness_values) / self.population_size
        
    def get_best(self):
        return min(self.fitness_values)

    def solve(self):
        while self.generation_number < self.max_generations:
            self.advance()

        best_index = self.fitness_values.index(self.get_best())

        return self.population[best_index]
