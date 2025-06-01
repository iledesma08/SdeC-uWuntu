/**
 * @file tp5_driver.c
 * @brief TP5 - Simulación de señales con dispositivo de carácter
 * @author Sistemas de Computación
 * @date 1 de Junio, 2025
 * @version 1.0
 *
 * Este módulo del kernel implementa un dispositivo de carácter que simula dos señales:
 *  - signal1: Señal cuadrada que alterna entre 0 y 1 cada 0.5 segundos
 *  - signal2: Señal triangular que incrementa en 2 cada 10ms, creando un triángulo simétrico de 0 a 100
 *
 * El usuario puede seleccionar cuál señal leer escribiendo "1" o "2" en el dispositivo.
 * La lectura devuelve el valor actual de la señal seleccionada.
 */

#include <linux/cdev.h>    /**< Estructuras y funciones para registrar dispositivos de carácter */
#include <linux/device.h>  /**< Funciones para crear dispositivos en /dev/ y gestión de clases */
#include <linux/fs.h>      /**< Funciones del sistema de archivos y operaciones de archivo */
#include <linux/init.h>    /**< Macros __init y __exit para funciones de inicialización y limpieza */
#include <linux/jiffies.h> /**< Definiciones para trabajar con jiffies, HZ y temporización */
#include <linux/kernel.h>  /**< Funciones de kernel como printk y niveles de log KERN_INFO */
#include <linux/module.h>  /**< Macros para module_init, module_exit, MODULE_LICENSE, etc. */
#include <linux/timer.h>   /**< Estructuras y funciones para trabajar con timers del kernel */
#include <linux/uaccess.h> /**< Funciones copy_to_user y copy_from_user para transferir datos */

/** @def DEVICE_NAME
 *  @brief Nombre del dispositivo en el sistema de archivos /dev/
 */
#define DEVICE_NAME "tp5_driver"

/** @def CLASS_NAME
 *  @brief Nombre de la clase del dispositivo para sysfs
 */
#define CLASS_NAME "tp5_class"

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Sistemas de Computación");
MODULE_DESCRIPTION("TP5 - Simulación de señales con CDD");

/** @brief Número de dispositivo (mayor:menor) */
static dev_t dev_num;

/** @brief Estructura del dispositivo de carácter */
static struct cdev c_dev;

/** @brief Clase del dispositivo para crear /dev/tp5_driver */
static struct class* cl;

/** @brief Timer del kernel para actualizar las señales */
static struct timer_list signal_timer;

/** @brief Valor de la señal cuadrada (0 o 1) */
static int signal1 = 0;

/** @brief Valor de la señal triangular (0 a 100) */
static int signal2 = 0;

/** @brief Dirección de la señal triangular: +1 (sube), -1 (baja) */
static int signal2_dir = 1;

/** @brief Selección del usuario: 1 = señal cuadrada, 2 = señal triangular */
static int active_signal = 1;

/**
 * @brief Función callback del timer ejecutada periódicamente
 * @param timer Puntero a la estructura del timer
 *
 * Esta función se ejecuta cada 10ms y actualiza ambas señales:
 * - signal1: Cambia cada 0.5 segundos (50 ticks de 10ms)
 * - signal2: Incrementa/decrementa en 2 cada tick para formar una triangular
 */
static void timer_callback(struct timer_list* timer)
{
    static int ticks = 0;

    ticks++;
    if (ticks >= 50)
    {
        signal1 = !signal1;
        ticks = 0;
    }

    signal2 += 2 * signal2_dir;

    if (signal2 >= 100)
    {
        signal2 = 100;
        signal2_dir = -1;
    }
    else if (signal2 <= 0)
    {
        signal2 = 0;
        signal2_dir = 1;
    }

    mod_timer(&signal_timer, jiffies + HZ / 100);
}

/**
 * @brief Función de lectura del dispositivo
 * @param f Puntero al archivo
 * @param buf Buffer del espacio de usuario donde escribir los datos
 * @param len Longitud máxima a leer
 * @param off Offset en el archivo
 * @return Número de bytes leídos o código de error negativo
 *
 * Esta función lee el valor actual de la señal seleccionada y lo devuelve
 * como texto al espacio de usuario. Equivale a hacer "cat /dev/tp5_driver".
 */
