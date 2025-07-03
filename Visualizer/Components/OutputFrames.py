from Visualizer.Components.BaseFrames import DisplayFrame
from Visualizer.Auxilary.Composites import SolutionBox, ScrollableFrame, TabMenu
from Visualizer.Auxilary.Utils import GUIUtils, ConfigUtils


class SolutionsFrame(DisplayFrame):
    def __init__(self, master, name, callback):
        super().__init__(master, name)
        self.table = ScrollableFrame(self.contents, 300, 200)
        self.solutions = {}
        self.display_callback = callback

    def init_contents(self):
        self.table.frame.grid(row=0, column=0, columnspan=3)

    def fill_table(self, solution_IDs):
        self.solutions = {f"chr_{i}": solution_IDs[i] for i in range(len(solution_IDs))}
        keys = [[f"chr_{i}" for i in range(j, len(solution_IDs), 4)] for j in range(4)]
        for i in range(len(keys)):
            for j in range(len(keys[i])):
                cell = GUIUtils.make_label(self.table.contents, keys[i][j])
                cell.grid(row=j, column=i, padx=10)
                cell.bind("<Button-1>", self.use_callback)
                cell.bind("<Enter>", ConfigUtils.hover_on)
                cell.bind("<Leave>", ConfigUtils.hover_off)

    def use_callback(self, event):
        clicked_widget = event.widget
        key = clicked_widget["text"]
        self.display_callback(self.solutions[key])

    def clear_data(self):
        self.table.clear()


class BestAnswerFrame(DisplayFrame):
    def __init__(self, master, name):
        super().__init__(master, name)
        self.solution_box = SolutionBox(self.contents, "")

    def init_contents(self):
        self.solution_box.frame.grid(row=1, column=0)

    def display_answer(self, solution_ID, matrices, chromosome, cost):
        self.solution_box.process_parentheses(matrices, chromosome)
        self.solution_box.write_info(solution_ID, cost)

    def clear_data(self):
        self.solution_box.clear()


class ViewAnswerFrame(DisplayFrame):
    def __init__(self, master, name):
        super().__init__(master, name)
        self.menu = TabMenu(self.contents, ["Окно 1", "Окно 2"], self.change_viewport)
        self.solution_box_1 = SolutionBox(self.contents, "(1) ")
        self.solution_box_2 = SolutionBox(self.contents, "(2) ")
        self.active_viewport = self.solution_box_1

    def init_contents(self):
        self.menu.frame.grid(row=0, columnspan=2, sticky="ew")

        self.solution_box_1.frame.grid(row=1, column=0, columnspan=2)
        self.solution_box_2.frame.grid(row=1, column=0, columnspan=2)
        self.solution_box_2.frame.grid_remove()

        self.contents.grid_columnconfigure(1, weight=1)

    def change_viewport(self, event):
        if self.active_viewport == self.solution_box_1:
            self.solution_box_1.frame.grid_remove()
            self.solution_box_2.frame.grid()
            self.active_viewport = self.solution_box_2
            return
        self.solution_box_2.frame.grid_remove()
        self.solution_box_1.frame.grid()
        self.active_viewport = self.solution_box_1

    def display_answer(self, solution_ID, matrices, chromosome, cost):
        self.active_viewport.process_parentheses(matrices, chromosome)
        self.active_viewport.write_info(solution_ID, cost)

    def clear_data(self):
        self.solution_box_1.clear()
        self.solution_box_2.clear()


class GraphFrame(DisplayFrame):
    def __init__(self, master, name):
        super().__init__(master, name)
        self.graph = GUIUtils.make_graph(self.contents)

    def init_layout(self):
        self.title.grid(row=0, column=0, sticky="ew", columnspan=2)
        self.contents.grid(row=1, column=0)

    def init_contents(self):
        self.graph.get_tk_widget().grid(row=0, column=0)

    def draw_graph(self, y1_arr, y2_arr):
        x_arr = range(1, len(y1_arr)+1)
        self.clear_data()
        axes = self.graph.figure.add_subplot(111)
        axes.plot(x_arr, y1_arr, color='red', linewidth=1, markersize=0, label='Среднее по популяции')
        axes.plot(x_arr, y2_arr, color='green', linewidth=1, markersize=0, label='Минимальное по популяции')
        axes.grid()
        axes.legend()
        self.graph.draw()

    def clear_data(self):
        self.graph.figure.clear()
        self.graph.draw()
