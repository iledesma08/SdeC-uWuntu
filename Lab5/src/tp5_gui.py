import tkinter as tk  # GUI principal con Tkinter
from tkinter import ttk  # Widgets mejorados (botones, layouts)
import matplotlib.pyplot as plt  # Para graficar señales
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
)  # Canvas embebido en GUI
import time  # Tiempos de muestreo
import threading  # Hilo secundario para lectura no bloqueante

# Ruta al archivo del driver (Character Device File)
DEVICE_PATH = "/dev/tp5_driver"


class TP5App:
    def __init__(self, root):
        self.root = root
        self.root.title("TP5 - Señales desde CDD")

        self.running = True  # Bandera para el hilo principal
        self.paused = False  # Bandera para pausar/reanudar graficación

        # Buffers de datos para graficar
        self.signal_data = []  # Valores leídos
        self.time_data = []  # Tiempos relativos
        self.start_time = time.time()  # Tiempo base

        self.active_signal = 1  # Señal activa (1 = cuadrada, 2 = triangular)
        self.update_interval = 0.02  # Intervalo de muestreo: 20 ms

        self.create_widgets()  # Inicializa la GUI

        # Inicia el hilo que lee y actualiza el gráfico
        self.update_thread = threading.Thread(target=self.update_loop, daemon=True)
        self.update_thread.start()

    def create_widgets(self):
        frame = ttk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        # Botón para activar señal 1 (cuadrada)
        self.button1 = ttk.Button(
            frame, text="Señal 1 (cuadrada)", command=lambda: self.change_signal(1)
        )
        self.button1.grid(row=0, column=0, padx=5)

        # Botón para activar señal 2 (triangular)
        self.button2 = ttk.Button(
            frame, text="Señal 2 (triangular)", command=lambda: self.change_signal(2)
        )
        self.button2.grid(row=0, column=1, padx=5)

        # Botón para pausar o reanudar la adquisición de datos
        self.pause_button = ttk.Button(
            frame, text="⏸️ Pausar", command=self.toggle_pause
        )
        self.pause_button.grid(row=0, column=2, padx=5)

        # Preparación del gráfico
        self.fig, self.ax = plt.subplots(figsize=(7, 4))
        self.ax.set_title("Señal sensada")
        self.ax.set_xlabel("Tiempo (s)")
        self.ax.set_ylabel("Valor")
        (self.line,) = self.ax.plot([], [], "b-")  # Línea azul

        # Embebido del gráfico en la ventana Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack()

    # Alterna entre pausar y reanudar la adquisición de datos
    def toggle_pause(self):
        self.paused = not self.paused  # Alterna estado

        if self.paused:
            self.pause_button.config(text="▶️ Reanudar")  # Cambia etiqueta del botón
        else:
            # Reinicia buffers y gráfico al reanudar
            self.signal_data = []
            self.time_data = []
            self.start_time = time.time()

            self.line.set_data([], [])
            self.ax.relim()
            self.ax.autoscale_view()
            self.canvas.draw()

            self.pause_button.config(text="⏸️ Pausar")

    # Cambia la señal activa y reinicia los buffers
    def change_signal(self, num):
        try:
            with open(DEVICE_PATH, "w") as f:
                f.write("1" if num == 1 else "2")  # Escribe "1" o "2" al driver
            self.active_signal = num

            # Reinicia buffers y tiempo
            self.signal_data = []
            self.time_data = []
            self.start_time = time.time()

            print(f"Señal activa: {num}")
        except Exception as e:
            print(f"Error al cambiar de señal: {e}")

    # Lectura del valor actual desde /dev/tp5_driver
    def read_signal(self):
        try:
            with open(DEVICE_PATH, "r") as f:
                value = int(f.read().strip())  # Convierte el texto a entero
            return value
        except Exception as e:
            print(f"Error al leer del driver: {e}")
            return None

    # Loop de actualización en hilo separado
    def update_loop(self):
        next_time = time.time()
        interval = self.update_interval  # 0.02s

        while self.running:
            now = time.time()

            if now >= next_time:
                if not self.paused:
                    value = self.read_signal()
                    if value is not None:
                        t = now - self.start_time
                        self.time_data.append(t)
                        self.signal_data.append(value)

                        # Limita la cantidad de puntos graficados a 20 segundos
                        max_points = int(20 / interval)
                        if len(self.time_data) > max_points:
                            self.time_data = self.time_data[-max_points:]
                            self.signal_data = self.signal_data[-max_points:]

                        # Actualiza gráfico
                        self.line.set_data(self.time_data, self.signal_data)
                        self.ax.relim()
                        self.ax.autoscale_view()
                        self.canvas.draw()

                next_time += interval

            time.sleep(0.005)  # Breve espera para no saturar CPU

    # Detener app
    def stop(self):
        self.running = False
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = TP5App(root)
    root.protocol("WM_DELETE_WINDOW", app.stop)
    root.mainloop()
