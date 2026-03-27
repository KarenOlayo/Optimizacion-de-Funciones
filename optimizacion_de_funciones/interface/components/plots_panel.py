import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from display.plot_function import plot_function
from display.plot_error import plot_error
from display.plot_approximations import plot_approximations
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class PlotsPanel(tk.Frame):

    def __init__(self, parent):

        super().__init__(parent, bg="#EAF4FF")

        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill='both', expand=True)

        self.func_tab = tk.Frame(self.tabs, bg="white", bd=1, relief="solid")
        self.error_tab = tk.Frame(self.tabs, bg="white", bd=1, relief="solid")
        self.approx_tab = tk.Frame(self.tabs, bg="white", bd=1, relief="solid")
        self.table_tab = tk.Frame(self.tabs, bg="white", bd=1, relief="solid")

        self.tabs.add(self.table_tab, text="Tabla")
        self.tabs.add(self.func_tab, text="Función")
        self.tabs.add(self.error_tab, text="Error")
        self.tabs.add(self.approx_tab, text="Aproximaciones")

        # placeholders iniciales
        self.create_placeholder(self.table_tab, "Tabla resumen")
        self.create_placeholder(self.func_tab, "Gráfica de la función")
        self.create_placeholder(self.error_tab, "Gráfica del error")
        self.create_placeholder(self.approx_tab, "Gráfica de aproximaciones")

   # Placeholder
    def create_placeholder(self, tab, text):
        label = tk.Label(
            tab,
            text=text,
            font=("Cambria Math", 12),
            bg="white",
            fg="gray"
        )
        label.place(relx=0.5, rely=0.5, anchor="center")

  
    def clear_tab(self, tab):
        for widget in tab.winfo_children():
            widget.destroy()

    def draw_figure(self, fig, tab):
 
        container = tk.Frame(tab, bg="white")
        container.pack(fill='both', expand=True)

        canvas = FigureCanvasTkAgg(fig, master=container)
        canvas.draw()
        canvas.get_tk_widget().pack(side='top', fill='both', expand=True)

    def update(self, result, f, a, b, user_points=None):

        if result is None:
            return

        plt.close('all')

        # limpiar tabs
        self.clear_tab(self.func_tab)
        self.clear_tab(self.error_tab)
        self.clear_tab(self.approx_tab)
        self.clear_tab(self.table_tab)

        # Funcion
        try:
            fig1 = plot_function(f, a, b, result, user_points=user_points or {})
            if fig1:
                self.draw_figure(fig1, self.func_tab)
            else:
                self.create_placeholder(self.func_tab, "No se puede graficar (dimensión > 2)")
        except Exception as e:
            self.create_placeholder(self.func_tab, f"Error en gráfica: {e}")

        # Error
        try:
            fig2 = plot_error(result)
            if fig2:
                self.draw_figure(fig2, self.error_tab)
            else:
                self.create_placeholder(self.error_tab, "Sin datos de error")
        except Exception as e:
            self.create_placeholder(self.error_tab, f"Error en gráfica: {e}")

        # Aproximaciones
        try:
            fig3 = plot_approximations(result)
            if fig3:
                self.draw_figure(fig3, self.approx_tab)
            else:
                self.create_placeholder(self.approx_tab, "Sin aproximaciones")
        except Exception as e:
            self.create_placeholder(self.approx_tab, f"Error en gráfica: {e}")

        # Tabla
        if result.table is not None:
            self.show_table(result.table)
        else:
            self.create_placeholder(self.table_tab, "Sin datos de tabla")

    def show_table(self, table):

        frame = ttk.Frame(self.table_tab)
        frame.pack(fill='both', expand=True)

        tree = ttk.Treeview(frame, columns=table.headers, show='headings')

        for h in table.headers:
            tree.heading(h, text=h)
            tree.column(h, width=100)

        for row in table.rows:
            tree.insert('', 'end', values=row)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)

        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
    
    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    def clear_all_tabs(self):

        self.clear_tab(self.func_tab)
        self.clear_tab(self.error_tab)
        self.clear_tab(self.approx_tab)
        self.clear_tab(self.table_tab)

        self.create_placeholder(self.func_tab, "Gráfica de la función")
        self.create_placeholder(self.error_tab, "Gráfica del error")
        self.create_placeholder(self.approx_tab, "Gráfica de aproximaciones")
        self.create_placeholder(self.table_tab, "Tabla resumen")
    
