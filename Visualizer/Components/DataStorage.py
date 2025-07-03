class DataStorage:
    def __init__(self):
        self.matrices_sizes = []
        self.populations = []

    def get_solution_by_ID(self, solution_index):
        return self.populations[-1][solution_index]

    def get_matrices(self):
        return self.matrices_sizes

    def add_new_population(self):
        if len(self.populations) == 3:
            self.populations = self.populations[1:]
        self.populations.append([])

    def add_solution(self, solution):
        self.populations[-1].append(solution)

    def pop_population(self):
        self.populations.pop()

    def get_population(self):
        return self.populations[-1]

    def clear_populations(self):
        self.populations = []

    def clear(self):
        self.matrices_sizes = []
        self.populations = []


class Solution:
    def __init__(self, chromosome, cost):
        self.chromosome = chromosome
        self.cost = cost
