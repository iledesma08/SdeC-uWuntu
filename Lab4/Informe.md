## **Desafío 3**

El principal desafío de este desafío es configurar el entorno de desarrollo necesario para compilar, probar y analizar módulos del kernel en Linux.

### 1. Instalación de herramientas necesarias

#### Comando sugerido (fallido)

```bash
sudo apt-get install build-essential checkinstall kernel-package linux-source
```

Este comando no funcionó correctamente en nuestro entorno, debido a que `kernel-package` no está disponible en los repositorios por defecto para sistemas operativos modernos.

#### Solución utilizada

```bash
sudo apt-get update
sudo apt-get install build-essential linux-headers-$(uname -r) checkinstall git
```

**¿Qué hace cada uno?**

* `sudo apt-get update`: Actualiza el índice de paquetes disponibles. Es un paso fundamental antes de cualquier instalación.
* `build-essential`: Incluye herramientas básicas de compilación (`gcc`, `make`, etc).
* `linux-headers-$(uname -r)`: Instala los encabezados del kernel en ejecución, necesarios para compilar módulos compatibles con él.
* `checkinstall`: Herramienta que permite crear paquetes `.deb` a partir de compilaciones, facilitando la gestión de desinstalación.
* `git`: Sistema de control de versiones, necesario para clonar el repositorio del TP.

**Nota técnica:** Aunque `linux-source` proporciona el código fuente completo del kernel, para compilar módulos **solo se necesitan los headers** (archivos `.h` con las definiciones internas del kernel en uso).

---

### 2. Clonar el repositorio del trabajo práctico

```bash
git clone https://gitlab.com/sistemas-de-computacion-unc/kenel-modules.git
```

Clona el repositorio con los archivos fuente y Makefiles necesarios para compilar y probar el módulo inicial.

---

### 3. Compilar e Insertar el módulo en el kernel

```bash
cd part1/module
make
sudo insmod mimodulo.ko
```

Se ejecuta el `Makefile`, generando un archivo `.ko` (Kernel Object), que es el módulo binario compilado compatible con el kernel en uso. Luego, `insmod` carga el módulo en memoria y lo registra en el kernel. Puede generar advertencias si no está firmado (por ejemplo, en sistemas con Secure Boot).

---

### 4. Verificar que el módulo está cargado con `lsmod | grep mod` y Ver mensajes del kernel

```bash
lsmod | grep mod
```

Verifica en la lista de módulos cargados si el nuestro (`mimodulo`) aparece correctamente, indicando que está activo en el sistema. La salida obtenida fue:

```bash
mimodulo               12288  0
```

Esto confirma que el modulo `mimodulo` esta cargado en el kernel y no esta siendo usado por ningun otro modulo (0 dependencias).

```bash
sudo dmesg
```

Permite ver la salida de `printk()`, osea el buffer de mensajes internos del kernel. Esto es muy útil para depurar el comportamiento del módulo. En este caso, se mostro el siguiente mensaje en `dmesg`:

```bash
...
[ 1704.831558] mimodulo: module verification failed: signature and/or required key missing - tainting kernel
[ 1704.835825] Modulo cargado en el kernel.
...
```

Esto indica nuevamente que el módulo fue cargado exitosamente, aunque no está firmado, por lo cual se marca al kernel como "tainted" (modificado por código externo).

---

### 5. Consultar más información del Módulo con `cat/proc/modules | grep mod`

Al ejecutar el comando se obtiene lo siguiente:

```bash
cat/proc/modules | grep mod
mimodulo 12288 0 - Live 0x0000000000000000 (OE)
```

#### **Desglose del resultado**

| Campo                | Significado                                                                       |
| -------------------- | --------------------------------------------------------------------------------- |
| `mimodulo`           | Nombre del módulo cargado.                                                        |
| `12288`              | Tamaño en bytes que ocupa en memoria.                                             |
| `0`                  | Cantidad de veces que está siendo usado (referenciado) por otros módulos.         |
| `-`                  | Información de dependencias (vacío porque no depende de otros módulos).           |
| `Live`               | Estado del módulo (activo en memoria).                                            |
| `0x0000000000000000` | Dirección de carga (virtual) del módulo en memoria del kernel.                    |
| `(OE)`               | **Indicador de "taint"** del kernel:                                              |
|                      | - `O` = módulo no está bajo licencia GPL.                                         |
|                      | - `E` = módulo no tiene firma digital aceptada (útil si Secure Boot está activo). |

