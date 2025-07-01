import tkinter as tk
from Visualizer.Auxilary.Utils import GUIUtils, ConfigUtils


class EntryBox:
    def __init__(self, master, name):
        self.label = GUIUtils.make_label(master, name)
        self.textbox = GUIUtils.make_text(master)

    def read(self):
        return self.textbox.get("1.0", "end")[:-1]

    def write(self, data):
        ConfigUtils.write_into_box(self.textbox, data)

    def clear(self):
        self.textbox.delete("1.0", "end")


class InfoBox:
    def __init__(self, master, caption):
        self.frame = tk.Frame(master, bg="white")
        self.label = GUIUtils.make_label(self.frame, caption)
        self.info_label = GUIUtils.make_label(self.frame, "")

        self.label.grid(row=0, column=0, sticky="w")
        self.info_label.grid(row=0, column=1, sticky="ew")

    def write(self, data):
        self.info_label.configure(text=data)

    def clear(self):
        self.write("")


class ScrollableFrame:
    def __init__(self, master, width, height):
        self.frame = tk.Frame(master)
        canvas = tk.Canvas(self.frame, bg="white", width=width, height=height, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=canvas.yview)
        self.contents = tk.Frame(canvas, bg="white")
        self.contents.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.contents)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.grid(row=0, column=0, columnspan=3, sticky="ew")
        scrollbar.grid(row=0, column=3, sticky="nse")

    def clear(self):
        for child in self.contents.winfo_children():
            child.destroy()


class TabMenu:
    def __init__(self, master, tabs, callback):
        self.frame = tk.Frame(master, bg="white")
        self.tab_buttons = []
        self.selected = None
        i = 0
        for text in tabs:
            tab_button = GUIUtils.make_label(self.frame, text)
            tab_button.grid(row=0, column=i, sticky="w", padx=(0, 25))
            tab_button.bind("<Enter>", lambda e: ConfigUtils.hover_on(e))
            tab_button.bind("<Leave>", lambda e: ConfigUtils.hover_off(e))
            tab_button.bind("<Button-1>", self.select, add="+")
            tab_button.bind("<Button-1>", callback, add="+")
            if i == 0:
                self.change_selection(tab_button)
            i += 1

    def select(self, event):
        new_selected = event.widget
        self.change_selection(new_selected)

    def change_selection(self, new_selected):
        if self.selected:
            self.selected.configure(bg="white", fg="black")
            self.selected.bind("<Leave>", lambda e: ConfigUtils.hover_off(e))
        new_selected.configure(bg="gray")
        new_selected.bind("<Leave>", lambda e: ConfigUtils.hover_off(e, bg="gray"))
        self.selected = new_selected


class SolutionBox:
    class Mtr:
        def __init__(self, string, uid):
            self.size = string
            self.uid = uid

    def __init__(self, master, text):
        self.frame = tk.Frame(master, bg="white")

        self.solution_info = InfoBox(self.frame, f"{text} Решение: ")
        self.cost_info = InfoBox(self.frame, "Стоимость этого решения: ")

        self.textbox = GUIUtils.make_text(self.frame, width=50, font=("Arial", 20))
        self.textbox.configure(state="disabled")
        scrollbar = GUIUtils.make_scrollbar(self.frame, self.textbox, "horizontal")
        self.textbox.grid(row=0, column=0, padx=10, columnspan=4, pady=(10, 0), sticky="ew")
        scrollbar.grid(row=1, column=0, sticky="ew", columnspan=4, padx=10, pady=(0, 15))

        self.solution_info.frame.grid(row=2, column=0, sticky="ew")
        self.cost_info.frame.grid(row=2, column=1, sticky="ew",)

    def write_info(self, solution_id, cost):
        self.solution_info.write(solution_id)
        self.cost_info.write(cost)

    def write_answer(self, answer):
        ConfigUtils.write_into_box_rich(self.textbox, answer)

    def clear(self):
        self.write_info("","")
        self.write_answer("")
        
    def process_parentheses(self, matrices, chromosome):          # HOLY FUCKING SHIT: 40,000 TODO: figure it out

        # Create mutable matrix objects with unique IDs
        pairs = [self.Mtr(f"[{matrices[i - 1]}x{matrices[i]}]", uid=i)
                 for i in range(1, len(matrices))]

        # Create a reference map: object UID -> current object reference
        ref_map = {m.uid: m for m in pairs}

        for i in chromosome:
            # Get current objects using UID map
            a_ref = ref_map[i]
            b_ref = ref_map[i + 1]

            # Create new merged object
            merged_size = f"({a_ref.size}{b_ref.size})"
            new_obj = self.Mtr(merged_size, uid=i)

            # Update reference map for all objects in b_ref's group
            for uid, obj in ref_map.items():
                if obj is b_ref:
                    ref_map[uid] = new_obj

            # Update reference map for all objects in a_ref's group
            for uid, obj in ref_map.items():
                if obj is a_ref:
                    ref_map[uid] = new_obj

            # Update the new object's reference to itself
            ref_map[new_obj.uid] = new_obj

        # Find the final merged object (will be the same for all)
        final_obj = next(iter(ref_map.values()))

        self.write_answer(final_obj.size)
