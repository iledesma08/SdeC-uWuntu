import time

DEVICE_PATH = "/dev/tp5_driver"


def seleccionar_senal():
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
    try:
        with open(DEVICE_PATH, "r") as f:
            valor = f.read().strip()
        return int(valor)
    except Exception as e:
        print(f"Error al leer del driver: {e}")
        return None


def main():
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