#### ¿Cuál conviene usar?

* **Para verificar si está cargado** → `lsmod | grep mimodulo`
* **Para análisis técnico o informes** → `cat /proc/modules | grep mimodulo`

---

### 6. Diferencias entre `lsmod` y `cat /proc/modules`

| Característica                   | `lsmod`                                 | `cat /proc/modules`                            |
| -------------------------------- | --------------------------------------- | ---------------------------------------------- |
| **Fuente de datos**              | Lee y formatea `/proc/modules`.         | Muestra directamente el contenido sin formato. |
| **Formato**                      | Más legible: solo nombre, tamaño y uso. | Crudo y completo, muestra más campos técnicos. |
| **Salidas típicas**              | Ejemplo: `mimodulo  12288  0`           | Ejemplo: `mimodulo 12288 0 - Live 0x... (OE)`  |
| **Incluye dirección en memoria** | ❌ No                                    | ✅ Sí (campo `Live 0x...`)                      |
| **Muestra el estado**            | ❌ No                                    | ✅ Sí (campo `Live`, `Unloading`, etc.)         |
| **Licencia y firma (taint)**     | ❌ No                                    | ✅ Sí (`(OE)` u otros indicadores)              |
| **Uso más habitual**             | Usuarios finales y verificación rápida. | Diagnóstico detallado y scripting técnico.     |

---

### 7. Inspección Detallada del Módulo con `modinfo`

Para obtener información detallada del módulo compilado, se ejecutó el siguiente comando:

```bash
modinfo mimodulo.ko
filename:       .../kenel-modules/part1/module/mimodulo.ko
author:         Catedra de SdeC
description:    Primer modulo ejemplo
license:        GPL
srcversion:     C6390D617B2101FB1B600A9
depends:        
retpoline:      Y
name:           mimodulo
vermagic:       6.8.0-60-generic SMP preempt mod_unload modversions
```

#### Interpretación de cada campo:

| Campo         | Significado                                                                                                                                                                                                                                                                                      |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `filename`    | Ruta completa del archivo `.ko` generado. Indica dónde fue compilado y guardado el módulo.                                                                                                                                                                                                       |
| `author`      | Autor declarado en el código fuente del módulo (`MODULE_AUTHOR`).                                                                                                                                                                                                                                |
| `description` | Descripción del propósito del módulo (`MODULE_DESCRIPTION`).                                                                                                                                                                                                                                     |
| `license`     | Licencia bajo la cual se distribuye el módulo. En este caso es `GPL`, lo que indica que el módulo es de código abierto compatible con el kernel.                                                                                                                                                 |
| `srcversion`  | Hash generado automáticamente que representa la versión del código fuente.                                                                                                                                                                                                                       |
| `depends`     | Otros módulos del kernel de los que depende este módulo. En este caso no depende de ninguno.                                                                                                                                                                                                     |
| `retpoline`   | Indica que el módulo fue compilado con mitigaciones contra ataques de tipo Spectre (retpoline).                                                                                                                                                                                                  |
| `name`        | Nombre declarado del módulo (`MODULE_NAME`).                                                                                                                                                                                                                                                     |
| `vermagic`    | Cadena que describe la versión del kernel para la cual fue compilado el módulo, incluyendo flags importantes como `SMP` (multi-procesador), `preempt` (preemptive kernel), `mod_unload` (permite descargar el módulo), y `modversions` (usa verificación de versiones para símbolos exportados). |

---

### 8. Remocion del modulo del kernel

```bash
sudo rmmod mimodulo
```

El comando `rmmod` permite remover el modulo del kernel que habia sido previamente insertado. Luego, se utilizo `sudo dmesg` para confirmar su descarga:

```bash
sudo dmesg
...
[ 2941.311357] Modulo descargado del kernel.
...
```

Esto indica que el modulo fue removido exitosamente y ya no reside en la memoria del kernel. Otra forma de verificar la descarga es con:

```bash
lsmod | grep mod
```

En este caso, `mimodulo               12288  0` no es detectado como antes (se confirma que el modulo no esta insertado en el kernel)

---

### 9. Análisis del módulo `des_generic.ko`

#### Intento fallido inicial

Se intentó obtener información del módulo `des_generic` ejecutando:

```bash
modinfo /lib/modules/$(uname -r)/kernel/crypto/des_generic.ko
```

El resultado fue:

