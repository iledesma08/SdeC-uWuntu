# 🧠 Trabajo Práctico N°1 - Índice GINI

## 🎯 Objetivo

Diseñar e implementar una interfaz que muestre el índice GINI.

---

## ✅ Requisitos para aprobar el TP#1

### 1. ⚙️ Funcionalidad general

- La aplicación debe recuperar el **índice GINI** desde el Banco Mundial:

[API - Worlbank](https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1&country="Argentina")

- Se recomienda el uso de **API REST** y **Python 🐍** para esta capa superior.

### 2. 🔁 Flujo de datos

- Los datos obtenidos deben ser entregados a un programa en **C 🧩** (capa intermedia).
- El programa en C convocará rutinas escritas en **ensamblador 🛠️** para:
  - Realizar la conversión de valores `float` a `int 🔢`.
  - Devolver el índice GINI de un país (como Argentina 🇦🇷), **sumando uno (+1 ➕)**.

### 3. 🧵 Convenciones

- Se debe utilizar el **stack 📚** para:
  - Convocar rutinas 🔂.
  - Enviar parámetros 📤.
  - Devolver resultados 📥.
- Se deben respetar las **convenciones de llamadas** entre lenguajes de alto y bajo nivel 🧬.

---

## 🔄 Iteraciones del TP

### 🥇 Primera Iteración

- Implementar **todo el TP utilizando únicamente Python y C** (sin ensamblador 🚫🛠️).

### 🥈 Segunda Iteración

- Incorporar las **rutinas en ensamblador 🧩🔧** para completar el trabajo práctico.

---

## 🧰 Tecnologías recomendadas

- **Python 🐍** (para consumo de API y visualización 📊).
- **C 🧩** (capa intermedia).
- **Ensamblador 🛠️** (rutinas de bajo nivel).