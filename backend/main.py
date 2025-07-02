import random
import bisect

class Solver:
    def __init__(self, max_generations = 150, population_size = 100,
                 p_crossover = 0.9, p_mutation = 0.1, mutation_type = "swap",
                 dimensions = None):
        self.max_generations = max_generations
        self.population_size = population_size

        self.p_crossover = p_crossover
        self.p_mutation = p_mutation
        self.mutation_type = mutation_type

        if dimensions is None:
            self.dimensions = [2, 10, 8, 6, 4]
        else:
            self.dimensions = dimensions.copy()

        self.matrix_number = len(dimensions) - 1

        self.mutations = {"swap": self.mutate_swap,
                          "reverse": self.mutate_reverse,
                          "shuffle": self.mutate_shuffle}
        
        self.generate_population()
        self.fitness_values = list(map(self.evaluate, self.population))

        self.generation_number = 0


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


    def ordered_crossover(self, parent1, parent2):
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

    def mutate_swap(self, individual):
        a, b = random.sample(range(len(individual)), 2)
        individual[a], individual[b] = individual[b], individual[a]

        return individual

    def mutate_reverse(self, individual):
        a, b = sorted(random.sample(range(len(individual)), 2))
        individual[a:b] = individual[a:b][::-1]

        return individual

    def mutate_shuffle(self, individual):
        a, b = sorted(random.sample(range(len(individual)), 2))
        segment = individual[a:b]
        random.shuffle(segment)
        individual[a:b] = segment

        return individual


    def advance(self):
        if self.generation_number < self.max_generations:
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

        return None
    

    def get_avg(self):
        return sum(self.fitness_values) / self.population_size

        
    def get_best(self):
        return min(self.fitness_values)
    

    def solve(self):
        while self.generation_number < self.max_generations:
            self.advance()

        best_index = self.fitness_values.index(self.get_best())

        return self.population[best_index]    

"""
# tmp generator
dims = []
MATRIX_NUMBER = 10

for _ in range(MATRIX_NUMBER + 1):
    a = random.randint(2, 10)
    dims.append(a)
"""

dims = [10, 6, 9, 8, 3, 4, 4, 8, 5, 4, 8]

solver = Solver(dimensions = dims)

res = solver.solve()

print(dims)
print(res, solver.get_best(), solver.get_avg())