```
modinfo: ERROR: Module /lib/modules/6.8.0-60-generic/kernel/crypto/des_generic.ko not found.
```

#### ¿Por qué ocurrió este error?

A pesar de que el archivo `.ko` no estaba presente como tal, el comando:

```bash
grep DES /boot/config-$(uname -r)
```

arrojó:

```
CONFIG_CRYPTO_DES=m
CONFIG_CRYPTO_DES3_EDE_X86_64=m
CONFIG_CRYPTO_LIB_DES=m
```

Esto indica que **el kernel tiene soporte para estos módulos, pero compilados como módulos opcionales (`=m`)**, no integrados (`=y`). Sin embargo, **no aparecían como archivos `.ko` visibles en disco**.

La clave fue notar que, en sistemas modernos como Ubuntu 24.04, **los módulos del kernel se comprimen por defecto usando el formato `.zst` (Zstandard)**. Por lo tanto, no existía `des_generic.ko`, sino:

```bash
/lib/modules/6.8.0-60-generic/kernel/crypto/des_generic.ko.zst
```

#### Solución aplicada

1. Se localizó el archivo comprimido:

   ```bash
   find /lib/modules/$(uname -r) -name '*des*.ko.zst'
   ```

2. Se descomprimió con:

   ```bash
   sudo zstd -d /lib/modules/$(uname -r)/kernel/crypto/des_generic.ko.zst
   ```

3. Finalmente, se pudo ejecutar `modinfo`:

   ```bash
   modinfo /lib/modules/$(uname -r)/kernel/crypto/des_generic.ko
   ```

#### Resultado y análisis

Se obtuvo la siguiente información:

```
/lib/modules/6.8.0-60-generic/kernel/crypto/des_generic.ko.zst: 11825 bytes    
filename:       /lib/modules/6.8.0-60-generic/kernel/crypto/des_generic.ko
alias:          crypto-des3_ede-generic
alias:          des3_ede-generic
alias:          crypto-des3_ede
alias:          des3_ede
alias:          crypto-des-generic
alias:          des-generic
alias:          crypto-des
alias:          des
author:         Dag Arne Osvik <da@osvik.no>
description:    DES & Triple DES EDE Cipher Algorithms
license:        GPL
srcversion:     B56606AD918CF0074D320DB
depends:        libdes
retpoline:      Y
intree:         Y
name:           des_generic
vermagic:       6.8.0-60-generic SMP preempt mod_unload modversions 
sig_id:         PKCS#7
signer:         Build time autogenerated kernel key
sig_key:        6D:97:F7:E0:E3:5E:DD:23:6A:0F:B7:E7:57:F1:51:88:FD:C7:1A:3A
sig_hashalgo:   sha512
signature:      ...
```

| Campo             | Explicación                                                                                                                                                                                                                                      |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **filename**      | Ruta absoluta del archivo del módulo en el sistema. Es el archivo que se carga en el kernel cuando se usa `insmod` o `modprobe`.                                                                                                                 |
| **alias**         | Nombres alternativos bajo los cuales puede ser llamado o cargado el módulo. Por ejemplo, si un programa solicita `crypto-des`, se carga este módulo automáticamente.                                                                             |
| **author**        | Persona o equipo que escribió el módulo, declarada con `MODULE_AUTHOR()` en el código fuente.                                                                                                                                                    |
| **description**   | Breve explicación del propósito del módulo, dada por `MODULE_DESCRIPTION()`.                                                                                                                                                                     |
| **license**       | Licencia del módulo. Si no es compatible con GPL, puede generar un “tainted kernel” al cargarse. Declarada con `MODULE_LICENSE()`.                                                                                                               |
| **srcversion**    | Identificador hash generado automáticamente por el compilador. Se usa internamente para rastrear versiones del código fuente.                                                                                                                    |
| **depends**       | Lista de otros módulos que este necesita para funcionar. En este caso: `libdes`. Si están vacíos, el módulo no depende de otros.                                                                                                                 |
| **retpoline**     | Indica si el módulo fue compilado con mitigaciones contra ataques Spectre v2 (Retpoline). “Y” significa que sí.                                                                                                                                  |
| **intree**        | Si aparece, indica que este módulo es parte del árbol oficial del kernel (no fue añadido externamente).                                                                                                                                          |
| **name**          | Nombre del módulo, definido en su código. Es el identificador formal dentro del kernel.                                                                                                                                                          |
| **vermagic**      | Información crítica que debe coincidir con la configuración del kernel. Incluye:<br>– Versión del kernel<br>– Si soporta SMP (multiprocesador)<br>– Si permite `mod_unload`<br>– Si usa `modversions` para verificar compatibilidad de símbolos. |
| **sig\_id**       | Identificador del tipo de firma digital. Aquí se usa `PKCS#7`.                                                                                                                                                                                   |
| **signer**        | Nombre de la clave utilizada para firmar el módulo. En este caso, una clave generada automáticamente al compilar el kernel.                                                                                                                      |
| **sig\_key**      | Hash de la clave pública usada para firmar.                                                                                                                                                                                                      |
| **sig\_hashalgo** | Algoritmo hash usado para la firma. Aquí es `sha512`.                                                                                                                                                                                            |
| **signature**     | La firma digital en sí, representada en formato hexadecimal. Se verifica al cargar el módulo si el sistema tiene Secure Boot activo.                                                                                                             |

