#include <stdio.h>

double prevDoD = 0.0;     // previous DoD value
double prevPrevDoD = 0.0; // DoD value two measurements ago
double prevNeq = 0.0;     // previous Neq value

double NeqRealTime(double DoD)
{
    double neq;

    if (prevDoD == 0.0 || prevPrevDoD == 0.0) {
        neq = 0.0; // set Neq to 0 for first two measurements
    } else {
        neq = 0.5 * (2.0 - (DoD + prevPrevDoD) / prevDoD);
    }

    prevPrevDoD = prevDoD; // update previous DoD value two measurements ago
    prevDoD = DoD;         // update previous DoD value one measurement ago
    prevNeq = neq;         // update previous Neq value

    return neq;
}

int main()
{
    double testDoD[] = {0.3, 0.5, 0.2, 0.8}; // example DoD measurements
    double expectedNeq[] = {0.0, 0.0, 0.333333, -0.416667}; // expected Neq values

    for (int i = 0; i < 4; i++) {
        double DoD = testDoD[i];
        double neq = NeqRealTime(DoD);
        double expected = expectedNeq[i];

        if (neq == expected) {
            printf("Test %d passed\n", i+1);
        } else {
            printf("Test %d failed: expected %f, but got %f\n", i+1, expected, neq);
        }
    }

    return 0;
}
