#include <stdio.h>
#include <stdlib.h>

/**
 * @param value value to perform operation
 * @brief This function parse the value to Int and increments the value.
 */
extern int convert(float value);

/**
 * @brief Converts an array of floating-point numbers to an array of integers.
 *
 * @param input Pointer to the input array of floating-point numbers.
 * @param output Pointer to the output array where converted integers will be stored.
 * @param length The number of elements in the input and output arrays.
 */
void convertion(float* input, int* output, int length) {
    for (int i = 0; i < length; i++) {
        output[i] = convert(input[i]);
    }
}

int main(void) {
    float  in[1]  = {38.5f};  
    int    out[1] = {0};      

    convertion(in, out, 1);     
    for (int i = 0; i < 1; i++)  
        printf("in[%d]=%f → out[%d]=%d\n", i, in[i], i, out[i]);

    return 0;
}
