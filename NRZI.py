import tkinter as tk
from tkinter import BOTH

class App:

    def __init__(self, master):

        # Configuración de la ventana
        
        master.title("Hamming Code App")
        master.geometry("1024x720")
        master.configure(bg="gray20")
        master.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.canvas = tk.Canvas(master, width=800, height=650, bg="gray20")

        # Eje X y Y
        self.canvas.create_line(150, 300, 860, 300, fill="gray", width=1.5)
        self.canvas.create_text(845, 310, fill="white", font="Times 12 bold", text="Time")
        
        self.canvas.create_line(160, 310, 160, 180, fill="gray", width=1.5)
        self.canvas.create_text(155, 165, fill="white", font="Times 12 bold", text="Amplitude")

        # Estado inicial de la señal
        self.canvas.create_line(160, 300, 210, 300, fill="green", width=3.0)
        self.canvas.create_line(210, 310, 210, 230, dash=(4, 2), fill="gray")
        self.canvas.create_text(185, 220, fill="white", font="Times 10 bold", text="0")
        self.x = 210
        self.y = 300

        self.draw_signal("000110101111") #1AF

    def draw_signal(self, bin_data):
        if bin_data == "":
            print("Drawn signal")
        else:
            if bin_data[0] == "0":
                self.canvas.create_line(self.x, self.y, self.x + 50, self.y, fill="green", width=3.0)
                self.x = self.x + 50
                self.canvas.create_line(self.x, 310, self.x, 230, dash=(4, 2), fill="gray")
                self.canvas.create_text(self.x - 25, 220, fill="white", font="Times 10 bold", text="0")
                
                self.draw_signal(bin_data[1:])

            elif bin_data[0] == "1" and self.y == 300:
                self.canvas.create_line(self.x, self.y, self.x, self.y - 50, fill="green", width=3.0)
                self.y = self.y - 50

                self.canvas.create_line(self.x, self.y, self.x + 50, self.y, fill="green", width=3.0)
                self.x = self.x + 50
                self.canvas.create_line(self.x, 310, self.x, 230, dash=(4, 2), fill="gray")
                self.canvas.create_text(self.x - 25, 220, fill="white", font="Times 10 bold", text="1")

                self.draw_signal(bin_data[1:])

            elif bin_data[0] == "1" and self.y == 250:
                self.canvas.create_line(self.x, self.y, self.x, self.y + 50, fill="green", width=3.0)
                self.y = self.y + 50

                self.canvas.create_line(self.x, self.y, self.x + 50, self.y, fill="green", width=3.0)
                self.x = self.x + 50
                self.canvas.create_line(self.x, 310, self.x, 230, dash=(4, 2), fill="gray")
                self.canvas.create_text(self.x - 25, 220, fill="white", font="Times 10 bold", text="1")

                self.draw_signal(bin_data[1:])

        self.canvas.pack(fill=BOTH, expand=1)

    def on_closing(self):
        root.destroy()
        

# Inicializa la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()