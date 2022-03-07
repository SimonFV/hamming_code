import tkinter as tk
from tkinter import messagebox
from tkinter import BOTH
import hamming
import convertidor


class App:
    def __init__(self, master):
        # Configuración de la ventana
        master.title("Hamming Code App")
        master.geometry("1240x800")
        master.configure(bg="gray25")
        master.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Scroll
        self.canvasScroll = tk.Canvas(master, bg="gray25")
        self.canvasScroll.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.scrollBar = tk.Scrollbar(master, command=self.canvasScroll.yview)
        self.scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvasScroll.config(yscrollcommand=self.scrollBar.set)

        # Frames para dividir la interfaz en secciones

        self.mainFrame = tk.Frame(self.canvasScroll, bg="gray25")

        self.basesFrame = tk.Frame(self.mainFrame, bg="gray15")
        self.basesFrame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        self.signalFrame = tk.Frame(self.mainFrame, bg="gray15")
        self.signalFrame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        self.parityFrame = tk.Frame(self.mainFrame, bg="gray15")
        self.parityFrame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        self.errorFrame = tk.Frame(self.mainFrame, bg="gray15")
        self.errorFrame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        self.canvasScroll.create_window((0, 0), window=self.mainFrame, anchor="nw")
        self.mainFrame.bind(
            "<Configure>",
            lambda e: self.canvasScroll.configure(
                scrollregion=self.canvasScroll.bbox("all")
            ),
        )
        self.canvasScroll.bind_all(
            "<MouseWheel>",
            lambda e: self.canvasScroll.yview_scroll(
                int(-1 * (e.delta / 120)), "units"
            ),
        )

        # Labels
        self.label1 = tk.Label(
            self.basesFrame,
            text="Conversión",
            bg="gray15",
            fg="cyan",
            font=("Arial Black", 12),
        ).grid(row=0, column=0, padx=5, sticky=tk.W)

        self.label1 = tk.Label(
            self.basesFrame,
            text="Paridad: ",
            bg="gray15",
            fg="yellow",
            font=("Arial Black", 12),
        ).grid(row=0, column=2, padx=5, sticky=tk.W)

        self.label2 = tk.Label(
            self.signalFrame,
            text="Señal NRZI",
            bg="gray15",
            fg="cyan",
            font=("Arial Black", 12),
        ).grid(row=0, column=0, sticky=tk.W)

        self.label4 = tk.Label(
            self.errorFrame,
            text="Error",
            bg="gray15",
            fg="cyan",
            font=("Arial Black", 12),
        ).grid(row=0, column=0, sticky=tk.W)

        # Entry
        entry = tk.Entry(
            self.basesFrame, bg="gray15", fg="gray70", font=("Arial Black", 12)
        )
        entry.grid(row=0, column=1, sticky=tk.W)

        # Tabla de conversion
        self.update_conversion_table(["-", "-", "-", "-"])

        # Tabla de paridad de hamming
        parity_titles = [
            "Hamming",
            "Dato (sin paridad)",
            "P1",
            "P2",
            "P3",
            "P4",
            "P5",
            "Dato (con paridad)",
        ]

        for m in range(8):
            self.cell = tk.Label(
                self.parityFrame,
                width=15,
                bg="gray15",
                fg="gray90",
                font=("Arial Black", 12, "bold"),
            )
            self.cell.grid(row=m, column=0, sticky=tk.W)
            self.cell.config(text=parity_titles[m])

        p = 1
        d = 1
        for n in range(1, 18):
            self.cell = tk.Label(
                self.parityFrame,
                width=4,
                bg="gray15",
                fg="cyan",
                font=("Arial Black", 12, "bold"),
            )
            self.cell.grid(row=0, column=n)
            if (n != 0) and (n & (n - 1) == 0):
                self.cell.config(text="P" + str(p))
                self.cell.configure(fg="yellow")
                p += 1
            else:
                self.cell.config(text="D" + str(d))
                d += 1

        for i in range(1, 8):
            for j in range(1, 18):
                self.cell = tk.Label(
                    self.parityFrame,
                    width=4,
                    bg="gray15",
                    fg="cyan",
                    font=("Arial Black", 12, "bold"),
                    text="-",
                )
                self.cell.grid(row=i, column=j)
                if (j != 0) and (j & (j - 1) == 0):
                    self.cell.configure(fg="yellow")

        # Funcion del boton update
        def update_button():
            input = entry.get()
            if convertidor.is_hex(input) and len(input) == 3:

                results = convertidor.hex_to_all(input)
                self.update_conversion_table(
                    [input, results[0], results[1], results[2]]
                )
                self.update_parity_table(convertidor.str_to_list(results[0]))
                self.draw_signal(results[0])
            else:
                messagebox.showerror(
                    "Error",
                    "Debe ingresar un número hexadecimal de 3 dígitos \n (De 000 a FFF)",
                )

        self.update = tk.Button(
            self.basesFrame,
            text="PROCESAR",
            bg="gray25",
            fg="cyan",
            font=("Arial Black", 10, "bold"),
            command=update_button,
        )
        self.update.grid(row=0, column=4, padx=10, sticky=tk.W)

        # Opcion de paridad
        self.parityOptions = ["Par", "Impar"]
        self.parityVar = tk.StringVar()
        self.parityVar.set(self.parityOptions[0])
        self.parity = tk.OptionMenu(
            self.basesFrame, self.parityVar, *self.parityOptions,
        )
        self.parity.grid(row=0, column=3, sticky=tk.W)
        self.parity.config(
            bg="gray25", fg="gray90", font=("Arial Black", 10, "bold"),
        )

        # Tabla de ERROR de hamming
        error_titles = [
            "Detección de error",
            "Dato recibido",
            "P1",
            "P2",
            "P3",
            "P4",
            "P5",
        ]

        for m in range(7):
            self.cell = tk.Label(
                self.errorFrame,
                width=15,
                bg="gray15",
                fg="gray90",
                font=("Arial Black", 12, "bold"),
            )
            self.cell.grid(row=m, column=0, sticky=tk.W)
            self.cell.config(text=error_titles[m])
        self.cellParity = tk.Label(
            self.errorFrame,
            width=8,
            bg="gray15",
            fg="gray90",
            font=("Arial Black", 12, "bold"),
            text="Prueba de\nparidad",
        )
        self.cellParity.grid(row=0, column=18)
        self.cellParity2 = tk.Label(
            self.errorFrame,
            width=8,
            bg="gray15",
            fg="gray90",
            font=("Arial Black", 12, "bold"),
            text="Bit de\nparidad",
        )
        self.cellParity2.grid(row=0, column=19)

        p = 1
        d = 1
        for n in range(1, 18):
            self.cell = tk.Label(
                self.errorFrame,
                width=4,
                bg="gray15",
                fg="cyan",
                font=("Arial Black", 12, "bold"),
            )
            self.cell.grid(row=0, column=n)
            if (n != 0) and (n & (n - 1) == 0):
                self.cell.config(text="P" + str(p))
                self.cell.configure(fg="yellow")
                p += 1
            else:
                self.cell.config(text="D" + str(d))
                d += 1

        for i in range(2, 7):
            for j in range(1, 18):
                self.cell = tk.Label(
                    self.errorFrame,
                    width=4,
                    bg="gray15",
                    fg="cyan",
                    font=("Arial Black", 12, "bold"),
                    text="-",
                )
                self.cell.grid(row=i, column=j)
                if (j != 0) and (j & (j - 1) == 0):
                    self.cell.configure(fg="yellow")

        for j in range(1, 18):
            self.cell = tk.Entry(
                self.errorFrame,
                width=4,
                bg="gray15",
                fg="cyan",
                font=("Arial Black", 12, "bold"),
            )
            self.cell.grid(row=1, column=j)
            self.cell.insert(tk.END, "-")
            if (j != 0) and (j & (j - 1) == 0):
                self.cell.configure(fg="yellow")

    # Funcion que dibuja los ejes X y Y de la señal unipolar con un estado previo en bajo
    def draw_signal(self, bin_data):
        # Definicion de canvas
        self.canvas = tk.Canvas(self.signalFrame, width=955, bg="gray15")
        self.canvas.grid(row=1, column=4, sticky=tk.W)

        # Eje X
        self.canvas.create_line(120, 200, 830, 200, fill="gray", width=1.5)
        self.canvas.create_text(
            815, 210, fill="white", font="Times 12 bold", text="Tiempo"
        )

        # Eje Y
        self.canvas.create_line(130, 210, 130, 80, fill="gray", width=1.5)
        self.canvas.create_text(
            127, 65, fill="white", font="Times 12 bold", text="Amplitud"
        )

        # Estado inicial de la señal
        self.canvas.create_line(130, 200, 180, 200, fill="green", width=3.0)
        self.canvas.create_line(180, 210, 180, 130, dash=(4, 2), fill="gray")
        self.canvas.create_text(155, 120, fill="white", font="Times 10 bold", text="0")
        self.x = 180
        self.y = 200

        self.draw_signal_aux(bin_data)

    # Funcion que dibuja el resto de la señal de acuerdo con el dato binario procedente del numero hexadecimal ingresado
    def draw_signal_aux(self, bin_data):
        if bin_data != "":
            # Dato de entrada 0
            if bin_data[0] == "0":
                self.canvas.create_line(
                    self.x, self.y, self.x + 50, self.y, fill="green", width=3.0
                )
                self.x = self.x + 50
                self.canvas.create_line(
                    self.x, 210, self.x, 130, dash=(4, 2), fill="gray"
                )
                self.canvas.create_text(
                    self.x - 25, 120, fill="white", font="Times 10 bold", text="0"
                )

                self.draw_signal_aux(bin_data[1:])

            # Dato de entrada 1 y estado previo en bajo
            elif bin_data[0] == "1" and self.y == 200:
                self.canvas.create_line(
                    self.x, self.y, self.x, self.y - 50, fill="green", width=3.0
                )
                self.y = self.y - 50

                self.canvas.create_line(
                    self.x, self.y, self.x + 50, self.y, fill="green", width=3.0
                )
                self.x = self.x + 50
                self.canvas.create_line(
                    self.x, 210, self.x, 130, dash=(4, 2), fill="gray"
                )
                self.canvas.create_text(
                    self.x - 25, 120, fill="white", font="Times 10 bold", text="1"
                )

                self.draw_signal_aux(bin_data[1:])

            # Dato de entrada 1 y estado previo en alto
            elif bin_data[0] == "1" and self.y == 150:
                self.canvas.create_line(
                    self.x, self.y, self.x, self.y + 50, fill="green", width=3.0
                )
                self.y = self.y + 50

                self.canvas.create_line(
                    self.x, self.y, self.x + 50, self.y, fill="green", width=3.0
                )
                self.x = self.x + 50
                self.canvas.create_line(
                    self.x, 210, self.x, 130, dash=(4, 2), fill="gray"
                )
                self.canvas.create_text(
                    self.x - 25, 120, fill="white", font="Times 10 bold", text="1"
                )

                self.draw_signal_aux(bin_data[1:])

    # Actualiza la tabla de paridad con la lista de 12 bits ingresada
    def update_parity_table(self, data):
        extended_data = hamming.add_places(data)
        matrix = hamming.get_parity_table(extended_data, self.parityVar.get())
        data_with_parity = hamming.final_message(matrix)
        table = []
        table.append(extended_data)
        for row in matrix:
            table.append(row)
        table.append(data_with_parity)

        for i in range(len(table)):
            for j in range(len(table[i])):
                if table[i][j] != -1:
                    self.parityFrame.grid_slaves(i + 1, j + 1)[0].config(
                        text=str(table[i][j])
                    )
                else:
                    self.parityFrame.grid_slaves(i + 1, j + 1)[0].config(text="")
        # master.geometry("1240x800")

    def update_conversion_table(self, data):
        conversion_titles = [
            "Hexadecimal",
            "Binario",
            "Octal",
            "Decimal",
        ]

        for m in range(4):
            self.cell = tk.Label(
                self.basesFrame,
                width=15,
                bg="gray15",
                fg="gray90",
                font=("Arial Black", 12, "bold"),
            )
            self.cell.grid(row=m + 1, column=0, sticky=tk.W)
            self.cell.config(text=conversion_titles[m])

        for i in range(0, 4):
            for j in range(1, 2):
                self.cell = tk.Label(
                    self.basesFrame,
                    width=15,
                    bg="gray15",
                    fg="cyan",
                    font=("Arial Black", 12, "bold"),
                    text=data[i],
                )
                self.cell.grid(row=i + 1, column=j)
                if (j != 0) and (j & (j - 1) == 0):
                    self.cell.configure(fg="yellow")

    def on_closing(self):
        root.destroy()


# Inicializa la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