Esta información es crucial para:

* Verificar **compatibilidad con el kernel**.
* Comprobar si el módulo es **oficial o externo**.
* Diagnosticar errores al cargar módulos (`taint`, firmas inválidas, etc.).
* Entender qué **servicios o funcionalidades** está proveyendo el módulo al sistema.

#### Conclusiones técnicas

* El módulo **sí estaba presente**, pero en formato **comprimido `.ko.zst`**.
* `modinfo` no funciona con archivos comprimidos; por eso el error inicial.
* Al descomprimir, se accedió a los metadatos que confirman:

  * **Firma digital PKCS#7** válida (clave generada al compilar el kernel).
  * **Licencia GPL**.
  * **Depende del módulo `libdes`**.
  * **Compatibilidad exacta** con el kernel actual gracias al `vermagic`.
  * **Alias útiles** para que pueda ser cargado automáticamente por nombre genérico (`des`, `des3_ede`, etc).

---

## **Preguntas Adicionales**

### **1. Diferencias entre los dos módulos analizados**

Comparar el resultado de `modinfo des_generic.ko` con `modinfo mimodulo.ko` permite identificar diferencias clave entre un **módulo del sistema** y un **módulo desarrollado a mano**.

| Campo                   | `des_generic.ko`                                                   | `mimodulo.ko`                                      | Comentario                                                                                                                                   |
| ----------------------- | ------------------------------------------------------------------ | -------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **Ubicación**           | `/lib/modules/.../kernel/crypto/des_generic.ko`                    | `/home/.../kenel-modules/part1/module/mimodulo.ko` | `des_generic` es parte del sistema. `mimodulo` es un módulo local compilado por el usuario.                                                  |
| **Alias**               | Múltiples (`des`, `crypto-des`, etc.)                              | No tiene alias                                     | El sistema usa alias para auto-carga con `modprobe`.                                                                                         |
| **Author**              | `Dag Arne Osvik <da@osvik.no>`                                     | `Catedra de SdeC`                                  | Uno es un autor individual mantenedor de kernel; el otro es un módulo educativo.                                                             |
| **Description**         | `DES & Triple DES EDE Cipher Algorithms`                           | `Primer modulo ejemplo`                            | `des_generic` tiene funcionalidad criptográfica real.                                                                                        |
| **Depends**             | `libdes`                                                           | *(vacío)*                                          | El primero depende de una biblioteca interna, el segundo no requiere otros módulos.                                                          |
| **srcversion**          | Diferente hash                                                     | Diferente hash                                     | Calculado automáticamente por `modpost` en compilación.                                                                                      |
| **retpoline**           | `Y` (mitigación de Spectre)                                        | `Y`                                                | Ambos se compilaron con mitigación activa.                                                                                                   |
| **intree**              | `Y`                                                                | *(no aparece)*                                     | `des_generic` está **dentro del árbol oficial del kernel**, `mimodulo` es externo.                                                           |
| **vermagic**            | `6.8.0-60-generic SMP preempt mod_unload modversions`              | Igual                                              | Ambos fueron compilados para el mismo kernel, lo que garantiza compatibilidad.                                                               |
| **Firma digital**       | Tiene (`sig_id`, `signer`, `sig_key`, `sig_hashalgo`, `signature`) | No tiene                                           | `des_generic` está firmado por el sistema, necesario para Secure Boot. `mimodulo` no está firmado, por eso "tainta" el kernel al insertarlo. |
| **Tamaño y compresión** | Estaba comprimido como `.ko.zst` antes de descomprimir             | Ya descomprimido                                   | Ubuntu comprime los módulos del sistema para ahorrar espacio.                                                                                |

