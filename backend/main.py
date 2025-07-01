import random

MATRIX_NUMBER = 10

MAX_GENERATIONS = 200
POPULATION_SIZE = 200

P_CROSSOVER = 0.8
P_MUTATION = 0.1
MUTATION_TYPE = "shuffle"

"""
# tmp generator
dimensions = []
left = random.randint(2, 10)
for _ in range(MATRIX_NUMBER):
    right = random.randint(2, 10)

    dimensions.append((left, right))
    left = right
#
"""

dimensions = [(6, 4), (4, 7), (7, 8), (8, 4), (4, 7), (7, 6), (6, 9), (9, 8), (8, 7), (7, 10)]


def generate_individual(n = MATRIX_NUMBER - 1):
    order = [i + 1 for i in range(n)]
    return random.sample(order, n)


def generate_population(n = MATRIX_NUMBER - 1, size = POPULATION_SIZE):
    return [generate_individual(n) for _ in range(size)]


def evaluate(order):
    groups = [(i, i) for i in range(MATRIX_NUMBER)]
    total_cost = 0

    for op in order:
        for i in range(len(groups) - 1):
            left = groups[i]
            right = groups[i + 1]

            if left[1] == op - 1 and right[0] == op:

                cost = dimensions[left[0]][0] * dimensions[left[1]][1] * dimensions[right[1]][1]
                total_cost += cost

                new_group = (left[0], right[1])
                groups = groups[:i] + [new_group] + groups[i + 2:]

                break

    return total_cost


def roulette_selection(population, fitness_values, size = POPULATION_SIZE):
    offspring = []

    max_fitness = max(fitness_values) + 1e-6
    inverse_fitness_values = [(max_fitness - fitness) for fitness in fitness_values]
    inverse_fitness_sum = sum(inverse_fitness_values)

    cumulative_probabilities = []
    cumulative = 0
    for fitness in inverse_fitness_values:
        cumulative += fitness / inverse_fitness_sum
        cumulative_probabilities.append(cumulative)
    
    for s in range(size):
        pick = random.random()

        new_size = s

        # can be rewriten with bisection
        for i, prob in enumerate(cumulative_probabilities):
            if pick <= prob:
                offspring.append(population[i][:])
                new_size = s + 1
                break

        if new_size == s:
            offspring.append(population[-1][:])
    
    """
    part = 1 / size

    pick = random.random()
    flag = True

    picks = []
    for i in range(size):
        new_pick = pick + part * i

        if new_pick > 1:
            new_pick -= 1
        
        picks.append(new_pick)

    for pick in picks:
        for i, prob in enumerate(cumulative_probabilities):
            if pick <= prob:
                offspring.append(population[i][:])

                flag = False
                break
    
        if flag:
            offspring.append(population[-1][:])
    """

    return offspring


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


def mutate_swap(individual):
    a, b = random.sample(range(len(individual)), 2)
    individual[a], individual[b] = individual[b], individual[a]
    return individual

def mutate_reverse(individual):
    a, b = sorted(random.sample(range(len(individual)), 2))
    individual[a:b] = individual[a:b][::-1]
    return individual

def mutate_shuffle(individual):
    a, b = sorted(random.sample(range(len(individual)), 2))
    segment = individual[a:b]
    random.shuffle(segment)
    individual[a:b] = segment
    return individual

# START

mutations = {"swap": mutate_swap,
             "reverse": mutate_reverse,
             "shuffle": mutate_shuffle}

population = generate_population()
fitness_values = list(map(evaluate, population))

generation_number = 0

while generation_number < MAX_GENERATIONS:
    generation_number += 1

    offspring = roulette_selection(population, fitness_values)

    random.shuffle(offspring)

    for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < P_CROSSOVER:
            ordered_crossover(ind1, ind2)
    
    for ind in offspring:
        if random.random() < P_MUTATION:
            mutations[MUTATION_TYPE](ind)
    
    population[:] = offspring
    fitness_values = list(map(evaluate, population))

best_index = fitness_values.index(min(fitness_values))
print(population[best_index], fitness_values[best_index])
