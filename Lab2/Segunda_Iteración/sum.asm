; ----------------------------
; int convert(float input)
; ----------------------------

section .text
    global convert

convert:
    push ebp
    mov ebp, esp

    fld dword [ebp + 8]      ; ST(0) = input
    fistp dword [esp - 4]    ; Guardar en stack temporal
    mov eax, [esp - 4]       ; eax = (int)input
    add eax, 1

    pop ebp
    ret

section .note.GNU-stack noalloc noexec nowrite progbits