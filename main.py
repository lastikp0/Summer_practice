import random
from Visualizer.Components.DataStorage import *
from Visualizer.Visualizer import Visualizer, InputFacade, OutputFacade


class Application:
    def __init__(self):
        self.data_storage = DataStorage()
        self.viz = Visualizer(self.data_storage)
        self.input_f = InputFacade(self.viz)
        self.output_f = OutputFacade(self.viz)
        # self.algorithm = GenAlgorithm(data_storage)


    def init_viz(self):
         self.viz.init_input()

         self.viz.init_display()

         self.viz.init_control_panel({"Шаг вперед": self.step_forward,
                                "Шаг назад": self.step_backward,
                                "До конца": self.to_the_end,
                                "Решить": self.solve,
                                "Сброс": self.clear})

         self.viz.master.mainloop()

    def solve(self):
        self.input_f.disable_input()
        matrices_sizes = self.input_f.get_matrices_sizes()
        self.data_storage.matrices_sizes = matrices_sizes
        population_size = self.input_f.get_algorithm_parameter("population_size")
        crossover_prob = self.input_f.get_algorithm_parameter("crossover_prob")
        mutation_prob = self.input_f.get_algorithm_parameter("mutation_prob")
        max_generations = self.input_f.get_algorithm_parameter("max_generations")

        # self.algorithm.solve()


    def clear(self):
        self.input_f.enable_input()
        self.output_f.clear_output()
        self.input_f.clear_input()


    def to_the_end(self):
        # algorithm.to_the_end()
        self.input_f.enable_input()


    def step_forward(self):
        self.output_f.clear_viewports()
        solutions_IDs = [x for x in range(len(self.data_storage.solutions))]
        self.output_f.display_solutions_table(solutions_IDs)

        best_solution_ID = random.randint(0, len(self.data_storage.solutions) - 1)
        self.output_f.display_best_solution(best_solution_ID)
        # self.algorithm.step_forward()


    def step_backward(self):
        pass


def a():
    lst = [x for x in range(1, 11)]
    random.shuffle(lst)
    return Solution(lst, random.randint(100, 500))


app = Application()
app.init_viz()


# ✓: Generators for Parameters and Matrix sizes
# TODO: Proper reading from file function
# ✓: Aliases for parameters of Input classes (so that we can pass their names to display and aliases to get)
# TODO: Add Exceptions to Input classes with pop-up warning windows

# ✓: Figure out how to put parentheses...
# ✓: Delete gen button from graph
# ✓: Create an upper level function (at Visualizer probably) that will display chosen a chromosome

# ✓: Create super class for input which will uhm probably collect data and pass it to app. A facade
# ✓: Create super class for output. A facade providing methods for displaying data
# TODO: Update this facades if needed

# ✓: Buttons at control panel must be bound to some app functions controlling the solution

# TODO: Update buttons at control panel behavior according to algorithm's logic if needed

# TODO: Complete DataStorage class

# Решить button should disable itself and input from Input classes (this will be done in app by facade)
# Сброс button should clear input, output, enable Решить button

# Control buttons call output functions (from facades) to display results of algorithm
# До конца button makes the algorithm work to the end, then display result, enable Решить button and input
# One-step buttons are obvious
