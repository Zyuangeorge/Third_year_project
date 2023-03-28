#include <stdio.h>
#include <math.h>


float EFCHisData[4] = {0.0,0.0,0.0,0.0};
float efcCycle = 0.0;

// This method is called equivalent number of cycles, related to the DoD, not equivalent full cycle.

float NeqRealTime(void)
{
    float neq;

    neq = 0.5 * (2.0 - (0.5*(EFCHisData[3]+EFCHisData[2]) + EFCHisData[0]) / EFCHisData[1]);

    return neq;
}

int main() {
    float testDoD[4] = {0.4, 0.8, 0.5, 0.5}; // example DoD measurements
    float neq;
    for (int i = 0; i < 4; i++) {
        EFCHisData[i] = testDoD[i];
        printf("%f\n", EFCHisData[i]);
    }

    neq = NeqRealTime();
    
    efcCycle += neq;

    printf("%f\n", neq);

    return 0;
}
