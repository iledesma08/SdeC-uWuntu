; int convert(float x)
; Converts a float to int and adds 1
global convert

section .text
convert:
    ; Input:  float in xmm0 (System V ABI)
    ; Output: int in eax
    
    cvtss2si eax, xmm0
    add eax, 1
    ret

section .note.GNU-stack noalloc noexec
