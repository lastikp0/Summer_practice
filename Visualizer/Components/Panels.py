import tkinter as tk
from Visualizer.Visualizer import GUIUtils


class ControlPanel:
    def __init__(self, master):
        self.frame = tk.Frame(master, bg="gray")
        self.buttons = {}
        self.BUTTONS_NAMES = {"solve_bt": "Решить",
                              "clear_bt": "Сброс",
                              "step_forward_bt": "Шаг вперед",
                              "step_backward_bt": "Шаг назад",
                              "to_the_end_bt": "До конца"}

    def init_contents(self):
        for key, text in self.BUTTONS_NAMES.items():
            self.buttons[key] = GUIUtils.make_button(self.frame, text, None)
        i = 0
        for button in self.buttons.values():
            side = "right" if i > len(self.buttons) - 4 else "left"
            button.pack(side=side, ipadx=5, padx=15, pady=10)
            i += 1
        self.block_steps()

    def init_commands(self, solve_command, clear_command, step_fwd_command, step_bwd_command, to_end_command):
        self.buttons["solve_bt"].configure(command=solve_command)
        self.buttons["clear_bt"].configure(command=clear_command)
        self.buttons["step_forward_bt"].configure(command=step_fwd_command)
        self.buttons["step_backward_bt"].configure(command=step_bwd_command)
        self.buttons["to_the_end_bt"].configure(command=to_end_command)

    def block_steps(self):
        self.buttons["step_forward_bt"].configure(state="disabled")
        self.buttons["step_backward_bt"].configure(state="disabled")
        self.buttons["to_the_end_bt"].configure(state="disabled")

    def start_solution(self):
        self.buttons["step_forward_bt"].configure(state="normal")
        self.buttons["step_backward_bt"].configure(state="normal")
        self.buttons["to_the_end_bt"].configure(state="normal")

    def disable_step_backward(self):
        self.buttons["step_backward_bt"].configure(state="disabled")

    def enable_step_backward(self):
        self.buttons["step_backward_bt"].configure(state="normal")

