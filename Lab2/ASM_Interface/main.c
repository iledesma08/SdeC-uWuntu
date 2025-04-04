#include <stdio.h>

/**
 * @param ptr Pointer to an integer
 * @brief This function increments the value pointed to by ptr by 1.
 */
extern void sum(int* ptr); // Function declaration with cdecl calling convention

void main(void)
{
    int i  =  10;
    sum(&i);

    printf("%d", i); 
    return;
}


