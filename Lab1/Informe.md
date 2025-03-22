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

![](Img\tiempoEjecucion.png)

![](Img\speedup.png)

# Conclusiones

Vemos que al incrementar la frecuencia del microcontrolador, el rendimiento mejora notablemente y, en base al gráfico de speedup podemos notar que al incrementar en tres la frecuencia (desde 80 [MHz]), así disminuyen los tiempos de ejecución en tres, aproximadamente. La suma de flotantes presenta tiempos más altos en comparación con los enteros, lo cual es esperado debido a la complejidad adicional de las operaciones en punto flotante.