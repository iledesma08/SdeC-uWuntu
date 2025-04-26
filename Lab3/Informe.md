
<h1 align="center">📘 Universidad Nacional de Córdoba</h1>

<p align="center">
  <img src="https://cybersecurityhub.cordoba.gob.ar/wp-content/uploads/2022/02/FCEFyN-Duotono_tagline-Javier-Jorge.png" width="400"/>
</p>

---

<h3 align="center">💻 SISTEMAS DE COMPUTACIÓN</h3>
<h4 align="center">Trabajo Práctico N°3: <em>Modo Protegido</em></h4>
<h4 align="center">Grupo: <strong>uWuntu</strong> 🚀</h4>

---

## Introducción
En los sistemas operativos modernos, las arquitecturas de procesadores fueron evolucionando para ofrecer diferentes modos de operación, tal como **Modo Real** y **Modo Protegido**; El primero se trata de la primera forma en la que se operaban los procesadores x86, fué diseñado para ser simple y permitir una ejecución directa de las instrucciones, mientras que el segundo permitió aprovechar características avanzadas de protección y de multitarea.

| Característica              | Modo Real                   | Modo Protegido               |
|:----------------------------|:----------------------------|:-----------------------------|
| **Tipo de instrucciones**    | 16 bits                     | 32/64 bits                   |
| **Protección de memoria**    | No                          |                           Sí |
| **Multitarea**               | No                          | Sí                            |
| **Seguridad**                | Baja, sin aislamiento       | Alta, con aislamiento entre procesos |
| **Acceso a hardware**        | Acceso directo              | Acceso controlado y restringido |

El uso hoy en día del modo real se limita sólamente al proceso de arranque, donde los sistemas operativos arrancan en modo real para ejecutar las rutinas iniciales del BIOS o UEFI, incluyendo la verificación del hardware y la carga del bootloader.

## Desarrollo
### UEFI y Coreboot

**UEFI (Unified Extensible Firmware Interface)** es una interfaz moderna entre el firmware del hardware y el sistema operativo que reemplaza al antiguo BIOS (Basic Input Output System) que tradicionalmente es basado en texto con configuraciones ajustadas mediante teclas específicas (modo real, teclado), esto nos permite iniciar el hardware para luego arrancar el sistema operativo; Para utilizarlo, al encender la computadora, presionando una tecla como `F2`, `Del` o `Esc` donde accedemos a UEFI desde una interfaz operativa donde es posible configurar el hardware, el orden de booteo, y demás.

<p align="center">
  <img src="/Lab3/Img/UEFI_BIOS.png" width="600"/>
</p>

| Aspecto | BIOS | UEFI |
|:---|:---|:---|
| **Origen** | Antiguo (1980s) | Moderno (2005+) |
| **Interfaz** | Texto | Gráfica y mouse |
| **Tamaño de disco soportado** | Hasta 2 TB | Más de 2 TB |
| **Velocidad de arranque** | Lento | Rápido |
| **Seguridad** | Básica | Secure Boot |
| **Arquitectura** | 16 bits | 32/64 bits |
| **Compatibilidad** | Alta con sistemas viejos | Mejor con sistemas nuevos |


Desde un sistema operativo se puede hacer llamadas a funciones UEFI, como:

| Función | Descripción|
|:---|:---|
| **GetTime()** | Lee la fecha y hora actual del sistema desde el reloj en tiempo real (RTC). |
| **SetTime()** | Cambia la fecha y hora del sistema. Solo puede hacerlo si el firmware lo permite (por seguridad). |
| **GetVariable()** | Recupera una variable almacenada en la memoria NVRAM (por ejemplo, configuraciones de booteo). |
| **SetVariable()** | Crea o actualiza una variable en la NVRAM. Sirve para guardar configuraciones persistentes. |
| **GetNextVariableName()** | Sirve para enumerar todas las variables NVRAM disponibles. |
| **ResetSystem()** | Reinicia o apaga el sistema de manera controlada desde el firmware. |
| ...| ... |


