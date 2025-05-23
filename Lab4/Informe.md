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

# Bibliografía
 [Arranque Seguro](https://docs.redhat.com/es/documentation/red_hat_enterprise_linux/8/html/managing_monitoring_and_updating_the_kernel/signing-kernel-modules-for-secure-boot_managing-kernel-modules)

 [¿Qué es un módulo de kernel?](https://sysprog21.github.io/lkmpg/#what-is-a-kernel-module)

 [Estructuras de Datos para GDT y LDT](https://stackoverflow.com/questions/25762625/file-in-which-the-data-structure-for-global-descriptor-and-local-descriptor-tabl)  

 [Llamadas de sistema](https://opensource.com/article/19/10/strace)