static ssize_t my_read(struct file* f, char __user* buf, size_t len, loff_t* off)
{
    char msg[32];
    int size;

    if (*off > 0)
        return 0;

    if (active_signal == 1)
        size = snprintf(msg, sizeof(msg), "%d\n", signal1);
    else
        size = snprintf(msg, sizeof(msg), "%d\n", signal2);

    if (copy_to_user(buf, msg, size))
        return -EFAULT;

    *off += size;
    return size;
}

/**
 * @brief Función de escritura del dispositivo
 * @param f Puntero al archivo
 * @param buf Buffer del espacio de usuario con los datos a escribir
 * @param len Longitud de los datos
 * @param off Offset en el archivo
 * @return Número de bytes escritos o código de error negativo
 *
 * Esta función permite al usuario seleccionar qué señal leer escribiendo
 * "1" o "2" en el dispositivo. Equivale a hacer "echo 1 > /dev/tp5_driver".
 */
static ssize_t my_write(struct file* f, const char __user* buf, size_t len, loff_t* off)
{
    char kbuf[2];

    if (len < 1)
        return -EINVAL;

    if (copy_from_user(kbuf, buf, 1))
        return -EFAULT;

    if (kbuf[0] == '1')
        active_signal = 1;
    else if (kbuf[0] == '2')
        active_signal = 2;
    else
        return -EINVAL;
    return len;
}

/**
 * @brief Función de apertura del dispositivo
 * @param i Puntero al inode
 * @param f Puntero al archivo
 * @return 0 en caso de éxito
 *
 * Se ejecuta cuando un proceso abre el dispositivo.
 */
static int my_open(struct inode* i, struct file* f)
{
    printk(KERN_INFO "tp5_driver: open()\n");
    return 0;
}

/**
 * @brief Función de cierre del dispositivo
 * @param i Puntero al inode
 * @param f Puntero al archivo
 * @return 0 en caso de éxito
 *
 * Se ejecuta cuando un proceso cierra el dispositivo.
 */
static int my_close(struct inode* i, struct file* f)
{
    printk(KERN_INFO "tp5_driver: close()\n");
    return 0;
}

/** @brief Estructura de operaciones del archivo del dispositivo */
static struct file_operations fops = {
    .owner = THIS_MODULE,
    .open = my_open,
    .release = my_close,
    .read = my_read,
    .write = my_write,
};

/**
 * @brief Función de inicialización del módulo
 * @return 0 en caso de éxito, código de error negativo en caso de fallo
 *
 * Esta función se ejecuta cuando se carga el módulo con insmod.
 * Registra el dispositivo de carácter, crea la entrada en /dev/ y
 * configura el timer para las señales.
 */
static int __init tp5_init(void)
{
    int ret;
    struct device* dev_ret;

    if ((ret = alloc_chrdev_region(&dev_num, 0, 1, DEVICE_NAME)) < 0)
        return ret;

    if (IS_ERR(cl = class_create(CLASS_NAME)))
    {
        unregister_chrdev_region(dev_num, 1);
        return PTR_ERR(cl);
    }

    if (IS_ERR(dev_ret = device_create(cl, NULL, dev_num, NULL, DEVICE_NAME)))
    {
        class_destroy(cl);
        unregister_chrdev_region(dev_num, 1);
        return PTR_ERR(dev_ret);
    }

    cdev_init(&c_dev, &fops);
    if ((ret = cdev_add(&c_dev, dev_num, 1)) < 0)
    {
        device_destroy(cl, dev_num);
        class_destroy(cl);
        unregister_chrdev_region(dev_num, 1);
        return ret;
    }

    timer_setup(&signal_timer, timer_callback, 0);
    mod_timer(&signal_timer, jiffies + HZ / 20);

    printk(KERN_INFO "tp5_driver: módulo cargado\n");
    return 0;
}

/**
 * @brief Función de limpieza del módulo
 *
 * Esta función se ejecuta cuando se descarga el módulo con rmmod.
 * Limpia todos los recursos: timer, dispositivo de carácter, entrada en /dev/, etc.
 */
static void __exit tp5_exit(void)
{
    del_timer_sync(&signal_timer);
    cdev_del(&c_dev);
    device_destroy(cl, dev_num);
    class_destroy(cl);
    unregister_chrdev_region(dev_num, 1);
    printk(KERN_INFO "tp5_driver: módulo descargado\n");
}

module_init(tp5_init);
module_exit(tp5_exit);
