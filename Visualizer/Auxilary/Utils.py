import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ConfigUtils:
    @staticmethod
    def write_into_box(textbox, data):
        textbox.delete("1.0", "end")
        textbox.insert("1.0", data)

    @staticmethod
    def write_into_box_rich(textbox, data):
        textbox.configure(state="normal")
        textbox.delete("1.0", "end")
        colors = ["red", "green", "blue"]
        tags = [f"color_{i}" for i in range(len(colors))]
        for i in range(len(tags)):
            textbox.tag_configure(tags[i], foreground=colors[i])
        stack = []
        j = 0
        for i in range(len(data)):
            if data[i] == "(":
                textbox.insert("end", data[i], f"color_{j % 3}")
                stack.append(j % 3)
                j += 1
            elif data[i] == ")":
                textbox.insert("end", data[i], f"color_{stack.pop()}")
            else:
                textbox.insert("end", data[i])
        textbox.configure(state="disabled")

    @staticmethod
    def hover_on(event, bg="blue", fg="white"):
        hovered_widget = event.widget
        hovered_widget.configure(bg=bg, fg=fg)

    @staticmethod
    def hover_off(event, bg="white", fg="black"):
        hovered_widget = event.widget
        hovered_widget.configure(bg=bg, fg=fg)


class GUIUtils:
    @staticmethod
    def make_label(master, text):
        return tk.Label(master=master, text=text, anchor="w", bg="white")

    @staticmethod
    def make_text(master, width=10, font=("Arial", 12)):
        return tk.Text(master=master, height=1, width=width, font=font, wrap="none")

    @staticmethod
    def make_button(master, text, func):
        return tk.Button(master=master, text=text, command=func)

    @staticmethod
    def make_graph(master):
        figure = Figure(figsize=(4, 2), dpi=100)
        canvas = FigureCanvasTkAgg(figure=figure, master=master)
        return canvas

    @staticmethod
    def make_scrollbar(master, scrollable_object, orientation):
        scrollbar = tk.Scrollbar(master=master, orient=orientation)
        if orientation == "horizontal":
            scrollbar.configure(command=scrollable_object.xview)
            scrollable_object.configure(xscrollcommand=scrollbar.set)
            return scrollbar
        scrollbar.configure(command=scrollable_object.yview)
        scrollable_object.configure(yscrollcommand=scrollbar.set)
        return scrollbar


class InitFrameUtils:
    @staticmethod
    def init_control_panel(self, buttons):
        self.control_panel.init_contents(buttons)
        self.control_panel.frame.grid(row=3, column=0, columnspan=3, sticky="ew")

    @staticmethod
    def init_input_frame(input_frame, parameters, **positioning):
        input_frame.init_layout()
        input_frame.init_contents(parameters)
        input_frame.frame.grid(positioning)

    @staticmethod
    def init_display_frame(display_frame, **positioning):
        display_frame.init_layout()
        display_frame.init_contents()
        display_frame.frame.grid(positioning)


class FileUtils:
    @staticmethod
    def read_from_file(filepath):
        if not filepath:
            return
        file = open(filepath, mode="r")
        info = " ".join([x.strip() for x in file.readlines() if not x.isspace()])
        data = []
        try:
            data = [float(x) for x in info.split(" ")]
        except ValueError:
            print("invalid format")
            pass
        file.close()
        return data
