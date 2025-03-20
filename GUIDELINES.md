# Trabajo Práctico #1 - Rendimiento

El trabajo se divide en **dos partes principales**, con algunas consignas específicas para el informe.

## 🧩 **Parte 1 - Benchmarks de terceros**

### ✅ ¿Qué hay que hacer?
1. Armar una **lista de benchmarks** útiles para cada integrante del grupo.
2. Asociar **tareas diarias** a **benchmarks** que mejor las representen.
3. Evaluar el **rendimiento** de tres CPUs compilando el kernel de Linux:
   - Intel Core i5-13600K
   - AMD Ryzen 9 5900X
   - AMD Ryzen 9 7950X
4. Analizar cuál es más eficiente en **uso de núcleos** y en **términos de costo**.
5. Usar herramientas como [OpenBenchmarking](https://openbenchmarking.org/test/pts/build-linux-kernel-1.15.0) y [Tom's Hardware](https://www.tomshardware.com/reviews/cpu-hierarchy,4312.html)

### 🧠 ¿Cómo hay que hacerlo?
- Hacer una tabla con **nombre del benchmark**, **tarea que representa** y **quién del grupo la hace**.
- Buscar en OpenBenchmarking.org y en reviews de Tom’s Hardware para sacar **tiempos de compilación del kernel** para los tres CPUs.
- Comparar los valores y calcular por ejemplo:
  - Tiempo de compilación (menor es mejor)
  - Precio actual de cada CPU
  - Costo por rendimiento (ej: segundos por dólar)
  - Eficiencia por núcleo

---

## 🧩 **Parte 2 - Código propio y time profiling**

### ✅ ¿Qué hay que hacer?
1. Usar una **placa con frecuencia modificable** (ESP32 o STM32).
2. Escribir un código que **tarde ~10 segundos** en ejecutarse (sumas de enteros y floats).
3. **Cambiar la frecuencia** del procesador y ver cómo impacta en el tiempo de ejecución.
4. **Hacer profiling del tiempo** de funciones y mostrar capturas/conclusiones.

### 🧠 ¿Cómo hay que hacerlo?
- Usar una **STM32F103C8T6** (porque es lo que tenemos).
- Escribir un código que mida el tiempo total de ejecución con SysTick o un timer.
- Medir con dos frecuencias distintas (por ejemplo, 36 MHz y 72 MHz) y comparar el tiempo.
- Hacer el profiling manual o con ayuda de un osciloscopio/timer externo si se quiere más precisión.
- Agregar capturas (terminal, código, medición, etc.) en el informe.

---

## 📝 **Informe final debe incluir**:
- Tabla de benchmarks y tareas
- Comparación de CPUs
- Resultados del tiempo de ejecución al cambiar la frecuencia
- Capturas de pantalla del profiling
- Conclusiones sobre qué pasa al duplicar la frecuencia

---

## 👥 Organización
- El trabajo es **grupal**, hasta 3 personas.
- Cada uno tendrá un **repo individual sincronizado** (a través de un fork de un repo principal).
- En el archivo de resultados se deben incluir los nombres, grupo y las **mediciones personales**.

---
