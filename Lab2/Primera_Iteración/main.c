// convertion.c
#include <stdio.h>
#include <stdlib.h>

/**
 * @param value value to perform operation
 * @brief This function parse the value to Int and increments the value.
 */
extern int convert(float value); // Function declaration with cdecl calling convention

void convertion(float* input, int* output, int length) {
    for (int i = 0; i < length; i++) {
        output[i] = convert(input[i]);
    }
}
