"""TP5 - Interfaz gráfica para visualización de señales desde driver del kernel.

Este módulo implementa una aplicación GUI con Tkinter que permite visualizar
en tiempo real las señales simuladas por el driver tp5_driver. Proporciona
una interfaz gráfica para seleccionar entre señal cuadrada y triangular,
pausar/reanudar la adquisición y mostrar los datos en un gráfico dinámico.

Author:
    Sistemas de Computación

Date:
    1 de Junio, 2025

Example:
    Ejecutar la aplicación:
        $ python3 tp5_gui.py
        
    Uso típico:
        - Hacer clic en "Señal 1 (cuadrada)" o "Señal 2 (triangular)"
        - Usar "⏸️ Pausar" / "▶️ Reanudar" para controlar la adquisición
        - El gráfico se actualiza automáticamente cada 20ms
"""

import tkinter as tk  
from tkinter import ttk  
import matplotlib.pyplot as plt  
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
)  
import time  
import threading  
DEVICE_PATH = "/dev/tp5_driver"


class TP5App:
    """Aplicación GUI para visualización de señales desde driver de kernel.
    
    Esta clase implementa una interfaz gráfica completa que permite:
    - Seleccionar entre dos señales simuladas (cuadrada y triangular)
    - Visualizar las señales en tiempo real con gráficos dinámicos
    - Pausar y reanudar la adquisición de datos
    - Controlar el intervalo de muestreo y la ventana de visualización
    
    Attributes:
        root (tk.Tk): Ventana principal de la aplicación.
        running (bool): Bandera para controlar el hilo de actualización.
        paused (bool): Bandera para pausar/reanudar la graficación.
        signal_data (list): Buffer de valores de señal leídos.
        time_data (list): Buffer de timestamps relativos.
        start_time (float): Tiempo de inicio para cálculos relativos.
        active_signal (int): Señal actualmente seleccionada (1 o 2).
        update_interval (float): Intervalo de muestreo en segundos (0.02s = 20ms).
    """
    
    def __init__(self, root):
        """Inicializa la aplicación GUI.
        
        Args:
            root (tk.Tk): Ventana principal de Tkinter.
        """
        self.root = root
        self.root.title("TP5 - Señales desde CDD")

        self.running = True  
        self.paused = False  
        self.signal_data = []  
        self.time_data = []  
        self.start_time = time.time()  

        self.active_signal = 1  
        self.update_interval = 0.02  
        
        self.create_widgets()  

        self.update_thread = threading.Thread(target=self.update_loop, daemon=True)
        self.update_thread.start()

    def create_widgets(self):
        """Crea y configura todos los widgets de la interfaz gráfica.
        
        Configura:
        - Botones para seleccionar señales (cuadrada/triangular)
        - Botón para pausar/reanudar adquisición
        - Gráfico matplotlib embebido en la ventana Tkinter
        - Layout y posicionamiento de elementos
        """
        frame = ttk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        self.button1 = ttk.Button(
            frame, text="Señal 1 (cuadrada)", command=lambda: self.change_signal(1)
        )
        self.button1.grid(row=0, column=0, padx=5)

        self.button2 = ttk.Button(
            frame, text="Señal 2 (triangular)", command=lambda: self.change_signal(2)
        )
        self.button2.grid(row=0, column=1, padx=5)

        self.pause_button = ttk.Button(
            frame, text="⏸️ Pausar", command=self.toggle_pause
        )
        self.pause_button.grid(row=0, column=2, padx=5)

        self.fig, self.ax = plt.subplots(figsize=(7, 4))
        self.ax.set_title("Señal sensada")
        self.ax.set_xlabel("Tiempo (s)")
        self.ax.set_ylabel("Valor")
        (self.line,) = self.ax.plot([], [], "b-")  

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack()

    def toggle_pause(self):
        """Alterna entre pausar y reanudar la adquisición de datos.
        
        Cuando se pausa:
        - Detiene la lectura de nuevos datos del driver
        - Cambia el texto del botón a "▶️ Reanudar"
        
        Cuando se reanuda:
        - Reinicia los buffers de datos
        - Reinicia el tiempo base
        - Limpia el gráfico
        - Cambia el texto del botón a "⏸️ Pausar"
        """
        self.paused = not self.paused  

        if self.paused:
            self.pause_button.config(text="▶️ Reanudar")  
        else:
            self.signal_data = []
            self.time_data = []
            self.start_time = time.time()

            self.line.set_data([], [])
            self.ax.relim()
            self.ax.autoscale_view()
            self.canvas.draw()

            self.pause_button.config(text="⏸️ Pausar")

    def change_signal(self, num):
        """Cambia la señal activa y reinicia los buffers de datos.
        
        Args:
            num (int): Número de señal a seleccionar (1 para cuadrada, 2 para triangular).
            
        Note:
            Escribe al driver para cambiar la señal activa y reinicia todos los
            buffers de datos para comenzar una nueva adquisición limpia.
        """
        try:
            with open(DEVICE_PATH, "w") as f:
                f.write("1" if num == 1 else "2")  
            self.active_signal = num

            self.signal_data = []
            self.time_data = []
            self.start_time = time.time()

            print(f"Señal activa: {num}")
        except Exception as e:
            print(f"Error al cambiar de señal: {e}")

    def read_signal(self):
        """Lee el valor actual de la señal desde el driver del kernel.
        
        Returns:
            int or None: Valor actual de la señal, o None si ocurre un error.
            
        Note:
            Los errores de lectura se imprimen en consola pero no interrumpen
            la ejecución de la aplicación.
        """
        try:
            with open(DEVICE_PATH, "r") as f:
                value = int(f.read().strip())  
            return value
        except Exception as e:
            print(f"Error al leer del driver: {e}")
            return None

    def update_loop(self):
        """Loop principal de actualización ejecutado en hilo separado.
        
        Este método:
        - Lee valores del driver cada 20ms (cuando no está pausado)
        - Actualiza los buffers de datos con timestamps relativos
        - Limita el buffer a 20 segundos de datos para mantener rendimiento
        - Actualiza el gráfico en tiempo real
        - Controla la temporización precisa del muestreo
        
        Note:
            Se ejecuta en un hilo daemon para no bloquear la GUI y permitir
            cierre limpio de la aplicación.
        """
        next_time = time.time()
        interval = self.update_interval 

        while self.running:
            now = time.time()

            if now >= next_time:
                if not self.paused:
                    value = self.read_signal()
                    if value is not None:
                        t = now - self.start_time
                        self.time_data.append(t)
                        self.signal_data.append(value)

                        max_points = int(20 / interval)
                        if len(self.time_data) > max_points:
                            self.time_data = self.time_data[-max_points:]
                            self.signal_data = self.signal_data[-max_points:]

                        self.line.set_data(self.time_data, self.signal_data)
                        self.ax.relim()
                        self.ax.autoscale_view()
                        self.canvas.draw()

                next_time += interval

            time.sleep(0.005)  

    def stop(self):
        """Detiene la aplicación y finaliza todos los hilos.
        
        Este método debe ser llamado antes de cerrar la aplicación para
        asegurar que el hilo de actualización termine correctamente.
        """
        self.running = False
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = TP5App(root)
    root.protocol("WM_DELETE_WINDOW", app.stop)
    root.mainloop()