<h1 align="center">📘 Universidad Nacional de Córdoba</h1>

<p align="center">
  <img src="https://cybersecurityhub.cordoba.gob.ar/wp-content/uploads/2022/02/FCEFyN-Duotono_tagline-Javier-Jorge.png" width="400"/>
</p>

---

<h3 align="center">💻 SISTEMAS DE COMPUTACIÓN</h3>
<h4 align="center">Trabajo Práctico N°4: <em>Módulos de Kernel & Llamadas a sistema</em></h4>
<h4 align="center">Grupo: <strong>uWuntu</strong> 🚀</h4>

---

# Introducción

Los módulos de kernel son fragmentos de código que permiten ampliar las funcionalidades del núcleo del sistema operativo sin necesidad de recompilar ni reiniciar todo el kernel. Esto es especialmente útil cuando se desea agregar nuevas funciones —como soporte para un dispositivo de hardware— sin modificar directamente el núcleo principal, que suele ser complejo y monolítico. 

Dado que estos módulos interactúan directamente con el núcleo, también representan la posibilidad de tener vulnerabilidades o pueden ser creados para usos maliciosos. Para mitigar estos riesgos, los sistemas implementan mecanismos de seguridad como la verificación mediante firmas digitales o claves, asegurando que solo módulos autorizados o firmados puedan ser cargados.

Las llamadas al sistema son la forma principal que los programas interactúan con el núcleo del sistema operativo, mediante esto, es posible que una aplicación soliicite servicios fundamentales como acceso a archivos, comunicación entre los procesos, adignación de memoria o el control de los dispositivos. Actúa como un puente seguro entre el espacio de usuario y el espacio del kernel, esto evita que los programas accedan directamente a los recursos del sistema operativo por razones de seguridad y estabilidad, cuando un proceso necesita realizar una operación privilegiada,  invoca una llamada al sistema específica, y el kernel se encarga de ejecutarla de forma controlada.

# Desarrollo

## Desafío 1

## Desafío 2

El objetivo de este apartado es examinar las llamadas al sistema realizadas por un programa en lenguaje C elemental, cuya única función es imprimir en pantalla el mensaje "Hello, world!". A pesar de su simplicidad, este tipo de programa permite evidenciar la interacción básica entre el espacio de usuario y el núcleo del sistema operativo, particularmente a través de la interfaz de llamadas al sistema (syscalls).

Para este análisis se utilizó la herramienta strace, ampliamente empleada en entornos Linux para rastrear y diagnosticar las llamadas al sistema que efectúa un proceso durante su ejecución.

## ¿Qué es un Segmentation Fault?

Un Segmentation Fault (fallo de segmentación) es un error en tiempo de ejecución que ocurre cuando un programa intenta acceder a una región de memoria que no tiene permiso para usar. Esto incluye situaciones como:

- Desreferenciar un puntero nulo
- Escribir en una dirección de solo lectura
- Acceder fuera de los límites de un array

Cuando esto sucede:

- El kernel, a través del sistema de memoria virtual y la MMU (Unidad de Gestión de Memoria), detecta la violación de acceso y genera una excepción.  
  Esta excepción se traduce en el envío de una señal SIGSEGV al proceso. Si el proceso no tiene un manejador específico para esa señal, será terminado automáticamente y se puede generar un core dump para análisis posterior.

- El programa, en el espacio de usuario, puede definir un manejador de señales (por ejemplo con `sigaction`) para interceptar la señal SIGSEGV. Esto permite, por ejemplo, imprimir información de diagnóstico antes de que el proceso finalice, aunque no es recomendable intentar continuar la ejecución.

### Ejemplo de código que genera un segmentation fault

```c
int *ptr = NULL;
*ptr = 5;  // Intento de escritura en una dirección no válida
```

En este ejemplo, el puntero `ptr` apunta a `NULL`, y cualquier intento de escritura provoca un acceso inválido de memoria.

> Este tipo de fallos son una forma en que el kernel protege la integridad del sistema, evitando que los programas mal diseñados o defectuosos afecten a otros procesos o al propio sistema operativo.

## Análisis de llamadas al sistema en un programa Hello World en C

### Introducción

