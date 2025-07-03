class DataStorage:
    def __init__(self):
        self.matrices_sizes = []
        self.solutions = []

    def get_solution_by_ID(self, solution_index):
        return self.solutions[solution_index]

    def get_matrices(self):
        return self.matrices_sizes

    def clear_solutions(self):
        self.solutions = []

    def clear(self):
        self.matrices_sizes = []
        self.solutions = []


class Solution:
    def __init__(self, chromosome, cost):
        self.chromosome = chromosome
        self.cost = cost
