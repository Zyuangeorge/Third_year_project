#include <math.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdint.h>

#define OCV_TABLE_SIZE 1000

typedef struct {
    float coefficient_4th;
    float coefficient_3rd;
    float coefficient_2nd;
    float coefficient_1st;
    float constant;
} ocv_config_t;

uint32_t g_ocvTable[OCV_TABLE_SIZE];

/*!
 * @brief Fill in the OSC-SOC lookup table.
 * The items in the lookup table is the voltage.
 * The index of the lookup table is the SOC value.
 * There are 1000 elements in the lookup table, so the accuracy of SOC is 0.1%
 */
void fillOcvTable(const ocv_config_t* const ocvConfig)
{
    uint16_t i = 0;
    uint16_t soc;
    float term_1, term_2, term_3, term_4, sum;

    for (soc = 0; soc <= OCV_TABLE_SIZE; soc++)
    {
        term_1 = ocvConfig->coefficient_4th * (soc * 0.1) * (soc * 0.1) * (soc * 0.1) * (soc * 0.1);
        term_2 = ocvConfig->coefficient_3rd * (soc * 0.1) * (soc * 0.1) * (soc * 0.1);
        term_3 = ocvConfig->coefficient_2nd * (soc * 0.1) * (soc * 0.1);
        term_4 = ocvConfig->coefficient_1st * (soc * 0.1);

        sum = term_1 + term_2 + term_3 + term_4 + ocvConfig->constant;

        g_ocvTable[i] = (uint32_t)round(sum * 1000000); // Round the result of the function so that all the value will be integer

        i++;
    }
}

static void getSOCResult(uint32_t cellVoltage, int16_t *soc)
{
    int16_t left = 0;
    int16_t right = OCV_TABLE_SIZE - 1;
    int16_t middle;

    if (g_ocvTable[OCV_TABLE_SIZE - 1] <= cellVoltage)
    {
        *soc = OCV_TABLE_SIZE - 1;
        return;
    }

    if (g_ocvTable[0] >= cellVoltage)
    {
        *soc = 0;
        return;
    }

    while (left <= right)
    {
        middle = (left + right) >> 1U;
        if (g_ocvTable[middle] > cellVoltage)
        {
            right = middle;
        }
        else
        {
            left = middle;
        }
    }

    *soc = left;
}

void test_fillOcvTable()
{
    ocv_config_t config = {
        .coefficient_4th = 1.0,
        .coefficient_3rd = 2.0,
        .coefficient_2nd = 3.0,
        .coefficient_1st = 4.0,
        .constant = 5.0
    };

    fillOcvTable(&config);

    // Check first and last values in the lookup table
    if (g_ocvTable[0] != 5000000) {
        printf("Test fillOcvTable failed: unexpected first value in lookup table\n");
        printf("Expected: %u, Actual: %u\n", 5000000, g_ocvTable[0]);
    }
    if (g_ocvTable[OCV_TABLE_SIZE - 1] != 1736441856) {
        printf("Test fillOcvTable failed: unexpected last value in lookup table\n");
        printf("Expected: %u, Actual: %u\n", 1736441856, g_ocvTable[OCV_TABLE_SIZE - 1]);
    }

    // Check some values in the lookup table
    if (g_ocvTable[500] != 829423616) {
        printf("Test fillOcvTable failed: unexpected value in lookup table\n");
        printf("Expected: %u, Actual: %u\n", 829423616, g_ocvTable[500]);
    }
    if (g_ocvTable[900] != 981467136) {
        printf("Test fillOcvTable failed: unexpected value in lookup table\n");
        printf("Expected: %u, Actual: %u\n", 981467136, g_ocvTable[900]);
    }
}

void test_getSOCResult()
{
    int16_t soc;

    // Test case 1: voltage lower than any in the table
    getSOCResult(4000000, &soc);
    if (soc != 0)
    {
        printf("Test getSOCResult failed: unexpected result for test case 1\n");
    }

    // Test case 2: voltage higher than any in the table
    getSOCResult(9000000, &soc);
    if (soc != OCV_TABLE_SIZE - 2)
    {
        printf("Test getSOCResult failed: unexpected result for test case 2\n");
    }

    // Test case 3: voltage in the middle of the table
    getSOCResult(556327719, &soc);
    if (soc != 590)
    {
        printf("Test getSOCResult failed: unexpected result for test case 3\n");
    }
}

void runTests()
{
    test_fillOcvTable();
    test_getSOCResult();
}

int main()
{
    // Run the tests
    runTests();

    return 0;
}
