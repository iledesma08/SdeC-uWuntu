.code16
.global _start
_start:
    cli

    # Cargar GDT
    lgdt gdt_descriptor

    # Activar modo protegido
    movl %cr0, %eax
    orl $0x1, %eax
    movl %eax, %cr0

    # Salto lejano para cambiar CS
    ljmp $0x08, $protected_mode

# GDT
.align 8
gdt_start:
    .quad 0x0000000000000000    # Descriptor nulo

    # Código (selector 0x08)
    .word 0xFFFF     # Límite bajo
    .word 0x0000     # Base baja
    .byte 0x00       # Base media
    .byte 0x9A       # Acceso: código + lectura
    .byte 0xCF       # Granularidad
    .byte 0x00       # Base alta

    # Datos (selector 0x10)
    .word 0xFFFF     # Límite bajo
    .word 0x0000     # Base baja
    .byte 0x00       # Base media
    .byte 0x92       # Acceso: datos lectura/escritura
    .byte 0xCF       # Granularidad
    .byte 0x00       # Base alta

gdt_end:

gdt_descriptor:
    .word gdt_end - gdt_start - 1    # Tamaño GDT - 1
    .long gdt_start                  # Dirección base GDT

.code32
protected_mode:
    # Cargar segmentos
    movw $0x10, %ax
    movw %ax, %ds
    movw %ax, %es
    movw %ax, %ss

    # Escribir en memoria
    movl $0x12345678, 0x00100000

    # Leer y escribir en otra dirección para verificar
    movl 0x00100000, %eax
    movl %eax, 0x00100004

hang:
    jmp hang
