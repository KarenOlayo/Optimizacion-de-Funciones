import tkinter as tk

class ResultsPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#D6EBFF", bd=1, relief="solid")

        self.label = tk.Label(
            self,
            text="Resultados aparecerán aquí",
            font=("Cambria Math", 11),
            bg="#D6EBFF",
            anchor="w",
            justify="left"
        )
        self.label.pack(fill='x', padx=5, pady=2)

    def update(self, result):

        if not result or not result.message:
            self.label.config(text="Sin resultados", fg="black")
            return

        msg = result.get_message_text()
        msg_type = result.get_message_type()

        if msg_type.name == "ERROR":
            color = "red"
        elif msg_type.name == "WARNING":
            color = "orange"
        else:
            color = "green"

        self.label.config(text=msg, fg=color)

    def update_message(self, message):
        self.label.config(text=message)