Este sección del documento examina las llamadas al sistema (*syscalls*) realizadas por un programa elemental en lenguaje C cuya única función es imprimir el mensaje "Hello, world!" en pantalla. Aunque aparentemente simple, este programa permite evidenciar la interacción fundamental entre el espacio de usuario y el kernel del sistema operativo a través de la interfaz de llamadas al sistema.

El análisis se realizó utilizando `strace`, una herramienta estándar en entornos Linux para rastrear y diagnosticar las llamadas al sistema que ejecuta un proceso durante su funcionamiento.

### Compilación del programa

Se creó un archivo fuente en C con el siguiente contenido:

```c
#include <stdio.h>

int main() {
    printf("Hello, world!\n");
    return 0;
}
```

El programa se compiló utilizando GCC con la siguiente instrucción:

```bash
gcc -Wall -o hello hello.c
```

### Seguimiento detallado con `strace -tt`

Para observar las llamadas al sistema con marcas temporales precisas, se ejecutó:

```bash
strace -tt ./hello
```

El resultado obtenido fue:

```
17:09:49.315772 execve("./hello", ["./hello"], 0x7fffa4371cb8 /* 55 vars */) = 0
17:09:49.316168 brk(NULL)               = 0x59ddee103000
17:09:49.316223 mmap(NULL, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7218fe37d000
17:09:49.316269 access("/etc/ld.so.preload", R_OK) = -1 ENOENT (No such file or directory)
17:09:49.316361 openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
17:09:49.316415 fstat(3, {st_mode=S_IFREG|0644, st_size=93343, ...}) = 0
17:09:49.316460 mmap(NULL, 93343, PROT_READ, MAP_PRIVATE, 3, 0) = 0x7218fe366000
17:09:49.316496 close(3)                = 0
17:09:49.316534 openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libc.so.6", O_RDONLY|O_CLOEXEC) = 3
17:09:49.316571 read(3, "\177ELF\2\1\1\3\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\220\243\2\0\0\0\0\0"..., 832) = 832
17:09:49.316607 pread64(3, "\6\0\0\0\4\0\0\0@\0\0\0\0\0\0\0@\0\0\0\0\0\0\0@\0\0\0\0\0\0\0"..., 784, 64) = 784
17:09:49.316641 fstat(3, {st_mode=S_IFREG|0755, st_size=2125328, ...}) = 0
17:09:49.316675 pread64(3, "\6\0\0\0\4\0\0\0@\0\0\0\0\0\0\0@\0\0\0\0\0\0\0@\0\0\0\0\0\0\0"..., 784, 64) = 784
17:09:49.316711 mmap(NULL, 2170256, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x7218fe000000
17:09:49.316746 mmap(0x7218fe028000, 1605632, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x28000) = 0x7218fe028000
17:09:49.316788 mmap(0x7218fe1b0000, 323584, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x1b0000) = 0x7218fe1b0000
17:09:49.316826 mmap(0x7218fe1ff000, 24576, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x1fe000) = 0x7218fe1ff000
17:09:49.316874 mmap(0x7218fe205000, 52624, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0x7218fe205000
17:09:49.316923 close(3)                = 0
17:09:49.316960 mmap(NULL, 12288, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7218fe363000
17:09:49.317002 arch_prctl(ARCH_SET_FS, 0x7218fe363740) = 0
17:09:49.317034 set_tid_address(0x7218fe363a10) = 950843
17:09:49.317065 set_robust_list(0x7218fe363a20, 24) = 0
17:09:49.317096 rseq(0x7218fe364060, 0x20, 0, 0x53053053) = 0
17:09:49.317175 mprotect(0x7218fe1ff000, 16384, PROT_READ) = 0
17:09:49.317212 mprotect(0x59ddc89e9000, 4096, PROT_READ) = 0
17:09:49.317249 mprotect(0x7218fe3b5000, 8192, PROT_READ) = 0
17:09:49.317303 prlimit64(0, RLIMIT_STACK, NULL, {rlim_cur=8192*1024, rlim_max=RLIM64_INFINITY}) = 0
17:09:49.317348 munmap(0x7218fe366000, 93343) = 0
17:09:49.317405 fstat(1, {st_mode=S_IFCHR|0620, st_rdev=makedev(0x88, 0x1), ...}) = 0
17:09:49.317442 getrandom("\x5b\x14\xea\x1c\xad\xbd\xd3\xf3", 8, GRND_NONBLOCK) = 8
17:09:49.317477 brk(NULL)               = 0x59ddee103000
17:09:49.317508 brk(0x59ddee124000)     = 0x59ddee124000
17:09:49.317546 write(1, "Hello, world!\n", 14Hello, world!
) = 14
17:09:49.317591 exit_group(0)           = ?
17:09:49.317686 +++ exited with 0 +++
```

