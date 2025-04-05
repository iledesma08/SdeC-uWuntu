# 🧠 **Trabajo Práctico N°2 - Índice GINI**

## 📄 **Enunciado**

Este Trabajo Práctico #2 propone construir una **calculadora de índices GINI**, integrando componentes escritos en **Python, C y Assembler**, siguiendo una arquitectura de capas.

## 🎯 **Objetivo**

Diseñar una **interfaz que muestre el índice GINI** de un país determinado (por ejemplo, Argentina), accediendo a datos reales del **Banco Mundial** a través de una **API REST**.

## 🧱 **Estructura por capas**

### 🐍 **Capa alta (Python)**  

- Se conecta a la **API del Banco Mundial** para obtener los índices GINI.
- Se recomienda usar **`requests`** para acceder a la API.
- Formato de respuesta: **JSON**.

> Ejemplo de URL:  
> ```
> https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1&country="Argentina"
> ```

### 💻 **Capa media (C)**  

- Recibe los datos desde Python.
- Se encarga de **interactuar con rutinas en ensamblador** para ciertos cálculos.
- También puede ser la capa encargada de mostrar resultados.

### ⚙️ **Capa baja (Assembler)**  

- Realiza una **conversión de float a int**, y luego **devuelve el índice GINI + 1**.
- Utiliza convenciones de llamadas y manejo explícito del stack.

## ✅ **Requisitos para aprobar el TP#2**

- Implementar **todas las capas**: Python, C y ASM.
- Usar **convenciones de llamada válidas** para pasar datos al assembler (por stack).
- Usar **GDB** para mostrar el estado del stack antes, durante y después de la función.
- **Primera iteración:** se puede hacer sin ASM (solo Python y C).
- **Segunda iteración:** se **debe** incluir ASM y demostrar uso de GDB.
- **Presentación grupal (2 o 3 personas)**.

### 🛠️ **Herramientas obligatorias y sugeridas**

- **Linux** (Ubuntu 22.04 recomendado)
- **Compiladores**: `gcc`, `nasm`
- **Depurador**: `gdb`
- **Editor de texto**: Codium, Sublime, etc.
- **Repositorio GitHub privado**, con:
  - Un miembro principal con mail institucional
  - Forks sincronizados
  - Commits breves y claros
  - Pull Requests entre miembros

### ⭐ **Extras que suman puntos**

- Casos de prueba
- Diagrama de bloques y de secuencia
- Comparación de performance entre C y Python
- Uso de herramientas de **profiling** en C (`gprof`, `valgrind`, etc.)

## 🧰 **Tecnologías recomendadas**

- **Python 🐍** (para consumo de API y visualización 📊).
- **C 🧩** (capa intermedia).
- **Ensamblador 🛠️** (rutinas de bajo nivel).

## 🖥️ **Requisitos del sistema**

### ✅ **Sistema Operativo**

- **Linux (Ubuntu 22.04 64 bits)** probado y recomendado.
- Funciona también en otras distros (como Linux Mint, que estás usando), mientras tengas soporte para paquetes de 32 bits.

### 🧱 **Arquitectura**

- Se trabaja sobre **x86 de 32 bits**, incluso en sistemas de 64 bits.
- Se necesita poder compilar y ejecutar binarios de 32 bits en tu sistema.

### 🛠️ **Compiladores y herramientas base**

Instalar las herramientas con:

```bash
sudo apt install build-essential nasm gcc-multilib g++-multilib
```

Esto incluye:

- `gcc` y `g++` (con soporte multilib de 32 bits)
- `nasm`: ensamblador para x86
- `make`, `ld`, etc.

## 📘 **Lectura previa recomendada**

Antes de la clase presencial, se sugiere:

1. Leer los **capítulos 1 a 4** del libro:
   > "Lenguaje Ensamblador para PC" de **Paul A. Carter**  
   > [http://pacman128.github.io/pcasm](http://pacman128.github.io/pcasm)

2. Compilar, ejecutar y revisar los programas de esos capítulos.
3. Ejecutar y depurar los programas del capítulo 4 usando GDB.

Este libro es un clásico para aprender ASM desde lo básico hasta lo útil.

## 🔁 **Flujo de ejecución sugerido**

1. Python obtiene datos del índice GINI desde la [API de Worldbank](https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1&country="Argentina").
2. Python los pasa a un programa C (capa intermedia).
3. C llama a una rutina en Assembler para:
   - Realizar la conversión de valores `float` a `int 🔢`.
   - Sumar 1
   - Devolver el resultado
4. C o Python muestra el resultado.

### **🧵 Convenciones**

- Se debe utilizar el **stack 📚** para:
  - Convocar rutinas 🔂.
  - Enviar parámetros 📤.
  - Devolver resultados 📥.
- Se deben respetar las **convenciones de llamadas** entre lenguajes de alto y bajo nivel 🧬.

## 🔄 **Iteraciones del TP**

### 🥇 Primera Iteración

- Implementar **todo el TP utilizando únicamente Python y C** (sin ensamblador 🚫🛠️).

### 🥈 Segunda Iteración

- Incorporar las **rutinas en ensamblador 🧩🔧** para completar el trabajo práctico.

### 🔍 Debugging: GDB

- Para poder depurar bien, compilá tus programas de C con `-g` o mejor aún con `-g3`:
```bash
gcc -m32 -g3 main.c -o programa
```

- En ensamblador (NASM), usá:
```bash
nasm -f elf32 -g -F dwarf archivo.asm
```
`-F dwarf` define el formato de debugging.

Podés ver todas las opciones de `nasm` con:
```bash
nasm -h
```

---
