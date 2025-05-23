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
La herramienta que nos facilida la creación de paquetes `.deb`, `.rpm` o `.tgz` es **checkinstall**, a partir de la instalación tradicional utilizando `make install`. En vez de copiar los archivos al sistema, intercepta esa acción y genera un paquete instalable, compatible con el gestor de paquetes de la distribución.
- Permite conocer los paquetes instalados.
- Mejora la distribución e instalación de paquetes en otros sistemas.
- Facilita la desinstalación de paquetes.

### Proceso de empaquetamiento

### Acciones para mejorar la Seguridad del Kernel
Para reforzar la seguridad del kernel, podemos tomar ciertas acciones como impedir la carga de módulos no firmados. Protegiendo al sistema contra módulos maliciosos como los `rootkits` que se insertan en el kernel para ocultar procesos, archivos o actividades.


Para autofirmar los módulos de kernel construidos de forma privada para su uso con RHEL 8 que incluye, cargadores de arranque firmados, granos firmados y módulos del kernel firmados; En sistemas basados en UEFI con arranque seguro, es necesario:

#### Autentificar un módulo de Kernel
Cuando se carga el módulo, en RHEL 8 se comprueba la firma del mismo con las claves públicas X.509 en `.builtin_trusted_keys` (Claves públicas integradas en el kernel), `.platform` (Claves de proveedores de plataformas y claves personalizadas) y en `.blacklist` (lista de claves revocadas).

1. **Generar un par de claves X.509**
```bash
  openssl req -new -x509 -newkey rsa:2048 -keyout MOK.priv -outform DER -out MOK.der -nodes -days 36500 -subj "/CN=MiClave/"
```

2. **Registrar la clave pública con el sistema (MOK)**
```bash
  sudo mokutil --import MOK.der
```
3. **Firmar el módulo del kernel**
```bash
  sudo /usr/src/kernels/$(uname -r)/scripts/sign-file sha256 MOK.priv MOK.der my_module.ko
```

4. **Instalar y cargar el módulo firmado:**
```bash
  sudo cp my_module.ko /lib/modules/$(uname -r)/extra/
  sudo depmod -a
  sudo modprobe my_module
```

5. **Verificar que se haya cargado correctamente**
```bash
  lsmod | grep my_module
```

## Desafío 2

###  Espacio de Usuario vs Espacio del Kernel
- **Programa (Espacio de Usuario)**:
  - Utiliza **llamadas al sistema** para interactuar con el kernel (por ejemplo: `open()`, `read()`, `write()`, `ioctl()`, etc.).
  - Accede a bibliotecas de alto nivel (`glibc`, `libc`, etc.).
  - No puede acceder directamente al hardware ni a estructuras del kernel.

- **Módulo (Espacio del Kernel)**:
  - Tiene acceso a funciones internas del kernel como `printk()`, `copy_to_user()`, `request_irq()`, etc.
  - Interactúa directamente con el hardware y administra recursos críticos.
  - Puede definir funciones como `init_module()` y `cleanup_module()` para inicialización y limpieza de los módulos.


| Característica       | Espacio de Usuario                         | Espacio del Kernel                        |
|----------------------|--------------------------------------------|-------------------------------------------|
| Privilegios          | Restringidos                               | Máximos (modo supervisor)                 |
| Acceso a hardware    | No permitido directamente                  | Permitido                                 |
| Estabilidad del sistema | No afecta directamente al sistema       | Un error puede colapsar el sistema        |
| Comunicación         | Mediante llamadas al sistema               | Directa con recursos del sistema          |


### Espacio de Datos

- **Espacio de datos del usuario**: 
  - Corresponde a la memoria del proceso en ejecución (heap, stack, datos, código).
  - El kernel no puede acceder directamente, debe usar funciones como `copy_from_user()`.

- **Espacio de datos del kernel**: 
  - Compartido entre todos los procesos en modo kernel.
  - Contiene estructuras como tablas de procesos, buffers de E/S, estructuras de módulos, etc.


### Drivers y el contenido de `/dev`

- **Drivers (controladores)**:
  - Son módulos del kernel que permiten la comunicación entre el sistema operativo y el hardware.
  - Implementan operaciones como `open()`, `read()`, `write()`, `release()` para interactuar con dispositivos.

- **Contenido de `/dev`**:
  - Contiene archivos especiales que representan dispositivos del sistema.
  - Ejemplos:
    - `/dev/null`: Dispositivo que descarta cualquier dato escrito.
    - `/dev/sda`: Disco duro o SSD.
    - `/dev/tty`: Terminales virtuales.
    - `/dev/random` y `/dev/urandom`: Generadores de números aleatorios.
  - Los archivos en `/dev` se comunican con los drivers correspondientes mediante los *major* y *minor numbers*.

---

# Bibliografía
 [Arranque Seguro](https://docs.redhat.com/es/documentation/red_hat_enterprise_linux/8/html/managing_monitoring_and_updating_the_kernel/signing-kernel-modules-for-secure-boot_managing-kernel-modules)

 [¿Qué es un módulo de kernel?](https://sysprog21.github.io/lkmpg/#what-is-a-kernel-module)

 [Llamadas de sistema](https://opensource.com/article/19/10/strace)