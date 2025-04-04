section .text
    global sum


sum:
    PUSH ebp
    MOV ebp, esp
    MOV eax, [ebp + 8]
    ADD dword [eax], 1; // *arg += 1
    MOV esp, ebp
    POP ebp
    RET

section .note.GNU-stack noalloc noexec nowrite progbits

; [int* i]        
; [DIR RETORNO]   
; [EBP(anterior)] 


