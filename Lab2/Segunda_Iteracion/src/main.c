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
 * This function takes an input array of floating-point numbers and converts
 * each element to an integer using the `convert` function. The converted
 * integers are stored in the output array.
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
