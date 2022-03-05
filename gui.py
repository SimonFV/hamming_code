import tkinter as tk
from tkinter import messagebox
import hamming
import convertidor

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

        self.parityFrame = tk.Frame(master, bg="gray20")
        self.parityFrame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        self.errorFrame = tk.Frame(master, bg="gray15")
        self.errorFrame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        
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

        self.label4 = tk.Label(
            self.errorFrame,
            text="Error:",
            bg="gray15",
            fg="gray70",
            font=("Arial Black", 12),
        ).grid(row=0, column=0, sticky=tk.W)

        #Entry
        entry = tk.Entry(self.basesFrame,
            bg="gray15",
            fg="gray70",
            font=("Arial Black", 12))
        entry.grid(row=0, column=1, sticky=tk.W) 

        # Tabla de conversion

        self.update_conversion_table(["-","-","-","-"])

        # Tabla de paridad de hamming

        parity_titles = [
            "Paridad:",
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
            self.cell.grid(row=m, column=0)
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
            print (len(input))
            if(convertidor.is_hex(input) and len(input)==3):
            
                results = convertidor.hex_to_all(input)
                self.update_conversion_table([input, results[0], results[1],results[2]])
                self.update_parity_table(convertidor.str_to_list(results[0]))
            else:
                messagebox.showerror("Error", "Debe ingresar un número hexadecimal de 3 dígitos \n (De 000 a FFF)")

        self.update = tk.Button(
            self.basesFrame,
            text="update",
            command= update_button
            
        )
        self.update.grid(row=0, column=2, sticky=tk.W)

    # ------------------------------------------------------------
    # Métodos
    # ------------------------------------------------------------
    
    # Actualiza la tabla de paridad con la lista de 12 bits ingresada
    def update_parity_table(self, data):
        extended_data = hamming.add_places(data)
        matrix = hamming.get_parity_table(extended_data)
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
                    self.parityFrame.grid_slaves(i + 1, j + 1)[0].config(text="-")

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
            self.cell.grid(row=m+1, column=0)
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
                self.cell.grid(row=i+1, column=j)
                if (j != 0) and (j & (j - 1) == 0):
                    self.cell.configure(fg="yellow")

    def on_closing(self):
        root.destroy()


# Inicializa la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
