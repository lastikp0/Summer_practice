import random
from Visualizer.Components.DataStorage import *
from Visualizer.Visualizer import Visualizer, InputFacade, OutputFacade

def solve():
    input_f.disable_input()
    # algorithm.solve()


def clear():
    input_f.enable_input()
    output_f.clear_output()
    input_f.clear_input()


def to_the_end():
    # algorithm.to_the_end()
    input_f.enable_input()


def step_forward():
    output_f.clear_viewports()
    solutions_IDs = [x for x in range(len(data_storage.solutions))]
    output_f.display_solutions_table(solutions_IDs)

    best_solution_ID = random.randint(0, len(data_storage.solutions) - 1)
    output_f.display_best_solution(best_solution_ID)
    # algorithm.step_forward()


def step_backward():
    pass


def a():
    lst = [x for x in range(1, 11)]
    random.shuffle(lst)
    return Solution(lst, random.randint(100, 500))


data_storage = DataStorage()
data_storage.matrices_sizes = [50, 120, 40, 80, 60, 10, 20, 75, 30, 45, 90, 15]
data_storage.solutions = [a() for i in range(10)]
viz = Visualizer(data_storage)
input_f: InputFacade = InputFacade(viz)
output_f: OutputFacade = OutputFacade(viz)

viz.init_input({"Размер популяции": "population_size",
                "Вероятность скрещивания": "crossover_prob",
                "Вероятность мутации": "mutation_prob",
                "Максимум поколений": "max_generations"},

               {})

viz.init_display()

viz.init_control_panel({"Шаг вперед": step_forward,
                        "Шаг назад": step_backward,
                        "До конца": to_the_end,
                        "Решить": solve,
                        "Сброс": clear})

viz.master.mainloop()


# TODO: Generators for Parameters and Matrix sizes
# TODO: Proper reading from file function
# ✓: Aliases for parameters of Input classes (so that we can pass their names to display and aliases to get)
# TODO: Add Exceptions to Input classes with pop-up warning windows
# TODO: Add a pop-up window asking for the number of sizes for random matrix sizes generation (??)

# TODO: Figure out how to put parentheses...
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