En UEFI existen varios bugs, un ejemplo famoso fue **Boothole** (2020), una vulnerabilidad en GRUB2 que afectaba sistemas UEFI Secure Boot, permitiendo a atacantes ejecutar código malicioso antes del arranque del sistema operativo, otros bugs se dan por mal manejo de variables NVRAM o drivers UEFI inseguros.

- **CSME (Converged Security and Management Engine)** es una parte del hardware de Intel que maneja la seguridad y gestión del sistema de forma independiente al CPU principal. Corre en un microprocesador embebido.
- **MEBx (Intel Management Engine BIOS Extension)** es la interfaz de configuración de esa tecnología. Permite configurar redes, contraseñas, y otras funciones de administración remota.

**Coreboot** es un proyecto de firmware de código abierto que reemplaza el BIOS propietario tradicional. Su objetivo principal es inicializar el hardware de la forma más rápida y sencilla posible, para luego arrancar un sistema operativo o un cargador de arranque.

Se caracteriza por:
- Realizar solo las tareas estrictamente necesarias para cargar un sistema operativo.
- Ser modular, rápido y confiable.

Lo utilizan las **Chromebooks**, **System76**, **Purism Librem**, **PC Engines APU**, **Raptor Computing Systems**, entre otros

| Ventaja | Descripción |
|:---|:---|
| **Arranque más rápido** | Inicializa el hardware de manera eficiente, reduciendo el tiempo de booteo. |
| **Código abierto y auditable** | Cualquiera puede inspeccionar, modificar y mejorar el código fuente. |
| **Mayor control sobre el hardware** | Permite personalizar exactamente qué componentes se inicializan. |
| **Mayor seguridad** | Evita firmware propietario cerrado que podría contener vulnerabilidades ocultas. |
| **Flexibilidad** | Puede trabajar con payloads como SeaBIOS, Tianocore, LinuxBoot o directamente con un kernel Linux. |
| **Menor tamaño** | El firmware generado es mucho más pequeño que un BIOS tradicional. |

Es posible crear nuestra propia imágen booteable simplemente respetando la estructura clásica genérica del MBR, en la siguiente imágen se crea un archivo `.img` de manera que este produzca un `halt` en qemu (máquina virtual).

<p align="center">
  <img src="/Lab3/Img/qemu_halt.jpeg" width="600"/>
</p>
---


# Linker
Un **linker** se trata de una herramienta que toma varios archivos de objetos generados por el compilador y los combina en un único ejecutable, es el encargado de resolver referencias a funciones y variables entre archivos.

---

# Modo Protegido

## Programa con dos descriptores de memoria (código y datos)
Se deben crear dos descriptores en la GDT:
- Uno para el segmento de código (solo lectura y ejecución).
- Uno para el segmento de datos (lectura/escritura).

## Cambiar bits de acceso del segmento de datos a solo lectura
Si se modifica el descriptor para que el segmento de datos sea solo lectura y luego se intenta escribir:
- Debería lanzarse una excepción de protección general (#GP).
- El sistema operativo o el manejador de excepciones debería actuar.

Esto puede verificarse en `gdb` generando la falla.

## ¿Con qué valor se cargan los registros de segmento en modo protegido? ¿Por qué?
Se cargan con el **selector** de la GDT correspondiente, no directamente con una dirección. El selector contiene el índice de entrada en la GDT y privilegios.

Esto es necesario porque en modo protegido no se trabaja directamente con direcciones físicas, sino con descriptores que definen propiedades del segmento (base, límite, permisos).


## Conclusión


## Bibliografías
 [Paso Modo Protegido x86](http://sistemasdecomputacionunc.blogspot.com/2014/04/paso-modo-protegido-x86.html)
 [Tutorial sobre la GDT](https://wiki.osdev.org/GDT_Tutorial)
 [Estructuras de Datos para GDT y LDT](https://stackoverflow.com/questions/25762625/file-in-which-the-data-structure-for-global-descriptor-and-local-descriptor-tabl)  
 [El mundo del Modo Protegido](http://www.osdever.net/tutorials/view/the-world-of-protected-mode)
 [Ejemplos bare-metal de x86](https://github.com/cirosantilli/x86-bare-metal-examples)