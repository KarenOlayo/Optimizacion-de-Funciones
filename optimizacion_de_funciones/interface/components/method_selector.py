import tkinter as tk
from tkinter import ttk

class MethodSelector(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#EAF4FF")

        tk.Label(self, text="Método:", font=("Cambria Math", 12), bg="#EAF4FF").pack()

        self.combo = ttk.Combobox(self, values=[
            "Bisección",
            "Falsa posición",
            "Razón dorada",
            "Interpolación cuadrática",
            "Newton",
            "Newton-Raphson",
            "Búsqueda aleatoria",
            "Máxima inclinación",
            "Lagrange"
        ])

        self.combo.pack()
        self.combo.current(0)

    def get_method(self):
        return self.combo.get()