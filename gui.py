import tkinter as tk


class App:
    def __init__(self, master):

        # Configuración de la ventana

        master.title("Hamming Code App")
        master.geometry("1024x720")
        master.configure(bg="gray20")
        master.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Frames para dividir la interfaz en secciones

        self.basesFrame = tk.Frame(master, bg="gray15")
        self.basesFrame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        self.signalFrame = tk.Frame(master, bg="gray15")
        self.signalFrame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        self.tablesFrame = tk.Frame(master, bg="gray15")
        self.tablesFrame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Labels

        self.label1 = tk.Label(
            self.basesFrame,
            text="Bases:",
            bg="gray15",
            fg="gray70",
            font=("Arial Black", 12),
        ).grid(row=0, column=0, sticky=tk.W)

        self.label2 = tk.Label(
            self.signalFrame,
            text="NRZI:",
            bg="gray15",
            fg="gray70",
            font=("Arial Black", 12),
        ).grid(row=0, column=0, sticky=tk.W)

        self.label3 = tk.Label(
            self.tablesFrame,
            text="Hamming:",
            bg="gray15",
            fg="gray70",
            font=("Arial Black", 12),
        ).grid(row=0, column=0, sticky=tk.W)

    # ------------------------------------------------------------
    # Métodos
    # ------------------------------------------------------------

    def on_closing(self):
        root.destroy()


# Inicializa la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
