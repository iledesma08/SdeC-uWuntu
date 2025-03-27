
# UNIVERSIDAD NACIONAL DE CÓRDOBA
# FACULTAD DE CIENCIAS EXACTAS, FÍSICAS Y NATURALES

# SISTEMAS DE COMPUTACIÓN	
## Trabajo Práctico N°1: Rendimiento
### Grupo: uWuntu

| Nombre |
|--------|
| Ledesma, Ignacio |
| Mouton, Alfonso |
| Zuñiga, Ivan |

### Docentes
- Jorge, Javier
- Solinas, Miguel

### Marzo del 2025

---

## Objetivos

El presente trabajo práctico tiene como objetivos:

1. Aplicar conocimientos sobre performance y rendimiento de computadores en situaciones prácticas.

2. Evaluar y seleccionar benchmarks apropiados para diferentes tareas computacionales, con énfasis en aquellos relevantes para nuestras actividades diarias.

3. Analizar el rendimiento de diferentes procesadores (Intel Core i5-13600K, AMD Ryzen 9 5900X y AMD Ryzen 9 7950X) en tareas específicas como la compilación del kernel de Linux. Para esto, sacamos información de esta página: https://openbenchmarking.org/test/pts/build-linux-kernel-1.15.0

4. Medir el rendimiento de nuestro código propio en una ESP32, cambiando la frecuencia de reloj de la misma y viendo como esto modifica el rendimiento. Documentar esto mediante imágenes y sacar conclusiones

5. Desarrollar criterios para la toma de decisiones informadas sobre hardware basadas en datos de benchmarks.

---

# Benchmarks

Un benchmark es una prueba diseñada para evaluar y comparar el rendimiento de sistemas informáticos o sus componentes. Proporciona datos objetivos sobre la eficiencia y velocidad de hardware o software, lo que facilita la toma de decisiones al elegir los dispositivos o programas más adecuados para tareas específicas.

## Lista de benchmarks

Los benchmarks se clasifican según el componente o aspecto del sistema que se desea evaluar. Algunos de los más comunes incluyen:

### Algunos de ellos son:

- **Benchmarks de CPU**:
Miden el rendimiento del procesador, tanto en su capacidad single core como multi core, en términos de velocidad de cálculo y capacidad para manejar múltiples tareas simultáneamente. Ejemplos: Cinebench, Geekbench y PassMark.

- **Benchmarks de GPU**:
Se enfocan en medir la capacidad de procesamiento gráfico de nuestra tarjeta gráfica. Ejemplos: 3DMark, Unigine Heaven y GFXBench.

- **Benchmarks unidades de almacenamiento**:
Evalúan la velocidad de lectura/escritura y el tiempo de acceso de unidades SSD, HDD y NVMe. Ejemplos: AS SSD Benchmark, ATTO Disk Benchmark y CrystalDiskMark.

- **Benchmarks de RAM**::
Evalúan la velocidad de acceso y transferencia de datos de la memoria RAM. Ejemplos: MemTest86, RAMMon y AIDA64.

- **Benchmarks de red**::
Evalúan el rendimiento y velocidad de las conexiones de red, ayudando a diagnosticar problemas de latencia o estabilidad. Ejemplos: comando ping, iPef y traceroute. Páginas como fast.com.

- **Benchmarks de compilación**::
Dentro de esta categoría entran los benchmarks como el de compilación del kernel de Linux, ampliamente reconocido como estándar para evaluar el rendimiento de sistemas en entornos de desarrollo. Este benchmark representa una carga de trabajo real que somete al sistema a exigencias del procesador, memoria, almacenamiento y eficiencia en sí del compilador.

## Benchmark para tareas cotidianas

Los integrantes del grupo hemos concordado que los benchmarks más útiles para nuestro caso son los siguientes:

- **CPU**: Cinebench r24  
Nos pareció un benchmark completo y estandarizado que nos permite saber qué tanto rendimiento nos puede dar nuestro CPU en tareas realistas.

- **GPU**: 3DMark Steel Nomad  
Todos jugamos videojuegos y este benchmark nos da una comparativa frente a otras opciones del mercado de cómo se desempeña nuestra PC en términos de rendimiento gráfico. Nos es útil, también, para encontrar posibles cuellos de botella del CPU.

- **Red**: fast.com  
Internet es algo que usamos a diario y es fundamental poder identificar la velocidad de la misma.

- **Benchmark específico de juegos (Alfonso e Ignacio)**: Red Dead 2  
Es útil para saber cómo se comporta nuestra PC frente a un determinado motor gráfico de forma específica.

