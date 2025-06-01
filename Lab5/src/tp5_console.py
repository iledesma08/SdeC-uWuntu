"""TP5 - Aplicación de consola para lectura de señales desde driver del kernel.

Este módulo implementa una interfaz de consola para interactuar con el driver
tp5_driver del kernel de Linux. Permite seleccionar entre dos señales simuladas
(cuadrada y triangular) y mostrar sus valores en tiempo real.

Author:
    Sistemas de Computación

Date:
    1 de Junio, 2025

Example:
    Ejecutar la aplicación:
        $ python3 tp5_console.py
    
    Uso típico:
        Seleccionar señal [1] cuadrada / [2] triangular / [q] salir: 1
        Leyendo Señal 1 (Ctrl+C para volver al menú)...
        [0.0 s] Valor: 0
        [1.0 s] Valor: 1
"""

import time

# Ruta del dispositivo de carácter del driver en /dev/
DEVICE_PATH = "/dev/tp5_driver"


def seleccionar_senal():
    """Permite al usuario seleccionar qué señal leer del driver.
    
    Presenta un menú interactivo para que el usuario elija entre la señal
    cuadrada (1) o triangular (2), o salir de la aplicación (q).
    Escribe la selección al driver para configurar qué señal leer.
    
    Returns:
        int or None: Número de señal seleccionada (1 o 2), o None para salir.
        
    Note:
        La función maneja automáticamente los errores de escritura al dispositivo
        y solicita una nueva entrada si la selección no es válida.
    """
    while True:
        seleccion = input(
            "Seleccionar señal [1] cuadrada / [2] triangular / [q] salir: "
        ).strip()
        if seleccion in ("1", "2"):
            try:
                with open(DEVICE_PATH, "w") as f:
                    f.write(seleccion)
                return int(seleccion)
            except Exception as e:
                print(f"Error al escribir al driver: {e}")
        elif seleccion.lower() == "q":
            return None
        else:
            print("Entrada no válida.")


def leer_valor():
    """Lee el valor actual de la señal seleccionada desde el driver.
    
    Abre el dispositivo de carácter en modo lectura y obtiene el valor
    actual de la señal que está configurada actualmente en el driver.
    
    Returns:
        int or None: Valor actual de la señal, o None si hay error.
        
    Note:
        Los errores de lectura se muestran por consola pero no detienen
        la ejecución del programa.
    """
    try:
        with open(DEVICE_PATH, "r") as f:
            valor = f.read().strip()
        return int(valor)
    except Exception as e:
        print(f"Error al leer del driver: {e}")
        return None


def main():
    """Función principal que implementa el bucle de la aplicación.
    
    Ejecuta el bucle principal de la aplicación que:
    1. Muestra el menú de selección de señales
    2. Lee y muestra valores de la señal seleccionada cada segundo
    3. Permite volver al menú con Ctrl+C
    4. Permite salir de la aplicación seleccionando 'q'
    
    La aplicación muestra timestamps relativos desde el inicio de la lectura
    de cada señal para facilitar el análisis temporal.
    
    Note:
        La función maneja KeyboardInterrupt para permitir volver al menú
        sin terminar la aplicación completa.
    """
    print("=== TP5 - Lectura de señales desde driver ===")
    while True:
        senal = seleccionar_senal()
        if senal is None:
            print("Saliendo...")
            break

        print(f"Leyendo Señal {senal} (Ctrl+C para volver al menú)...\n")
        tiempo_inicio = time.time()

        try:
            while True:
                valor = leer_valor()
                if valor is not None:
                    tiempo = time.time() - tiempo_inicio
                    print(f"[{tiempo:.1f} s] Valor: {valor}")
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nInterrumpido. Volviendo al menú...\n")


if __name__ == "__main__":
    main()
    