#### Análisis de las llamadas principales

El fragmento más relevante del trace es:

```
17:09:49.315772 execve("./hello", ["./hello"], 0x7fffa4371cb8 /* 55 vars */) = 0
...
17:09:49.317546 write(1, "Hello, world!\n", 14Hello, world!) = 14
17:09:49.317591 exit_group(0)           = ?
17:09:49.317686 +++ exited with 0 +++
```

Entre las llamadas observadas se encuentran `execve`, `mmap`, `openat`, `fstat`, `brk`, `write` y `exit_group`. La línea más significativa para nuestro análisis es:

```
write(1, "Hello, world!\n", 14) = 14
```

Esta línea demuestra cómo la función de alto nivel `printf()` se traduce internamente en una llamada al sistema `write`, que escribe directamente en el descriptor de archivo 1 (correspondiente a `stdout`). El valor de retorno `14` indica que se escribieron exitosamente los 14 bytes del mensaje.


#### Resumen estadístico con `strace -c`

Para obtener un análisis cuantitativo del uso de llamadas al sistema, se utilizó la opción `-c`:

```bash
strace -c ./hello
```

Resultado obtenido:

```
Hello, world!
% time     seconds  usecs/call     calls    errors syscall
------ ----------- ----------- --------- --------- ----------------
 58,02    0,000304         304         1           execve
 18,32    0,000096          12         8           mmap
  4,96    0,000026          13         2           openat
  3,05    0,000016           5         3           fstat
  2,29    0,000012           6         2           pread64
  2,10    0,000011           5         2           close
  2,10    0,000011           3         3           mprotect
  2,10    0,000011          11         1         1 access
  1,53    0,000008           8         1           read
  1,15    0,000006           2         3           brk
  1,15    0,000006           6         1           arch_prctl
  1,15    0,000006           6         1           set_robust_list
  1,15    0,000006           6         1           rseq
  0,95    0,000005           5         1           set_tid_address
  0,00    0,000000           0         1           write
  0,00    0,000000           0         1           munmap
  0,00    0,000000           0         1           prlimit64
  0,00    0,000000           0         1           getrandom
------ ----------- ----------- --------- --------- ----------------
100,00    0,000524          15        34         1 total
```

#### Interpretación de los resultados estadísticos

El resumen estadístico revela aspectos importantes sobre el comportamiento del programa:

- **`execve`** representa el 58% del tiempo total de ejecución, siendo la operación más costosa debido a la carga del binario y la inicialización del proceso.

- **`mmap`** consume el 18% del tiempo con 8 llamadas, reflejando las múltiples asignaciones de memoria necesarias para cargar las bibliotecas compartidas.

- La llamada **`write`**, responsable de imprimir nuestro mensaje, aparece con tiempo prácticamente nulo (0,00%) debido a su simplicidad y rapidez de ejecución.

## Implementación del mismo Hello World como módulo del kernel firmado

Como continuación del análisis de llamadas al sistema, se procedió a implementar un módulo del kernel que imprime "Hello, Kernel World!" al cargarse y "Goodbye, Kernel World!" al descargarse. Para asegurar la compatibilidad con sistemas con Secure Boot habilitado, también se firmó dicho módulo.

### Creación del módulo del kernel

#### Código fuente `hellomodule.c`

```c
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>

static int __init hello_init(void) {
    printk(KERN_INFO "Hello, Kernel World!\n");
    return 0;
}

static void __exit hello_exit(void) {
    printk(KERN_INFO "Goodbye, Kernel World!\n");
}

module_init(hello_init);
module_exit(hello_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Tu Nombre");
MODULE_DESCRIPTION("Un módulo Hello World firmado");
```

#### Makefile

```make
obj-m += hellomodule.o

all:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
```

