import tkinter as tk

class InputPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#EAF4FF")

        tk.Label(self, text="f(x):", font=("Cambria Math", 12), bg="#EAF4FF").grid(row=0, column=0)
        self.func_entry = tk.Entry(self, width=40)
        self.func_entry.grid(row=0, column=1)

        tk.Label(self, text="a:", bg="#EAF4FF").grid(row=1, column=0)
        self.a_entry = tk.Entry(self)
        self.a_entry.grid(row=1, column=1)

        tk.Label(self, text="b:", bg="#EAF4FF").grid(row=2, column=0)
        self.b_entry = tk.Entry(self)
        self.b_entry.grid(row=2, column=1)

        tk.Label(self, text="Error:", bg="#EAF4FF").grid(row=3, column=0)
        self.error_entry = tk.Entry(self)
        self.error_entry.grid(row=3, column=1)

    def get_function(self):
        return self.func_entry.get()

    def get_values(self):
        return float(self.a_entry.get()), float(self.b_entry.get()), float(self.error_entry.get())