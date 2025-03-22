#include <Arduino.h>

// Configurable: cantidad de iteraciones
const int loop_count = 10000000;

// Función con sumas de enteros
void suma_enteros() {
  volatile int acc = 0;
  for (int i = 0; i < 100; i++) {
    acc += i;
  }
}

// Función con sumas de floats
void suma_floats() {
  volatile float acc = 0;
  for (int i = 0; i < 100; i++) {
    acc += i * 0.1f;
  }
}

void setup() {
  Serial.begin(115200);
  delay(1000);  // Esperar que el monitor serial conecte

  // Cambiar la frecuencia del CPU (80, 160, 240 MHz)
  setCpuFrequencyMhz(160);  // Cambiá este valor para probar
  delay(100);

  Serial.printf("Frecuencia actual del CPU: %d MHz\n", getCpuFrequencyMhz());

  unsigned long start = millis();

  for (int i = 0; i < loop_count; i++) {
    suma_enteros();
    suma_floats();
  }

  unsigned long end = millis();
  float total_seconds = (end - start) / 1000.0;

  Serial.printf("Tiempo total de ejecución: %.3f segundos\n", total_seconds);
}

void loop() {
  // No se repite nada
}