#### Compilación

```bash
make
```

Esto generará `hellomodule.ko`.

### Firma del módulo para Secure Boot

#### 1. Crear clave y certificado

```bash
mkdir ~/modsign
cd ~/modsign
openssl req -new -x509 -newkey rsa:2048 -keyout MOK.priv -outform DER -out MOK.der -nodes -days 36500 -subj "/CN=My Kernel Module Signing Key by UWU Team/"
```

| Opción             | Significado                                                                                                              |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------ |
| `req`              | Inicia una solicitud de certificado X.509.                                                                               |
| `-new`             | Indica que se está generando una nueva solicitud de certificado.                                                         |
| `-x509`            | Solicita que OpenSSL genere directamente un certificado X.509 autofirmado, en lugar de una CSR para CA.              |
| `-newkey rsa:2048` | Genera una nueva clave privada RSA de 2048 bits.                                                                     |
| `-keyout MOK.priv` | Guarda la clave privada en el archivo `MOK.priv`.                                                                        |
| `-outform DER`     | Exporta el certificado en formato DER (binario), que es requerido por `mokutil`.                                     |
| `-out MOK.der`     | Guarda el certificado público en el archivo `MOK.der`.                                                                   |
| `-nodes`           | Evita que se encripte la clave privada (sin passphrase). Necesario para que `sign-file` la pueda usar automáticamente.   |
| `-days 36500`      | El certificado tendrá una validez de 100 años (36500 días), útil para evitar vencimientos frecuentes.                |
| `-subj "/CN=..."`  | Define el campo `Common Name` del certificado. Es opcional, pero recomendable para identificar el propósito de la clave. |

> **Nota:** Un certificado X.509 es un archivo digital que asocia una clave pública con una identidad verificable (como una persona, organización o sistema).  
>  
> Es el estándar más utilizado en sistemas de confianza digital, como HTTPS y Secure Boot. Contiene información como:
> - Clave pública
> - Identidad del titular
> - Período de validez
> - Algoritmo de firma
> - Firma digital que lo autentica
>  
> En el contexto de firmado de módulos del kernel, se usa para que el sistema (Secure Boot) pueda verificar que la firma del módulo proviene de una fuente confiable.

<p align="center">
  <img src="./Img/Key_Certificate.png" width="800"/>
</p>

<p align="center"><strong>Figura 1:</strong> Generación de un certificado X.509 autofirmado y su clave privada usando OpenSSL.  
Este certificado será utilizado para firmar módulos del kernel en un entorno con Secure Boot habilitado.</p>



#### 2. Registrar la clave con `mokutil`

```bash
sudo mokutil --import MOK.der
```

<p align="center">
  <img src="./Img/MOK_DER.png" width="600"/>
</p>

<p align="center"><strong>Figura 2:</strong> Proceso de importación del certificado público (`MOK.der`) en la base de claves de Secure Boot utilizando `mokutil`.  
Se solicita una contraseña temporal que se usará para confirmar la operación en el menú de MOK Manager al reiniciar el sistema.</p>


- Ingresamos una contraseña que recordemos fácilmente
- Reiniciamos el sistema
- En el menú de MOK Manager que aparecerá al inicio, seleccionamos:
    - Enroll MOK
    - Continue
    - Ingresamos la contraseña que elegimos
    - Reboot

<p align="center">
  <img src="./Img/MOK_1.jpeg" width="500"/>
</p>
<p align="center"><strong>Figura 3:</strong> Menú inicial del MOK Manager al iniciar el sistema. Desde aquí se accede a la opción para registrar una nueva clave pública.</p>

<p align="center">
  <img src="./Img/MOK_2.jpeg" width="500"/>
</p>
<p align="center"><strong>Figura 4:</strong> Solicitud de la contraseña temporal establecida al ejecutar `mokutil --import` para validar el proceso de enrolamiento.</p>

<p align="center">
  <img src="./Img/MOK_3.jpeg" width="500"/>
</p>
<p align="center"><strong>Figura 5:</strong> Confirmación del usuario para autorizar el registro de la clave en la base MOK del sistema.</p>

<p align="center">
  <img src="./Img/MOK_4.jpeg" width="500"/>
