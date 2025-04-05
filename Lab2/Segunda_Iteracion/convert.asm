; ----------------------------
; int convert(float input)
; ----------------------------

section .text
global convert

convert:
    push ebp
    mov ebp, esp

    fld dword [ebp+8]   ; ST0 ← valor flotante
    fld1                ; ST0 ← 1.0, ST1 ← value
    faddp st1, st0      ; ST0 ← value + 1.0

    fistp dword [ebp-4] ; convertir a entero, guardar temporal
    mov eax, [ebp-4]    ; resultado en EAX

    mov esp, ebp
    pop ebp
    ret

section .note.GNU-stack noalloc noexec nowrite progbits
