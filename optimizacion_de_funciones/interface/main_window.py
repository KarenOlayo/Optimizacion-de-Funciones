import tkinter as tk
from tkinter import ttk

from interface.components.results_panel import ResultsPanel
from interface.components.plots_panel import PlotsPanel
from interface.controller import Controller
from interface.utils.parser_nd import parse_function_nd


class MainWindow:

    def __init__(self, root):

        self.root = root
        self.root.title("Optimización de funciones")
        self.root.geometry("1000x700")
        self.root.configure(bg="#EAF4FF")

        self.controller = Controller()
        self.dynamic_entries = {}

        self.functionality_map = {
            "Aproximar raíz": [
                "Bisección",
                "Interpolación Lineal",
                "Método de Newton-Raphson"
            ],
            "Aproximar extremo (mínimo/máximo)": [
                "Razón Dorada",
                "Interpolación Cuadrática",
                "Método de Newton"
            ],
            "Extremo multidimensional": [
                "Búsqueda Aleatoria"
            ]
        }

        self.build_ui()
    
    def clear_all(self):

        # Limpiar funcion y variable
        self.func_entry.delete(0, tk.END)
        self.var_entry.delete(0, tk.END)
        self.var_entry.insert(0, "x")

        # Limpiar combobox
        self.functionality_combo.set("")
        self.method_combo.set("")
        self.method_combo['values'] = []
        
        # Limpiar inputs dinamicos
        for entry in self.dynamic_entries.values():
            entry.delete(0, tk.END)

        # Limpiar frame dinamico 
        for w in self.dynamic_frame.winfo_children():
            w.destroy()

        self.dynamic_entries.clear()

        # Limpiar resultados
        self.results_panel.update_message("")

        # Limpiar la grafica 
        self.plots_panel.clear_all_tabs()

        # eliminar selector de objetivo si existe
        if hasattr(self, "objective_combo"):
            self.objective_combo.destroy()
            del self.objective_combo

    def build_ui(self):

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(4, weight=2)

        # Titulo
        title = tk.Label(
            self.root, text="Optimización de Funciones",
            font=("Segoe UI", 16, "bold"),
            bg="#EAF4FF", fg="#2C3E50"
        )
        title.grid(row=0, column=0, pady=(10, 5))

        # Panel superior
        top_card = tk.Frame(self.root, bg="white", bd=1)
        top_card.grid(row=1, column=0, padx=20, pady=5, sticky="ew")

        container = tk.Frame(top_card, bg="white")
        container.pack(padx=15, pady=10, fill="x")

        # Funcion + variable
        tk.Label(container, text="Variable:", bg="white").grid(row=0, column=0)
        self.var_entry = tk.Entry(container, width=5)
        self.var_entry.insert(0, "x")
        self.var_entry.grid(row=0, column=1)

        tk.Label(container, text="f =", bg="white").grid(row=0, column=2)
        self.func_entry = tk.Entry(container, width=40)
        self.func_entry.grid(row=0, column=3, columnspan=4, sticky="ew")

        # Funcionalidad 
        tk.Label(container, text="Funcionalidad:", bg="white").grid(row=1, column=0)

        self.functionality_combo = ttk.Combobox(
            container,
            values=list(self.functionality_map.keys()),
            state="readonly",
            width=35
        )
        self.functionality_combo.grid(row=1, column=1)

        self.functionality_combo.bind("<<ComboboxSelected>>", self.update_methods)

        # Metodo
        tk.Label(container, text="Método:", bg="white").grid(row=1, column=2)

        self.method_combo = ttk.Combobox(container, values=[], state="readonly", width=25)
        self.method_combo.grid(row=1, column=3)
        self.method_combo.bind("<<ComboboxSelected>>", lambda e: self.build_dynamic_inputs())


        # Frame dinamico
        self.dynamic_frame = tk.Frame(container, bg="white")
        self.dynamic_frame.grid(row=2, column=0, columnspan=6, pady=10)

        # Resultados
        tk.Label(self.root, text="Resumen de Resultados",
                 font=("Segoe UI", 11, "bold"),
                 bg="#EAF4FF").grid(row=2, column=0, sticky="w", padx=20)

        results_card = tk.Frame(self.root, bg="#F8F9FA")
        results_card.grid(row=3, column=0, padx=20, sticky="ew")

        self.results_panel = ResultsPanel(results_card)
        self.results_panel.pack(fill="x", padx=10, pady=5)

        # Graficas
        bottom_card = tk.Frame(self.root, bg="white")
        bottom_card.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")

        bottom_card.rowconfigure(0, weight=1)
        bottom_card.columnconfigure(0, weight=1)

        self.plots_panel = PlotsPanel(bottom_card)
        self.plots_panel.grid(row=0, column=0, sticky="nsew")

    def update_methods(self, event=None):
        func = self.functionality_combo.get()
        self.method_combo['values'] = self.functionality_map.get(func, [])

        # Limpiar inputs cuando cambia la funcionalidad
        for w in self.dynamic_frame.winfo_children():
            w.destroy()
        self.dynamic_entries.clear()

    def add_objective_selector(self):

        tk.Label(self.dynamic_frame, text="Objetivo", bg="white").pack(side="left")

        self.objective_combo = ttk.Combobox(
            self.dynamic_frame,
            values=["Mínimo", "Máximo"],
            state="readonly",
            width=10
        )
        self.objective_combo.pack(side="left", padx=5)
        self.objective_combo.set("Mínimo")

    def build_dynamic_inputs(self):

        for w in self.dynamic_frame.winfo_children():
            w.destroy()

        self.dynamic_entries.clear()

        # eliminar referencia anterior del objective
        if hasattr(self, "objective_combo"):
            del self.objective_combo


        method = self.method_combo.get()


        if not method:
            self.results_panel.update_message("Seleccione un método")
            return

        def add(name):
            tk.Label(self.dynamic_frame, text=name, bg="white").pack(side="left")
            e = tk.Entry(self.dynamic_frame, width=8)
            e.pack(side="left", padx=5)
            self.dynamic_entries[name] = e
        
        # Para aproximar una raiz

        if method in ["Bisección", "Interpolación Lineal"]:
            add("a"); add("b"); add("error")

        elif method == "Método de Newton-Raphson":
            add("x0"); add("error")
        
        # Para aproximar un extremo u optimo

        elif method == "Razón Dorada":
            add("a"); add("b"); add("error")
            self.add_objective_selector()
        
        elif method == "Interpolación Cuadrática":
            add("x0"); add("x1"); add("x2"); add("error")
            self.add_objective_selector()

            
        elif method == "Método de Newton":
            add("x0"); add("error")
            self.add_objective_selector()
        
        # Para aproximar optimos en multivariable

        elif method == "Búsqueda Aleatoria":
            add("lim_inf"); add("lim_sup"); add("iteraciones")
            self.add_objective_selector()

        tk.Button(
            self.dynamic_frame,
            text="Ejecutar",
            command=self.run_method,
            bg="#27AE60",
            fg="white"
        ).pack(side="left", padx=10)

        tk.Button(
            self.dynamic_frame,
            text="Limpiar",
            command=self.clear_all,
            bg="#E74C3C",
            fg="white"
        ).pack(side="left", padx=5)

    def run_method(self):

        f = parse_function_nd(self.func_entry.get(), self.var_entry.get())
        expr = self.func_entry.get()

        if f is None:
            self.results_panel.update_message("Error en la función o variables.")
            return
        
        # Parametros requeridos por método
        required = {
            "Bisección":                ["a", "b", "error"],
            "Interpolación Lineal":     ["a", "b", "error"],
            "Razón Dorada":             ["a", "b", "error"],
            "Interpolación Cuadrática": ["x0", "x1", "x2", "error"],
            "Método de Newton":         ["x0", "error"],
            "Método de Newton-Raphson": ["x0", "error"],
            "Búsqueda Aleatoria":       ["lim_inf", "lim_sup", "iteraciones"],
        }

        method = self.method_combo.get()

        # Verificar que los inputs dinamicos correspondan al metodo actual
        missing = [k for k in required.get(method, []) if k not in self.dynamic_entries]
        if missing:
            self.results_panel.update_message(
                f"Haga clic en 'Seleccionar' antes de ejecutar."
            )
            return        
        
        try:

            params = {}

            for k, v in self.dynamic_entries.items():
                value = v.get()

                if k in ["lim_inf", "lim_sup"]:
                    params[k] = value

                elif k == "iteraciones":
                    params[k] = int(value)
                    if params[k] <= 0:
                        raise ValueError

                else:
                    params[k] = float(value)
                    
            
            if hasattr(self, "objective_combo"):
                params["objective"] = self.objective_combo.get()

        except:
            self.results_panel.update_message("Error en parámetroa")
            return
        

        method = self.method_combo.get()
        var = self.var_entry.get()

        # Validacion de dimension
        if "," in var and method != "Búsqueda Aleatoria":
            self.results_panel.update_message("Este método solo permite una variable.")
            return

        if "," not in var and method == "Búsqueda Aleatoria":
            self.results_panel.update_message("Este método requiere múltiples variables.")
            return

        result = self.controller.execute(method, f, expr=expr, var=var, **params)

        if result is None:
            self.results_panel.update_message("Error al ejecutar")
            return

        self.results_panel.update(result)

        var = self.var_entry.get()

        if "," not in var:
                
            a = params.get("a") or params.get("x0")
            b = params.get("b") or params.get("x2")

            if method in ["Bisección", "Interpolación Lineal", "Razón Dorada"]:
                user_points = {"a": params.get("a"), "b": params.get("b")}

            elif method in ["Método de Newton", "Método de Newton-Raphson"]:
                user_points = {"x0": params.get("x0")}

            elif method == "Interpolación Cuadrática":
                user_points = {
                    "x0": params.get("x0"),
                    "x1": params.get("x1"),
                    "x2": params.get("x2")
                }
            else:
                user_points = {}

            self.plots_panel.update(result, f, a, b, user_points)

        else:
            lim_inf = params.get("lim_inf")
            lim_sup = params.get("lim_sup")
            self.plots_panel.update(result, f, lim_inf, lim_sup)
