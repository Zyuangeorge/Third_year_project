#include <math.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdint.h>

/*!
 * @brief Function used for sorting the cellVoltage as well as cellLabel
 */
void bubbleSort(uint32_t cellVoltage[], uint8_t cellLabel[], uint8_t len)
{
    uint32_t i, j, labelTamp;
    uint32_t dataTamp;

    for (i = 0; i < len - 1; i++){
        for (j = 0; j < len - 1 - i; j ++){
            if (cellVoltage[j] > cellVoltage[j + 1]){
                dataTamp = cellVoltage[j];
                cellVoltage[j] = cellVoltage[j + 1];
                cellVoltage[j + 1] = dataTamp;

                labelTamp = cellLabel[j];
                cellLabel[j] = cellLabel[j + 1];
                cellLabel[j + 1] = labelTamp;                
            }
        }
    }
}


int main() {
    uint32_t cellVoltage[] = { 1977539, 1930541, 2000000, 2018432, 1864471, 1974792, 1973114, 1824035, 2055206, 2089691, 2112121, 2044982, 2047119, 2135009};
    uint8_t cellLabel[] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13};
    uint8_t len = (uint8_t) sizeof(cellVoltage) / sizeof(*cellVoltage);

    bubbleSort(cellVoltage, cellLabel, len);
    uint32_t i;
    for (i = 0; i < len; i++)
        printf("%d ", cellLabel[i]);
    return 0;
}