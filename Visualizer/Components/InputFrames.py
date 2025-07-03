from Visualizer.Components.BaseFrames import InputFrame
from Visualizer.Auxilary.Composites import EntryBox, ScrollableFrame, DropdownChoice
from Visualizer.Auxilary.Utils import GUIUtils

PARAMETERS = {"Размер популяции": "population_size",
              "Вероятность скрещивания": "crossover_prob",
              "Вероятность мутации": "mutation_prob",
              "Максимум поколений": "max_generations"}

MUTATION_TYPES = {"обмен":"swap", "обращение":"reverse", "перетасовка":"shuffle"}

SELECTION_TYPES = {"ранжированный":"ranged"}


class ParameterFrame(InputFrame):
    def __init__(self, master, name, generator):
        super().__init__(master, name, generator)
        self.INPUT_BUTTONS = {"Стандартно": self.generate_data,
                              "Из файла": self.read_data,
                              "Очистить": self.clear_data}

    def init_contents(self):
        self.parameters = {param_name: EntryBox(self.contents, label_text) for label_text, param_name in
                           PARAMETERS.items()}

        self.parameters["mutation_type"] = DropdownChoice(self.contents, "Тип мутации", MUTATION_TYPES)
        self.parameters["selection_type"] = DropdownChoice(self.contents, "Тип отбора", SELECTION_TYPES)

        i = 1
        for entrybox in self.parameters.values():
            pady = (10, 0) if i == 1 else 0
            entrybox.label.grid(row=i, column=0, ipadx=5, padx=5, pady=pady, sticky="ew")
            entrybox.box.grid(row=i, column=1, padx=10, pady=pady, sticky="w")
            i += 1


class MatrixFrame(InputFrame):
    def __init__(self, master, name, generator):
        super().__init__(master, name, generator)
        self.scrollable_frame = ScrollableFrame(self.contents, 315, 100)

    def init_contents(self):

        self.parameters = {f"P_{i}": EntryBox(self.scrollable_frame.contents, f"P_{i}") for i in range(4)}

        i = 1
        for entrybox in self.parameters.values():
            pady = (10, 0) if i == 1 else 0
            entrybox.label.grid(row=i, column=0, ipadx=5, padx=5, pady=pady, sticky="ew")
            entrybox.box.grid(row=i, column=1, padx=10, pady=pady, sticky="w")
            i += 1

        self.scrollable_frame.frame.grid(row=0, column=0, columnspan=3, pady=5, sticky="ew")

        bt1 = GUIUtils.make_button(self.contents, "Добавить", self.add_parameter)
        bt1.grid(row=1, column=0, sticky="w", padx=5, pady=(0, 5))
        bt2 = GUIUtils.make_button(self.contents, "Удалить", self.remove_parameter)
        bt2.grid(row=1, column=1, sticky="w", padx=5, pady=(0, 5))
        self.buttons += [bt1, bt2]

    def add_parameter(self):
        num = len(self.parameters)
        entrybox = EntryBox(self.scrollable_frame.contents, f"P_{num}")
        entrybox.label.grid(row=num + 1, column=0, ipadx=5, padx=5, sticky="ew")
        entrybox.box.grid(row=num + 1, column=1, padx=10, pady=0, sticky="w")
        self.parameters[f"P_{num}"] = entrybox

    def remove_parameter(self):
        if len(self.parameters) == 4:
            return
        num = len(self.parameters) - 1
        self.parameters[f"P_{num}"].label.destroy()
        self.parameters[f"P_{num}"].box.destroy()
        self.parameters.pop(f"P_{num}")
