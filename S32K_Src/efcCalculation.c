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
    // example loop for measuring DoD every 200ms
    while (1) {
        double DoD = measureDoD(); // function to measure DoD

        double neq = NeqRealTime(DoD); // compute Neq using real-time function

        // use neq and prevNeq as needed for control or monitoring
        // ...

        sleep(0.2); // wait 200ms before measuring DoD again
    }

    return 0;
}