- **Benchmark específico para rpcs3 (Ivan)**: Passmark Single Thread Benchmark  
A la hora de emular juegos de PS3 es fundamental tener un rendimiento single core, a diferencia de otras tareas que sustentan esto con el uso de múltiples cores y threads.

---


## 🔍 Análisis del perfil de ejecución con `gprof` (Ivan Zuñiga)

### 📊 Flat profile

| Función     | % Tiempo | Tiempo (s) | Llamadas | Tiempo/llamada | Total/llamada |
|-------------|-----------|------------|----------|----------------|----------------|
| `new_func1` | 88.54%    | 1.70       | 1        | 1.70           | 1.70           |
| `func1`     | 5.73%     | 0.11       | 1        | 0.11           | 1.81           |
| `func2`     | 5.73%     | 0.11       | 1        | 0.11           | 0.11           |

🔎 **Observaciones:**
- `new_func1()` consume **la mayor parte del tiempo** total del programa.
- `func1()` llama a `new_func1()` y, por eso, su *tiempo total por llamada (1.81s)* incluye el tiempo de `new_func1`.
- `main()` tiene una participación mínima en el tiempo total, es ejecutada por un tiempo menor a 0.00 s, debido a esto no aparece en el análisis temporal. 

### 🧭 Call Graph (Árbol de llamadas)

- `main()` → llama a `func1()` y `func2()`
- `func1()` → llama a `new_func1()`

**Distribución de tiempo según el grafo de llamadas:**

| Función      | Tiempo propio (`self`) | Tiempo de hijos (`children`) | Tiempo total |
|--------------|------------------------|-------------------------------|---------------|
| `main()`     | 0.00 s                 | 1.92 s                        | 1.92 s        |
| `func1()`    | 0.11 s                 | 1.70 s                        | 1.81 s        |
| `new_func1()`| 1.70 s                 | 0.00 s                        | 1.70 s        |
| `func2()`    | 0.11 s                 | 0.00 s                        | 0.11 s        |

📌 Esto confirma que:
- **`new_func1()` es el cuello de botella** principal.
- El tiempo total de `main()` coincide con la suma de `func1() + func2()`.
- `func1()` actúa como puente, sin ser costosa por sí sola.
- Como se dijo anteriormente, el tiempo propio de `main()` es menor a 0.00 s.

---

# Medición de Performance de Código Propio 🖥️📊

Con el objetivo de analizar cómo la **frecuencia del procesador** impacta en el **tiempo de ejecución** de un programa, se desarrolló una prueba controlada utilizando una placa **ESP32** 🛠️, la cual permite modificar dinámicamente la frecuencia del núcleo.

## Descripción del Código Implementado 🔧

El código ejecuta una función simple basada en **sumas de números enteros** ➕ o **flotantes** 🔢, dependiendo de lo que se quiera analizar, dentro de un **bucle repetido** una gran cantidad de veces. Esto garantiza un tiempo de ejecución apreciable para observar variaciones significativas.

## Procedimiento del Experimento 🧪

1. Se midió el **tiempo total de ejecución** utilizando `millis()` ⏱️.
2. Se repitió la prueba múltiples veces, configurando el microcontrolador a distintas frecuencias estables:
   - **80 MHz** 🏃
   - **120 MHz** 🚀
   - **240 MHz** ⚡

## Objetivo del Experimento 🎯

El objetivo es observar cómo el **rendimiento** se ve afectado por la **frecuencia del procesador**, identificando si existe una **relación proporcional** entre el incremento de la frecuencia y la disminución del tiempo de ejecución. Además, se pretende determinar qué tipo de relación queda definida en caso de existir.

## Resultados del Experimento 📊

| Frecuencia (MHz) | Suma de Enteros (segundos) | Suma de Flotantes (segundos) |
|------------------|----------------------------|------------------------------|
| 80               | 14.419                     | 17.076                       |
| 160              | 7.099                      | 8.398                        |
| 240              | 4.694                      | 5.551                        |

### Gráfico de Resultados 📉

<image src="Img\tiempoEjecucion.png">
<image src="Img\speedup.png">

---

# Conclusiones

Vemos que al incrementar la frecuencia del microcontrolador, el rendimiento mejora notablemente y, en base al gráfico de speedup podemos notar que al incrementar en tres la frecuencia (desde 80 [MHz]), así disminuyen los tiempos de ejecución en tres, aproximadamente. La suma de flotantes presenta tiempos más altos en comparación con los enteros, lo cual es esperado debido a la complejidad adicional de las operaciones en punto flotante.