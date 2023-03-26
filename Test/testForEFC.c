#include <stdio.h>
#include <math.h>

float prevDoD = 0.0;
float prevPrevDoD = 0.0;

float NeqRealTime(float DoD)
{
    float neq;

    printf("DoD = %f, prevDoD = %f, prevPrevDoD = %f, neq = %f\n", DoD, prevDoD, prevPrevDoD, neq);

    if (prevDoD == 0.0 || prevPrevDoD == 0.0) {
        neq = 0.0; // set Neq to 0 for first two measurements
    }else {
        neq = 0.5 * (2.0 - (DoD + prevPrevDoD) / prevDoD);
    }

    prevPrevDoD = prevDoD; // update previous DoD value two measurements ago

    prevDoD = DoD;         // update previous DoD value one measurement ago

    return neq;
}

int main() {
    float testDoD[] = {0.4, 0.8, 0.5}; // example DoD measurements
    float expectedNeq[] = {0.0, 0.0, 0.4375}; // updated expected Neq values

    int numTests = sizeof(testDoD) / sizeof(float);

    for (int i = 0; i < numTests; i++) {
        float DoD = testDoD[i];
        float neq = NeqRealTime(DoD);
        float expected = expectedNeq[i];

        if (fabs(neq - expected) < 1e-6) {
            printf("Test %d passed\n", i+1);
        } else {
            printf("Test %d failed: expected %f, but got %f\n", i+1, expected, neq);
        }

        prevPrevDoD = prevDoD;
        prevDoD = DoD;
    }

    return 0;
}
