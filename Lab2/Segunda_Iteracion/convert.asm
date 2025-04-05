global convert

section .text
convert:
    ; usa xmm0, devuelve en eax
    cvtss2si eax, xmm0
    add eax, 1
    ret

section .note.GNU-stack noalloc noexec
