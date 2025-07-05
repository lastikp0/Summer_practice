import tkinter as tk

from Visualizer.Components.InputFrames import *
from Visualizer.Components.OutputFrames import *
from Visualizer.Components.Panels import *
from Visualizer.Auxilary.Utils import InitFrameUtils
from Visualizer.Components.DataStorage import *
from Visualizer.Auxilary.Generator import *


class Visualizer:

    def __init__(self, data_storage: DataStorage):
        self.master = tk.Tk()
        self.master.geometry("1175x700")
        self.master.resizable(False, False)

        self.data_storage = data_storage

        self.parameters_frame = ParameterFrame(self.master, "Парметры алгоритма", GeneratorParams)
        self.matrix_frame = MatrixFrame(self.master, "Размеры матриц", GeneratorMatrix)

        self.solutions_frame = SolutionsFrame(self.master, "Решения", self.display_solution)
        self.best_answer_frame = BestAnswerFrame(self.master, "Лучший ответ")
        self.graph_frame = GraphFrame(self.master, "График")
        self.view_answers_frame = ViewAnswerFrame(self.master, "Просмотр решений")

        self.control_panel = ControlPanel(self.master)

    def init_display(self):
        InitFrameUtils.init_display_frame(self.best_answer_frame,
                                          row=0, column=1, columnspan=2, sticky="n", pady=(15, 0), padx=(15, 15))
        InitFrameUtils.init_display_frame(self.graph_frame,
                                          row=2, column=1, sticky="n", padx=(0, 5), pady=(0, 15))
        InitFrameUtils.init_display_frame(self.solutions_frame,
                                          row=2, column=2, sticky="n", padx=(5, 0), pady=(0, 15))
        InitFrameUtils.init_display_frame(self.view_answers_frame,
                                          row=1, column=1, columnspan=2, sticky="n", pady=(15, 15), padx=(15, 15))

    def init_input(self):
        InitFrameUtils.init_input_frame(self.parameters_frame,
                                        row=0, column=0, rowspan=2, pady=(15, 0), padx=(15, 0), sticky="n")
        InitFrameUtils.init_input_frame(self.matrix_frame,
                                        row=2, column=0, sticky="n", pady=(0, 15), padx=(15, 0))

    def init_control_panel(self, solve_command, clear_command, step_fwd_command, step_bwd_command, to_the_end_command):
        self.control_panel.init_contents()
        self.control_panel.init_commands(solve_command,
                                         clear_command,
                                         step_fwd_command,
                                         step_bwd_command,
                                         to_the_end_command)
        self.control_panel.frame.grid(row=3, column=0, columnspan=3, sticky="ew")
        self.master.grid_columnconfigure(2, weight=1)

    def get_algorithm_parameter(self, parameter_key: str):
        return self.parameters_frame.get_parameter(parameter_key)

    def get_matrices_sizes(self):
        return self.matrix_frame.get_all_parameters()

    def display_best_solution(self, solution_ID: int):
        solution = self.data_storage.get_solution_by_ID(solution_ID)
        self.best_answer_frame.display_answer(solution_ID,
                                              self.data_storage.get_matrices(),
                                              solution.chromosome,
                                              solution.cost)

    def clear_best_solution(self):
        self.best_answer_frame.clear_data()

    def display_solution(self, solution_ID: str):
        solution = self.data_storage.get_solution_by_ID(solution_ID)
        self.view_answers_frame.display_answer(solution_ID,
                                               self.data_storage.get_matrices(),
                                               solution.chromosome,
                                               solution.cost)

    def clear_solution(self):
        self.view_answers_frame.clear_data()

    def display_solutions_table(self, solution_IDs: list):
        self.solutions_frame.fill_table(solution_IDs)

    def display_graph(self, x_arr: list, y_arr: list):
        self.graph_frame.draw_graph(x_arr, y_arr)
        
    def display_generation_info(self, generation_number, average_fitness, best_fitness):
        self.graph_frame.display_info(generation_number, average_fitness, best_fitness)

    def disable_input(self):
        self.parameters_frame.disable_input()
        self.matrix_frame.disable_input()

    def enable_input(self):
        self.parameters_frame.enable_input()
        self.matrix_frame.enable_input()

    def clear_input(self):
        self.parameters_frame.clear_data()
        self.matrix_frame.clear_data()

    def clear_output(self):
        self.best_answer_frame.clear_data()
        self.view_answers_frame.clear_data()
        self.graph_frame.clear_data()
        self.solutions_frame.clear_data()
 
    def start_solution(self):
        self.control_panel.start_solution()

    def end_solution(self):
        self.control_panel.block_steps()

    def enable_step_backward(self):
        self.control_panel.enable_step_backward()
        
    def disable_step_backward(self):
        self.control_panel.disable_step_backward()

    def show_warning(self, text):
        tk.messagebox.showwarning(message=text)


class InputFacade:
    def __init__(self, visualizer: Visualizer):
        self.visualizer = visualizer

    def get_algorithm_parameter(self, parameter_key: str):
        return self.visualizer.get_algorithm_parameter(parameter_key)

    def get_matrices_sizes(self):
        return self.visualizer.get_matrices_sizes()

    def disable_input(self):
        self.visualizer.disable_input()

    def enable_input(self):
        self.visualizer.enable_input()

    def start_solution(self):
        self.visualizer.start_solution()

    def end_solution(self):
        self.visualizer.end_solution()

    def enable_step_backward(self):
        self.visualizer.enable_step_backward()

    def disable_step_backward(self):
        self.visualizer.disable_step_backward()

    def clear_input(self):
        self.visualizer.clear_input()


class OutputFacade:
    def __init__(self, visualizer: Visualizer):
        self.visualizer = visualizer

    def display_best_solution(self, solution_ID: int):
        self.visualizer.display_best_solution(solution_ID)

    def clear_viewports(self):
        self.visualizer.clear_best_solution()
        self.visualizer.clear_solution()

    def display_solutions_table(self, solution_IDs: list):
        self.visualizer.display_solutions_table(solution_IDs)

    def display_graph(self, x_arr: list, y_arr: list):
        self.visualizer.display_graph(x_arr, y_arr)
        
    def display_generation_info(self, generation_number, average_fitness, best_fitness):
        self.visualizer.display_info(generation_number, average_fitness, best_fitness)

    def clear_output(self):
        self.visualizer.clear_output()

    def show_warning(self, text):
        self.visualizer.show_warning(text)

