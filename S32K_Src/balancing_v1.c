#include <math.h>
#include <stdlib.h>
#include "bcc/bcc.h"
#include "bcc_s32k144/bcc_wait.h"
#include "common.h"

/* Array used in UART communication */
uint32_t cellData[17];

/* Timeout value of the lpit */
int32_t timeout = 0;
uint32_t balanceTimeout = 0;

/* BCC driver configuration. */
bcc_drv_config_t drvConfig;

#define BATTERY_NUMBER 14; // Number of cells
#define VOLTAGE_DIFFERENCE_THRESHOLD 5000; // 5000 uV
#define MAX_BALANCED_CELL_NUMBER 7; // Maximum number of cells under balancing
#define REST_TIME 1000; // Rest time between balancing processes in mS

static void bubbleSort(uint32_t cellVoltage, int8_t cellLabel);
static void cellBalancing(uint32_t cellData, int32_t timeoutMs);

/*!
 * @brief Function used for sorting the cellVoltage as well as cellLabel
 */
static void bubbleSort(uint32_t cellVoltage, uint8_t cellLabel)
{
    uint8_t i, j, labelTamp, len;
    uint32_t dataTamp;

    len = (uint8_t) sizeof(cellVoltage) / sizeof(*cellVoltage);
    for (i = 0; i < len - 1; i++){
        for (j = 0; j < len - 1 - i; j ++){
            if (cellVoltage[j] > arr[j + 1]){
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

/*!
 * @brief Function used for cell balancing
 */
static void cellBalancing(void)
{
    uint32_t cellVoltage = [];
    uint8_t cellLabel = [];
    uint8_t i, j; 
    uint8_t balancedCellNumber;
    uint16_t balanceTime = 1; // In minutes
    
    for(i = 0; i < BATTERY_NUMBER; i++){
        cellVoltage[i] = cellData[i + 1];
        cellLabel[i] = i; 
    }

    bubbleSort(cellVoltage, cellLabel);

    if((cellVoltage[BATTERY_NUMBER - 1] - cellVoltage[0]) > VOLTAGE_DIFFERENCE_THRESHOLD){
        BCC_CB_Enable(drvConfig, BCC_CID_DEV1, true);

        for(i = BATTERY_NUMBER - 1; i > 1; i--){
            if((cellVoltage[i] - cellVoltage[0]) > VOLTAGE_DIFFERENCE_THRESHOLD){
                balancedCellNumber++;
            }
            if(balancedCellNumber < MAX_BALANCED_CELL_NUMBER){
                BCC_CB_SetIndividual(drvConfig, BCC_CID_DEV1, i, true, balanceTime);
            }
        }
    }
    else{
        BCC_CB_Pause(drvConfig, BCC_CID_DEV1, true);
    }
}

/*!
* @brief LPIT0 IRQ handler.
*/
void LPIT0_Ch0_IRQHandler(void)
{
    LPIT_DRV_ClearInterruptFlagTimerChannels(INST_LPIT1, (1 << LPIT0_CHANNEL_TYPGUI));
    timeout--;
    balanceTimeout++;
}

/*!
 * @brief Function used for cell balancing control
 */
static void cellBalancingControl(void)
{
    uint8_t cellIndex;
    uint16_t readVal;
    bool balanceEnable = false;

    for(i = 0; i < BATTERY_NUMBER; i++){
        BCC_Reg_Read(drvConfig, BCC_CID_DEV1, MC33771C_CB1_CFG_OFFSET + cellIndex, 1U, &readVal);
        balanceEnable |= readVal;
    }
    
    if((!balanceEnable == true) && (balanceTimeout == REST_TIME)){
        cellBalancing();
        balanceTimeout = 0; // Reset balance time out to 1 min
    }
}
