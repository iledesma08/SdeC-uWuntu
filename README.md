# 🧪 Trabajo Práctico: Performance y Rendimiento de Computadoras

Este trabajo tiene como objetivo poner en práctica los conceptos de **performance** y evaluación de **rendimiento** en computadoras, tanto a nivel de hardware como mediante el análisis de ejecución de código propio.

El trabajo se divide en **dos partes**:

---

## 🧩 Parte 1: Uso de Benchmarks de Terceros

### Objetivos:
- Investigar y seleccionar benchmarks representativos de las tareas que cada integrante del grupo realiza diariamente.
- Comparar el rendimiento de diferentes procesadores compilando el kernel de Linux.
- Analizar la eficiencia en el uso de núcleos y la relación rendimiento/costo.

### Actividades:
- Armar una tabla con tareas diarias y benchmarks que mejor las representen.
- Evaluar y comparar el rendimiento de los siguientes procesadores:
  - Intel Core i5-13600K
  - AMD Ryzen 9 5900X
  - AMD Ryzen 9 7950X (aceleración comparativa)
- Utilizar herramientas como:
  - [OpenBenchmarking.org - Build Linux Kernel Test](https://openbenchmarking.org/test/pts/build-linux-kernel-1.15.0)
  - [Tom’s Hardware CPU Hierarchy](https://www.tomshardware.com/reviews/cpu-hierarchy,4312.html)

---

## ⚙️ Parte 2: Medición de Performance de Código Propio

### Objetivos:
- Ejecutar un código simple en una placa de desarrollo con frecuencia modificable (STM32 o ESP32).
- Medir el tiempo de ejecución de una función que tarde aproximadamente 10 segundos.
- Analizar cómo varía ese tiempo al modificar la frecuencia del procesador.
- Realizar time profiling para evaluar el uso del tiempo por función.

### Actividades:
- Ejecutar código con sumas de enteros y floats.
- Cambiar la frecuencia del microcontrolador y medir los tiempos de ejecución.
- Capturar resultados y reflexionar sobre el impacto de la frecuencia en la performance.
- Mostrar capturas del uso de herramientas de profiling si se aplican.

---

## 📦 Entregables

- Informe con:
  - Tabla de tareas y benchmarks.
  - Resultados comparativos de CPUs.
  - Capturas de profiling.
  - Conclusiones sobre el impacto de la frecuencia.
- Repositorio individual por cada integrante, sincronizado con el grupo.
- Archivo final con:
  - Nombres de los integrantes.
  - Nombre del grupo.
  - Resultados individuales.

---

## 👥 Notas

- El trabajo es grupal, con hasta 3 personas por grupo.
- Se permite un integrante de ingeniería electrónica por grupo.
- Cada integrante debe realizar y registrar sus mediciones individualmente.