</p>
<p align="center"><strong>Figura 6:</strong> Vista previa de la clave a registrar antes de continuar con el proceso.</p>

<p align="center">
  <img src="./Img/MOK_5.jpeg" width="500"/>
</p>
<p align="center"><strong>Figura 7:</strong> Selección final de la opción "Enroll MOK" para completar el registro y permitir la carga de módulos firmados con esa clave.</p>

#### 2.1 Verificación de Secure Boot

Antes de firmar e intentar cargar el módulo, es fundamental verificar que el sistema tenga Secure Boot activado, ya que esto garantiza que solo se permitirán módulos del kernel con firmas válidas.

Para comprobarlo, ejecutamos el siguiente comando:

```bash
mokutil --sb-state
```

La salida esperada es:

<p align="center">
  <img src="./Img/SecureBoot.png" width="500"/>
</p>

<p align="center"><strong>Figura 8:</strong> Verificación del estado de Secure Boot utilizando el comando `mokutil --sb-state`.</p>

Esto confirma que el sistema está funcionando con Secure Boot habilitado.  
Como resultado, cualquier módulo `.ko` que se desee cargar deberá estar firmado digitalmente con una clave previamente registrada mediante el mecanismo de MOK (Machine Owner Key).

> Si `SecureBoot` no está activado, el sistema permitirá la carga de módulos sin firma.


#### 3. Firmar el módulo

Antes de ejecutar este comando, asegurate de estar ubicado en la carpeta que contiene el archivo `hellomodule.ko`, ya que el script `sign-file` espera encontrar el módulo en el directorio actual.

```bash
sudo /usr/src/linux-headers-$(uname -r)/scripts/sign-file sha256 ~/modsign/MOK.priv ~/modsign/MOK.der hellomodule.ko
```

#### 4. Verificar la firma

```bash
modinfo hellomodule.ko | grep -i signer
```

<p align="center">
  <img src="./Img/Signer.png" width="600"/>
</p>

<p align="center"><strong>Figura 9:</strong> Verificación de la firma del módulo `hellomodule.ko` mediante `modinfo`.  
Se confirma que fue firmado correctamente con la clave "My Kernel Module Signing Key by UWU Team", coincidiendo con el certificado MOK registrado.</p>

#### 5. Cargar y verificar el módulo firmado

Antes de ejecutar los siguientes comandos, asegurate de estar ubicado en la carpeta donde se encuentra el archivo `hellomodule.ko`, ya que `insmod` espera encontrar el módulo en el directorio actual o con una ruta válida.

```bash
sudo insmod hellomodule.ko
dmesg | tail
```

El comando `dmesg | tail` muestra los últimos mensajes del kernel.  
Si la carga fue exitosa, deberías ver una línea como:

```
Hello, Kernel World!
```

---

Para descargar el módulo y confirmar su correcta limpieza:

```bash
sudo rmmod hellomodule
dmesg | tail
```

Nuevamente, `dmesg | tail` permite verificar la salida del kernel.  
En este caso, deberías ver:

```
Goodbye, Kernel World!
```

Este proceso confirma que tanto la función de inicialización (`init`) como la de limpieza (`exit`) del módulo están funcionando correctamente.

<p align="center">
  <img src="./Img/HelloAndGoodbye.png" width="600"/>
</p>

<p align="center"><strong>Figura 10:</strong> Salida del comando `dmesg` que muestra los mensajes del kernel al cargar y descargar el módulo.  
Se observa que el módulo fue cargado correctamente, ejecutando "Hello, Kernel World!", y posteriormente removido, mostrando "Goodbye, Kernel World!".</p>


# Bibliografía
 [Arranque Seguro](https://docs.redhat.com/es/documentation/red_hat_enterprise_linux/8/html/managing_monitoring_and_updating_the_kernel/signing-kernel-modules-for-secure-boot_managing-kernel-modules)

 [¿Qué es un módulo de kernel?](https://sysprog21.github.io/lkmpg/#what-is-a-kernel-module)

 [Estructuras de Datos para GDT y LDT](https://stackoverflow.com/questions/25762625/file-in-which-the-data-structure-for-global-descriptor-and-local-descriptor-tabl)  

 [Llamadas de sistema](https://opensource.com/article/19/10/strace)