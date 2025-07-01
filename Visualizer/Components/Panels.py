import tkinter as tk
from Visualizer.Visualizer import GUIUtils


class ControlPanel:
    def __init__(self, master):
        self.frame = tk.Frame(master, bg="gray")
        self.buttons = []

    def init_contents(self, buttons):
        self.buttons = [GUIUtils.make_button(self.frame, text, command) for text, command in buttons.items()]
        i = 0
        for button in self.buttons:
            side = "left" if i > len(self.buttons) - 3 else "right"
            button.pack(side=side, ipadx=5, padx=15, pady=10)
            i += 1