#### **Conclusiones clave**

* **`des_generic` es un módulo oficial**, firmado y mantenido por el kernel, cargado automáticamente por alias cuando se requieren algoritmos DES/3DES.
* **`mimodulo` es un módulo experimental**, sin firma digital, sin alias, y sin dependencias, útil para aprender cómo funciona la carga de módulos pero no usable en entornos productivos sin modificaciones.

---

### **2. ¿Qué divers/modulos estan cargados en sus propias pc? Comparar y explicar diferencias**

[TODO]

---

### **3. ¿Cuales no están cargados pero están disponibles? Que pasa cuando el driver de un dispositivo no está disponible?**

[TODO]

---

### **4. Correr hwinfo en una pc real con hw real y agregar la url de la información de hw en el reporte**

En este caso, se corrió hw-probe como en la clase práctica en la computadora de uno de los integrantes. [Estos fueron los resultados](https://linux-hardware.org/?probe=ecc2d87800)

---

### **5. ¿Qué diferencia existe entre un módulo y un programa?**

Los **módulos del kernel** y los **programas de espacio de usuario** tienen propósitos, comportamientos y restricciones completamente diferentes.

#### Lugar donde se ejecutan

* **Programa**: Se ejecuta en el **espacio de usuario**, aislado del kernel. No tiene acceso directo al hardware ni a estructuras internas del sistema operativo.
* **Módulo del kernel**: Se ejecuta en el **espacio del kernel**, con acceso total al hardware y a las estructuras internas del SO. Forma parte del núcleo en ejecución.

#### Inicio y fin del ciclo de vida

* **Programa**:

  * Comienza en la función `main()`.
  * Se ejecuta línea por línea hasta su final o hasta que se detiene (voluntaria o involuntariamente).
  * El sistema operativo gestiona su creación y destrucción.

* **Módulo**:

  * Comienza con la función `module_init()` y termina con `module_exit()`.
  * Permanece **activo en memoria** mientras el kernel lo necesite.
  * No se ejecuta "linealmente" como un programa. Su código es invocado por el kernel cuando es necesario.

#### Herramientas y funciones disponibles

* **Programa**:

  * Usa funciones de la **libc** (por ejemplo, `printf`, `scanf`, `malloc`, etc).
  * Puede usar llamadas al sistema para acceder a recursos (mediante `strace` podés verlas).

* **Módulo**:

  * No puede usar funciones de biblioteca estándar (no hay `printf`, `malloc`, etc).
  * Solo puede usar **símbolos exportados por el kernel** (como `printk`, `kmalloc`, `copy_to_user`, etc).
  * El kernel define su propia "API".

#### Consecuencias de un error

* **Programa**: Si se cuelga o falla (ej: `segmentation fault`), el sistema operativo lo mata. **No afecta al resto del sistema**.
* **Módulo**: Si tiene un error, **puede colapsar todo el sistema operativo** (kernel panic). No hay aislamiento: si el módulo falla, falla el kernel.

#### Ejemplo de uso

* **Programa**: Un juego, un editor de texto, una calculadora.
* **Módulo**: Un driver de red, un controlador de USB, un sistema de archivos, un firewall (como Netfilter)

#### Cuadro comparativo

| **Aspecto**                  | **Programa (Espacio de Usuario)**                                | **Módulo del Kernel (Espacio del Kernel)**                          |
| ---------------------------- | ---------------------------------------------------------------- | ------------------------------------------------------------------- |
| **Espacio de ejecución**     | Espacio de usuario                                               | Espacio del kernel                                                  |
| **Punto de entrada**         | `main()`                                                         | `module_init()`                                                     |
| **Forma de finalización**    | Termina al finalizar la ejecución del código                     | Se descarga con `module_exit()` o `rmmod`                           |
| **Acceso al hardware**       | Indirecto, a través de llamadas al sistema                       | Directo, puede manipular hardware (drivers, puertos, IRQs)          |
| **Dependencia del SO**       | Depende del sistema operativo para su gestión                    | Se ejecuta como parte integral del kernel                           |
| **Funciones disponibles**    | Funciones de la biblioteca estándar (`libc`, `printf`, `malloc`) | Solo funciones exportadas por el kernel (`printk`, `kmalloc`, etc.) |
| **Compilación**              | Se genera un ejecutable (`a.out`, `programa`)                    | Se genera un archivo `.ko` (kernel object)                          |
| **Ejecución**                | Ejecutado por el sistema operativo como un proceso independiente | Insertado en el kernel en tiempo de ejecución                       |
| **Tolerancia a errores**     | Aislado; si falla no afecta al sistema                           | Crítico; un error puede generar un *kernel panic*                   |
| **Uso típico**               | Aplicaciones, herramientas de usuario                            | Drivers, extensiones del kernel, sistemas de archivos               |
| **Visibilidad del sistema**  | Acceso limitado al sistema                                       | Acceso completo a estructuras internas del kernel                   |
| **Comunicación con usuario** | Entrada/salida estándar, GUI, sockets                            | Vía archivos en `/proc`, llamadas ioctl, sysfs                      |

---

### **6. ¿Cómo puede ver una lista de las llamadas al sistema que realiza un simple helloworld en c?**

Se puede ver la lista de llamadas al sistema que realiza un programa en C (como un `helloworld.c`) usando **`strace`**, una herramienta que intercepta y muestra todas las llamadas al sistema realizadas por un proceso en Linux.

#### 1. Crear un programa `helloworld.c`

```c
#include <stdio.h>

int main() {
    printf("Hola mundo\n");
    return 0;
}
```

#### 2. Compilarlo

```bash
gcc helloworld.c -o helloworld
```

#### 3. Ejecutar con `strace`

```bash
strace ./helloworld
```

Este comando mostrará **todas las llamadas al sistema** realizadas por el programa, incluyendo `write()`, `open()`, `mmap()`, `exit_group()`, entre otras.

#### **Salida simplificada**

```
execve("./helloworld", ["./helloworld"], 0x7fffdc1f) = 0
brk(NULL)                               = 0x564f1591d000
mmap(NULL, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = ...
write(1, "Hola mundo\n", 11)            = 11
exit_group(0)                           = 0
```

```bash
execve("./helloworld", ["./helloworld"], 0x7fffdc1f) = 0
```

* **`execve`** es la llamada al sistema que el shell usa para ejecutar un binario.
* Toma tres argumentos: la ruta del ejecutable (`"./helloworld"`), los argumentos (`["./helloworld"]`) y las variables de entorno.
* El resultado `= 0` indica que la llamada fue exitosa.

```bash
brk(NULL) = 0x564f1591d000
```

* **`brk()`** es una llamada para gestionar el heap del proceso, es decir, la memoria dinámica.
* En este caso, se consulta la posición actual del "break" del heap sin cambiarlo.
* El resultado indica la dirección actual del heap.

```bash
mmap(NULL, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = ...
```

* **`mmap()`** se usa para asignar páginas de memoria al proceso, típicamente para el stack, buffers o librerías dinámicas.
* Está pidiendo 8192 bytes (una página de memoria) de forma anónima y privada.
* `PROT_READ|PROT_WRITE` indica que puede leerse y escribirse.
* `-1` y `0` indican que no está mapeando un archivo, sino que es memoria vacía.

```bash
write(1, "Hola mundo\n", 11) = 11
```

* **`write()`** es la llamada que realmente imprime el mensaje en pantalla.
* El `1` es el descriptor del archivo correspondiente a **stdout**.
* `"Hola mundo\n"` es el texto a imprimir, y `11` es la cantidad de bytes.
* Devuelve `11`, lo que indica que se escribieron correctamente todos los bytes.

Esto nos muestra que `printf()` no es más que una función de la biblioteca C que internamente **llama al sistema a través de `write()`**.

```bash
exit_group(0) = 0
```

* **`exit_group()`** termina el proceso y libera sus recursos.
* El `0` indica que el programa finalizó correctamente.
* Es la versión moderna de `exit()` para programas multihilo.

#### **Resumen conceptual**

Este trazado muestra cómo un programa tan simple como `helloworld`:

1. Se ejecuta con `execve()`.
2. Reserva memoria (`brk()`, `mmap()`).
3. Escribe en pantalla (`write()`).
4. Finaliza (`exit_group()`).

Estas llamadas son **interfaces entre el espacio de usuario y el kernel**. Toda operación importante que hace un programa (entradas/salidas, memoria, procesos, archivos) **pasa por el kernel** mediante estas llamadas.

---
