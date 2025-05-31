/*
 * tp5_driver.c - TP5 - Simulación de señales con CDD
 *
 * Este módulo del kernel implementa un dispositivo de carácter que simula dos señales:
 *  - signal1: Señal cuadrada que alterna entre 0 y 1 cada segundo.
 *  - signal2: Señal que incrementa en 10 cada segundo y vuelve a 0 al superar 100.
 *
 * El usuario puede seleccionar cuál señal leer escribiendo "1" o "2" en el dispositivo.
 * La lectura devuelve el valor actual de la señal seleccionada.
 */

#include <linux/module.h>       // Para macros module_init, module_exit, etc.
#include <linux/kernel.h>       // Para printk y nivel de log KERN_INFO
#include <linux/init.h>         // Para __init y __exit
#include <linux/fs.h>           // Para funciones de sistema de archivos
#include <linux/cdev.h>         // Para registrar el char device
#include <linux/device.h>       // Para crear /dev/tp5_driver
#include <linux/uaccess.h>      // Para copy_to_user y copy_from_user
#include <linux/timer.h>        // Para utilizar timer_list
#include <linux/jiffies.h>      // Para trabajar con HZ y temporización

#define DEVICE_NAME "tp5_driver"  // Nombre del dispositivo en /dev/
#define CLASS_NAME  "tp5_class"   // Nombre de la clase del dispositivo

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Sistemas de Computación");
MODULE_DESCRIPTION("TP5 - Simulación de señales con CDD");

static dev_t dev_num;               // Número de dispositivo mayor:menor
static struct cdev c_dev;           // Estructura del char device
static struct class *cl;           // Clase para crear /dev/tp5_driver

static struct timer_list signal_timer;  // Timer del kernel para actualizar señales

// Variables de señal
static int signal1 = 0;            // Señal cuadrada (0 o 1)
static int signal2 = 0;            // Señal triangular (0 a 100)
static int signal2_dir = 1;        // Dirección de la triangular: +1 (sube), -1 (baja)
static int active_signal = 1;      // Selección del usuario: 1 = cuadrada, 2 = triangular

// Función que se ejecuta periódicamente
static void timer_callback(struct timer_list *timer)
{
    static int ticks = 0;  // Contador de ticks de 10 ms

    // Señal 1: cambia cada 0.5 segundos = 50 ticks
    ticks++;
    if (ticks >= 50) {
        signal1 = !signal1;  // Alterna entre 0 y 1
        ticks = 0;
    }

    // Señal 2: triangular simétrica, 100 pasos de 2 → 1 segundo de período
    signal2 += 2 * signal2_dir;

    // Cambiar dirección cuando llega a extremos
    if (signal2 >= 100) {
        signal2 = 100;
        signal2_dir = -1;  // Empieza a bajar
    } else if (signal2 <= 0) {
        signal2 = 0;
        signal2_dir = 1;   // Empieza a subir
    }

    // Reprogramar el timer para dentro de 10 ms
    mod_timer(&signal_timer, jiffies + HZ / 100);
}

// Función de lectura (cat /dev/tp5_driver)
static ssize_t my_read(struct file *f, char __user *buf, size_t len, loff_t *off)
{
    char msg[32];   // Buffer para almacenar el número como texto
    int size;

    if (*off > 0) return 0;  // Permite una única lectura (como si fuera EOF)

    // Formatear el valor de la señal seleccionada en texto
    if (active_signal == 1)
        size = snprintf(msg, sizeof(msg), "%d\\n", signal1);
    else
        size = snprintf(msg, sizeof(msg), "%d\\n", signal2);

    // Copiar al espacio de usuario
    if (copy_to_user(buf, msg, size)) return -EFAULT;

    *off += size;  // Actualiza offset para futuras lecturas
    return size;
}

// Función de escritura (echo 1 > /dev/tp5_driver)
static ssize_t my_write(struct file *f, const char __user *buf, size_t len, loff_t *off)
{
    char kbuf[2];  // Buffer para un solo carácter + '\0'

    if (len < 1) return -EINVAL;  // Si se escribe menos de 1 byte

    if (copy_from_user(kbuf, buf, 1)) return -EFAULT;  // Traer 1 byte desde user space

    // Determinar qué señal se selecciona
    if (kbuf[0] == '1')
        active_signal = 1;
    else if (kbuf[0] == '2')
        active_signal = 2;
    else
        return -EINVAL;  // Valor inválido

    return len;
}

static int my_open(struct inode *i, struct file *f) {
    printk(KERN_INFO "tp5_driver: open()\\n");
    return 0;
}

static int my_close(struct inode *i, struct file *f) {
    printk(KERN_INFO "tp5_driver: close()\\n");
    return 0;
}

static struct file_operations fops = {
    .owner = THIS_MODULE,
    .open = my_open,
    .release = my_close,
    .read = my_read,
    .write = my_write,
};

static int __init tp5_init(void)
{
    int ret;
    struct device *dev_ret;

    // 1. Obtener número mayor y menor disponible
    if ((ret = alloc_chrdev_region(&dev_num, 0, 1, DEVICE_NAME)) < 0)
        return ret;

    // 2. Crear clase para que aparezca en /sys/class/
    if (IS_ERR(cl = class_create(CLASS_NAME))) {
        unregister_chrdev_region(dev_num, 1);
        return PTR_ERR(cl);
    }

    // 3. Crear entrada en /dev/
    if (IS_ERR(dev_ret = device_create(cl, NULL, dev_num, NULL, DEVICE_NAME))) {
        class_destroy(cl);
        unregister_chrdev_region(dev_num, 1);
        return PTR_ERR(dev_ret);
    }

    // 4. Inicializar y registrar el cdev
    cdev_init(&c_dev, &fops);
    if ((ret = cdev_add(&c_dev, dev_num, 1)) < 0) {
        device_destroy(cl, dev_num);
        class_destroy(cl);
        unregister_chrdev_region(dev_num, 1);
        return ret;
    }

    // 5. Configurar y arrancar el timer (dentro de 50 ms para asegurar arranque rápido)
    timer_setup(&signal_timer, timer_callback, 0);
    mod_timer(&signal_timer, jiffies + HZ / 20);

    printk(KERN_INFO "tp5_driver: módulo cargado\\n");
    return 0;
}

static void __exit tp5_exit(void)
{
    del_timer_sync(&signal_timer);     // Detiene el timer
    cdev_del(&c_dev);                  // Elimina el char device
    device_destroy(cl, dev_num);       // Elimina el dispositivo de /dev/
    class_destroy(cl);                 // Destruye la clase en /sys/class
    unregister_chrdev_region(dev_num, 1); // Libera el número mayor:menor
    printk(KERN_INFO "tp5_driver: módulo descargado\\n");
}

module_init(tp5_init);
module_exit(tp5_exit);
