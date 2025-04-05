#include <stdio.h>
#include <stdlib.h>

void convertion(float* input, int* output, int length)
{
    for(int i = 0; i < length; i++)
    {
        output[i] = (int)(input[i]+1.0f);
    }
}

int main()
{
    float gini_vals[] = {42.6f, 33.9f, 28.4f, 49.7f, 37.3f};
    int gini_vals_int[5];

    convertion(gini_vals, gini_vals_int, 5);

    for(int i = 0; i<5; i++)
    {
        printf("%d \n", gini_vals_int[i]);
    }
    return 0;
}