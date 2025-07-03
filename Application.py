import random

import backend.GenAlgorithm
from Visualizer.Components.DataStorage import *
from Visualizer.Visualizer import Visualizer, InputFacade, OutputFacade
from backend.GenAlgorithm import Solver


class Application:
    def __init__(self):
        self.data_storage = DataStorage()
        self.viz = Visualizer(self.data_storage)
        self.input_f = InputFacade(self.viz)
        self.output_f = OutputFacade(self.viz)
        self.solver = None

    def start(self):
        self.viz.init_input()

        self.viz.init_display()

        self.viz.init_control_panel(self.solve, self.clear, self.step_forward, self.step_backward, self.to_the_end)

        self.viz.master.mainloop()

    def update_population(self):
        population = self.solver.population
        self.data_storage.add_new_population()
        for ind in population:
            self.data_storage.add_solution(Solution(ind, self.solver.evaluate(ind)))

        self.viz.display_solutions_table(range(len(population)))
        #self.viz.display_best_solution(self.solver.get_best_index()))
        self.viz.display_best_solution(list(map(self.solver.evaluate, population)).index(self.solver.get_best()))
        self.viz.display_graph(self.solver.avg_all_gens, self.solver.best_all_gens)

    @staticmethod
    def int_validation(var):
        var = int(var)
        if var <= 0:
            raise ValueError
        return var

    @staticmethod
    def float_validation(var):
        var = float(var)
        if var < 0 or var > 1:
            raise ValueError
        return var

    def solve(self):
        try:
            matrices_sizes = list(map(self.int_validation, self.input_f.get_matrices_sizes()))
        except ValueError:
            self.viz.show_warning("Введены некорректные размеры матриц")
            return
        try:
            population_size = self.int_validation(self.input_f.get_algorithm_parameter("population_size"))
            crossover_prob = self.float_validation(self.input_f.get_algorithm_parameter("crossover_prob"))
            mutation_prob = self.float_validation(self.input_f.get_algorithm_parameter("mutation_prob"))
            max_generations = self.int_validation(self.input_f.get_algorithm_parameter("max_generations"))
        except ValueError:
            self.viz.show_warning("Введены некорректные числовые параметры алгоритма")
            return
        try:
            mutation_type = self.input_f.get_algorithm_parameter("mutation_type")
        except KeyError:
            self.viz.show_warning("Введены некорректные типы мутаций")
            return

        self.input_f.disable_input()
        self.input_f.start_solution()
        self.solver = Solver(max_generations, population_size, crossover_prob, mutation_prob, mutation_type,
                             matrices_sizes)
        self.data_storage.matrices_sizes = matrices_sizes
        self.update_population()

    def clear(self):
        self.input_f.enable_input()
        self.output_f.clear_output()
        self.input_f.clear_input()
        self.data_storage.clear()
        self.input_f.end_solution()

    def to_the_end(self):
        self.solver.solve()
        self.update_population()
        self.input_f.enable_input()

    def step_forward(self):
        if len(self.data_storage.populations) >= 1:
            self.input_f.enable_step_backward()
        self.output_f.clear_viewports()
        solutions_IDs = [x for x in range(len(self.data_storage.get_population()))]
        self.output_f.display_solutions_table(solutions_IDs)

        best_solution_ID = random.randint(0, len(self.data_storage.get_population()) - 1)
        self.output_f.display_best_solution(best_solution_ID)
        self.solver.advance()
        self.update_population()

    def step_backward(self):
        self.input_f.enable_step_backward()
        self.data_storage.pop_population()
        self.solver.set_gen(self.solver.generation_number-1, [x.chromosome for x in self.data_storage.get_population()], self.solver.avg_all_gens[:-1], self.solver.best_all_gens[:-1])

        population = self.solver.population
        self.viz.display_solutions_table(range(len(population)))
        #self.viz.display_best_solution(self.solver.get_best_index()))
        self.viz.display_best_solution(list(map(self.solver.evaluate, population)).index(self.solver.get_best()))
        self.viz.display_graph(self.solver.avg_all_gens, self.solver.best_all_gens)
        if len(self.data_storage.populations) <= 1:
    	    self.input_f.disable_step_backward()


# ✓: Generators for Parameters and Matrix sizes
# ✓: Proper reading from file function
# ✓: Aliases for parameters of Input classes (so that we can pass their names to display and aliases to get)
# ✓: Add Exceptions to Input classes with pop-up warning windows

# ✓: Figure out how to put parentheses...
# ✓: Delete gen button from graph
# ✓: Create an upper level function (at Visualizer probably) that will display chosen a chromosome

# ✓: Create super class for input which will uhm probably collect data and pass it to app. A facade
# ✓: Create super class for output. A facade providing methods for displaying data
# ✓: Update this facades if needed

# ✓: Buttons at control panel must be bound to some app functions controlling the solution

# ✓: Update buttons at control panel behavior according to algorithm's logic if needed

# ✓: Complete DataStorage class

