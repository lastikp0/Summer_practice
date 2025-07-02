import abc
import tkinter as tk
from tkinter import filedialog as fd
from Visualizer.Auxilary.Utils import GUIUtils, FileUtils


class BaseFrame:
    def __init__(self, master, name):
        self.frame = tk.Frame(master, bg="white")
        self.contents = tk.Frame(self.frame, bg="white")
        self.title = tk.Label(self.frame, text=name, font="Tahoma", fg="white", bg="blue")

    @abc.abstractmethod
    def init_layout(self):
        pass

    @abc.abstractmethod
    def init_contents(self):
        pass

    @abc.abstractmethod
    def clear_data(self):
        pass


class InputFrame(BaseFrame):
    def __init__(self, master, name, generator):
        super().__init__(master, name)
        self.buttons = []
        self.parameters = {}
        self.generator = generator
        self.INPUT_BUTTONS = {"Случайно": self.generate_data,
                              "Из файла": self.read_data,
                              "Очистить": self.clear_data}

    def init_layout(self):
        self.title.grid(row=0, column=0, columnspan=4, sticky="ew")
        self.contents.grid(row=1, column=0, columnspan=4, sticky="ew")

        self.buttons = [GUIUtils.make_button(self.frame, text, command) for text, command in self.INPUT_BUTTONS.items()]

        i = 0
        for button in self.buttons:
            button.grid(row=2, column=i, ipadx=5, padx=5, pady=10, sticky="w")
            i += 1

    @abc.abstractmethod
    def init_contents(self):
        pass

    def generate_data(self):
        arr = self.generator.generate(len(self.parameters))
        i = -1

        for entrybox in self.parameters.values():
            i += 1
            entrybox.write(arr[i])

    def read_data(self):
        filepath = fd.askopenfilename()
        data = FileUtils.read_from_file(filepath)
        print(data)  # TODO: set the logic properly...
        if not data:
            return
        i = 0
        for entrybox in self.parameters.values():
            entrybox.write(data[i])
            i += 1  # TODO: we can have more fields than numbers in file... (index error)

    def clear_data(self):
        for entrybox in self.parameters.values():
            entrybox.clear()

    def get_parameter(self, parameter_name):
        try:
            return self.parameters[parameter_name].read()
        except KeyError:
            pass

    def get_all_parameters(self):
        res = []
        for entrybox in self.parameters.values():
            res.append(entrybox.read())
        return res

    def disable_input(self):
        for entrybox in self.parameters.values():
            entrybox.box.configure(state="disabled")
        for button in self.buttons:
            button.configure(state="disabled")

    def enable_input(self):
        for entrybox in self.parameters.values():
            entrybox.box.configure(state="normal")
        for button in self.buttons:
            button.configure(state="normal")


class DisplayFrame(BaseFrame):
    def __init__(self, master, name):
        super().__init__(master, name)

    @abc.abstractmethod
    def init_contents(self):
        pass

    def init_layout(self):
        self.title.grid(row=0, column=0, sticky="ew", columnspan=2)
        self.contents.grid(row=1, column=0)

    @abc.abstractmethod
    def clear_data(self):
        pass
