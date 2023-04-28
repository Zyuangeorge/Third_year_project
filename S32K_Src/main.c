/* ###################################################################
**     Filename    : main.c
**     Processor   : S32K1xx
**     Abstract    :
**         Main module.
**         This module contains user's application code.
**     Settings    :
**     Contents    :
**         No public methods
**
** ###################################################################*/
/*!
** @file main.c
** @version 1.0.0
** @brief
** 			Used for 7-cell lithium ion battery.
**         	Enhanced CC method.
**         	7 cell balancing.
*/
/*!
**  @addtogroup main_module main module documentation
**  @{
*/

/* MODULE main */

/* Including necessary module. Cpu.h contains other modules needed for compiling.*/
#include "Cpu.h"

  volatile int exit_code = 0;

/* User includes (#include below this line is not maintained by Processor Expert) */
#include <math.h>
#include <stdlib.h>
#include <string.h>
#include "bcc/bcc.h"
#include "bcc_s32k144/bcc_wait.h"
#include "common.h"

/*******************************************************************************
* Definitions
******************************************************************************/

/* On-board LED.
 * Blue: Charging
 * Green: Discharging
 * White: OC
 * Red: error
 */
#define RED_LED_PORT         PTD
#define RED_LED_PIN          15U
#define BLUE_LED_PORT        PTD
#define BLUE_LED_PIN         0U
#define GREEN_LED_PORT        PTD
#define GREEN_LED_PIN         16U

/* Relay port */
#define RELAY_PORT         PTC
#define RELAY_PIN          8U

/* LPSPI_TX configuration. */
#define BCC_TX_LPSPI_DELAY_PCS_TO_SCLK         3U  /* 3us (f >= 1.75us) */
#define BCC_TX_LPSPI_DELAY_SCLK_TO_PCS         1U  /* 1us (g >= 0.60us) */
#define BCC_TX_LPSPI_DELAY_BETWEEN_TRANSFERS   5U  /* 5us (t_MCU_RES >= 4us) */

/* Used channel of LPIT0 for GUI timing. */
#define LPIT0_CHANNEL_TYPGUI  0U

/* Used channel of LPIT0 for BCC SW driver timing. */
#define LPIT0_CHANNEL_BCCDRV   3U

/* Battery rated capacitance */
#define RATEDCAPACITANCE    2.9

/* The minimum value of OCV */
#define OCV_MINSOC          0

/* The maximum value of OCV */
#define OCV_MAXSOC          1000 // permille

/* The size of the lookup table*/
#define OCV_TABLE_SIZE      (OCV_MAXSOC - OCV_MINSOC + 1) // 1000 sets of data in the lookupTable

/* Operation efficiency */
#define KC 1 // Charging tuning
#define KD 1.15 // Discharging tuning

/* Current threshold for determining the current direction */
#define ISENSETHRESHOLD 8500 // In uV

/* Battery minimum and maximum voltages */
#define MC33771C_TH_ALL_CT_UV_TH 2600 // 2600 mV
#define MC33771C_TH_ALL_CT_OV_TH 4300 // 4300 mV

/* Voltage difference threshold for cell balancing 5 mV */
#define VOLTAGE_DIFFERENCE_THRESHOLD 5000

/* Maximum number of cells under balancing */
#define MAX_BALANCED_CELL_NUMBER 3 //

/* Rest time between balancing processes in mS */
#define REST_TIME 3500

/* Cell balancing time setting in minute */
#define BALANCE_TIME 1

/* Receive buffer size */
#define BUFFER_SIZE 6

/* SoC calibrate time after cell balancing*/
#define BALANCEING_SOC_CALIBRATE_TIME -180000

/* Battery cycle life */
#define CYCLELIFE 1555

/* Lookup table setup */
//#define LINEAR
#define POLYNOMIAL

/*  Number of cells */
#define BATTERY_NUMBER 14 // Don't modify the value, change the setting below

/* Number of cells configuration */
//#define CELL14
#define CELL7

/*******************************************************************************
* Enum definition
******************************************************************************/

//Different state of bms system
typedef enum
{   
    Idle_State,
    Charge_State,
    Discharge_State,
    OpenCircuit_State,
	Fault_State
} bmsSystemState;

//Different type events
typedef enum
{
    Discharge_Event,
    Charge_Event,
    OpenCircuit_Event,
	Fault_Event
} bmsSystemEvent;

/*******************************************************************************
* Structure definition
******************************************************************************/

typedef struct
{
	int16_t SOC_0[BATTERY_NUMBER]; // Initial SoC value: permille

	int16_t SOC_c[BATTERY_NUMBER]; // Current SoC value: permille

    int16_t DOD_0[BATTERY_NUMBER]; // Inital depth of Discharge: permille

    int16_t DOD_c[BATTERY_NUMBER]; // Current depth of Discharge: permille

    int16_t SOH[BATTERY_NUMBER]; // State of health: permille
    
    int16_t CB_ControlStatus[BATTERY_NUMBER]; // Cell balancing control status

    float efcCounter; // EFC counter

    float absIntegratedCurent[BATTERY_NUMBER]; // Absolute integrated current value: A*s

	float integratedCurrent[BATTERY_NUMBER]; // The integral value of current: A*s
} Ah_integral_data;

/* Define a struct used in OCV_SOC lookup table */
typedef struct
{
    float coefficient_4th; // 4th order coefficient

    float coefficient_3rd; // 3rd order coefficient

    float coefficient_2nd; // 2nd order coefficient

    float coefficient_1st; // 1st order coefficient

    float constant; // constant value
} ocv_config_t;

/*******************************************************************************
 * Initial BCC configuration
 ******************************************************************************/

/*! @brief  Number of MC33771 registers configured in the initialization with
 * user values. */
#define BCC_INIT_CONF_REG_CNT     56U

/* Structure containing a register name and its address. */
typedef struct
{
    const uint8_t address;

    const uint16_t defaultVal;

    const uint16_t value;
} bcc_init_reg_t;

/* Initial register configuration for MC33771C for this example. */
static const bcc_init_reg_t s_initRegsMc33771c[BCC_INIT_CONF_REG_CNT] = {
    {MC33771C_GPIO_CFG1_OFFSET, MC33771C_GPIO_CFG1_POR_VAL, MC33771C_GPIO_CFG1_VALUE},
    {MC33771C_GPIO_CFG2_OFFSET, MC33771C_GPIO_CFG2_POR_VAL, MC33771C_GPIO_CFG2_VALUE},
    {MC33771C_TH_ALL_CT_OFFSET, MC33771C_TH_ALL_CT_POR_VAL, MC33771C_TH_ALL_CT_VALUE},
    {MC33771C_TH_CT14_OFFSET, MC33771C_TH_CT14_POR_VAL, MC33771C_TH_CTX_VALUE},
    {MC33771C_TH_CT13_OFFSET, MC33771C_TH_CT13_POR_VAL, MC33771C_TH_CTX_VALUE},
    {MC33771C_TH_CT12_OFFSET, MC33771C_TH_CT12_POR_VAL, MC33771C_TH_CTX_VALUE},
    {MC33771C_TH_CT11_OFFSET, MC33771C_TH_CT11_POR_VAL, MC33771C_TH_CTX_VALUE},
    {MC33771C_TH_CT10_OFFSET, MC33771C_TH_CT10_POR_VAL, MC33771C_TH_CTX_VALUE},
    {MC33771C_TH_CT9_OFFSET, MC33771C_TH_CT9_POR_VAL, MC33771C_TH_CTX_VALUE},
    {MC33771C_TH_CT8_OFFSET, MC33771C_TH_CT8_POR_VAL, MC33771C_TH_CTX_VALUE},
    {MC33771C_TH_CT7_OFFSET, MC33771C_TH_CT7_POR_VAL, MC33771C_TH_CTX_VALUE},
    {MC33771C_TH_CT6_OFFSET, MC33771C_TH_CT6_POR_VAL, MC33771C_TH_CTX_VALUE},
    {MC33771C_TH_CT5_OFFSET, MC33771C_TH_CT5_POR_VAL, MC33771C_TH_CTX_VALUE},
    {MC33771C_TH_CT4_OFFSET, MC33771C_TH_CT4_POR_VAL, MC33771C_TH_CTX_VALUE},
    {MC33771C_TH_CT3_OFFSET, MC33771C_TH_CT3_POR_VAL, MC33771C_TH_CTX_VALUE},
    {MC33771C_TH_CT2_OFFSET, MC33771C_TH_CT2_POR_VAL, MC33771C_TH_CTX_VALUE},
    {MC33771C_TH_CT1_OFFSET, MC33771C_TH_CT1_POR_VAL, MC33771C_TH_CTX_VALUE},
    {MC33771C_TH_AN6_OT_OFFSET, MC33771C_TH_AN6_OT_POR_VAL, MC33771C_TH_ANX_OT_VALUE},
    {MC33771C_TH_AN5_OT_OFFSET, MC33771C_TH_AN5_OT_POR_VAL, MC33771C_TH_ANX_OT_VALUE},
    {MC33771C_TH_AN4_OT_OFFSET, MC33771C_TH_AN4_OT_POR_VAL, MC33771C_TH_ANX_OT_VALUE},
    {MC33771C_TH_AN3_OT_OFFSET, MC33771C_TH_AN3_OT_POR_VAL, MC33771C_TH_ANX_OT_VALUE},
    {MC33771C_TH_AN2_OT_OFFSET, MC33771C_TH_AN2_OT_POR_VAL, MC33771C_TH_ANX_OT_VALUE},
    {MC33771C_TH_AN1_OT_OFFSET, MC33771C_TH_AN1_OT_POR_VAL, MC33771C_TH_ANX_OT_VALUE},
    {MC33771C_TH_AN0_OT_OFFSET, MC33771C_TH_AN0_OT_POR_VAL, MC33771C_TH_ANX_OT_VALUE},
    {MC33771C_TH_AN6_UT_OFFSET, MC33771C_TH_AN6_UT_POR_VAL, MC33771C_TH_ANX_UT_VALUE},
    {MC33771C_TH_AN5_UT_OFFSET, MC33771C_TH_AN5_UT_POR_VAL, MC33771C_TH_ANX_UT_VALUE},
    {MC33771C_TH_AN4_UT_OFFSET, MC33771C_TH_AN4_UT_POR_VAL, MC33771C_TH_ANX_UT_VALUE},
    {MC33771C_TH_AN3_UT_OFFSET, MC33771C_TH_AN3_UT_POR_VAL, MC33771C_TH_ANX_UT_VALUE},
    {MC33771C_TH_AN2_UT_OFFSET, MC33771C_TH_AN2_UT_POR_VAL, MC33771C_TH_ANX_UT_VALUE},
    {MC33771C_TH_AN1_UT_OFFSET, MC33771C_TH_AN1_UT_POR_VAL, MC33771C_TH_ANX_UT_VALUE},
    {MC33771C_TH_AN0_UT_OFFSET, MC33771C_TH_AN0_UT_POR_VAL, MC33771C_TH_ANX_UT_VALUE},
    {MC33771C_CB1_CFG_OFFSET, MC33771C_CB1_CFG_POR_VAL, MC33771C_CBX_CFG_VALUE},
    {MC33771C_CB2_CFG_OFFSET, MC33771C_CB2_CFG_POR_VAL, MC33771C_CBX_CFG_VALUE},
    {MC33771C_CB3_CFG_OFFSET, MC33771C_CB3_CFG_POR_VAL, MC33771C_CBX_CFG_VALUE},
    {MC33771C_CB4_CFG_OFFSET, MC33771C_CB4_CFG_POR_VAL, MC33771C_CBX_CFG_VALUE},
    {MC33771C_CB5_CFG_OFFSET, MC33771C_CB5_CFG_POR_VAL, MC33771C_CBX_CFG_VALUE},
    {MC33771C_CB6_CFG_OFFSET, MC33771C_CB6_CFG_POR_VAL, MC33771C_CBX_CFG_VALUE},
    {MC33771C_CB7_CFG_OFFSET, MC33771C_CB7_CFG_POR_VAL, MC33771C_CBX_CFG_VALUE},
    {MC33771C_CB8_CFG_OFFSET, MC33771C_CB8_CFG_POR_VAL, MC33771C_CBX_CFG_VALUE},
    {MC33771C_CB9_CFG_OFFSET, MC33771C_CB9_CFG_POR_VAL, MC33771C_CBX_CFG_VALUE},
    {MC33771C_CB10_CFG_OFFSET, MC33771C_CB10_CFG_POR_VAL, MC33771C_CBX_CFG_VALUE},
    {MC33771C_CB11_CFG_OFFSET, MC33771C_CB11_CFG_POR_VAL, MC33771C_CBX_CFG_VALUE},
    {MC33771C_CB12_CFG_OFFSET, MC33771C_CB12_CFG_POR_VAL, MC33771C_CBX_CFG_VALUE},
    {MC33771C_CB13_CFG_OFFSET, MC33771C_CB13_CFG_POR_VAL, MC33771C_CBX_CFG_VALUE},
    {MC33771C_CB14_CFG_OFFSET, MC33771C_CB14_CFG_POR_VAL, MC33771C_CBX_CFG_VALUE},
    {MC33771C_OV_UV_EN_OFFSET, MC33771C_OV_UV_EN_POR_VAL, MC33771C_OV_UV_EN_VALUE},
    {MC33771C_SYS_CFG1_OFFSET, MC33771C_SYS_CFG1_POR_VAL, MC33771C_SYS_CFG1_VALUE},
    {MC33771C_SYS_CFG2_OFFSET, MC33771C_SYS_CFG2_POR_VAL, MC33771C_SYS_CFG2_VALUE},
    {MC33771C_ADC_CFG_OFFSET, MC33771C_ADC_CFG_POR_VAL, MC33771C_ADC_CFG_VALUE},
    {MC33771C_ADC2_OFFSET_COMP_OFFSET, MC33771C_ADC2_OFFSET_COMP_POR_VAL, MC33771C_ADC2_OFFSET_COMP_VALUE},
    {MC33771C_FAULT_MASK1_OFFSET, MC33771C_FAULT_MASK1_POR_VAL, MC33771C_FAULT_MASK1_VALUE},
    {MC33771C_FAULT_MASK2_OFFSET, MC33771C_FAULT_MASK2_POR_VAL, MC33771C_FAULT_MASK2_VALUE},
    {MC33771C_FAULT_MASK3_OFFSET, MC33771C_FAULT_MASK3_POR_VAL, MC33771C_FAULT_MASK3_VALUE},
    {MC33771C_WAKEUP_MASK1_OFFSET, MC33771C_WAKEUP_MASK1_POR_VAL, MC33771C_WAKEUP_MASK1_VALUE},
    {MC33771C_WAKEUP_MASK2_OFFSET, MC33771C_WAKEUP_MASK2_POR_VAL, MC33771C_WAKEUP_MASK2_VALUE},
    {MC33771C_WAKEUP_MASK3_OFFSET, MC33771C_WAKEUP_MASK3_POR_VAL, MC33771C_WAKEUP_MASK3_VALUE},
};

/*******************************************************************************
 * Global variables
 ******************************************************************************/

/* BCC driver configuration. */
bcc_drv_config_t drvConfig;

/* Array used in UART communication */
uint32_t cellData[17];

/* Array needed to store all measured values. */
uint16_t measurements[BCC_MEAS_CNT];

/* Ah integral data*/
Ah_integral_data AhData;

/* The OCV-SOC lookup table */
uint32_t g_ocvTable[OCV_TABLE_SIZE];

/* State variable (used as indication if SPI is accessible or not). */
bool sleepMode = false;

/* Timeout value of the lpit */
int32_t timeout = 0;
int32_t balanceTimeout = 0;

/* Current direction flag: 0 is discharge, 1 is charge, 2 is open circuit */
int16_t currentDirectionFlag = 2;

/* Charging and discharging counter used for EFC Calculation */
int16_t EFCFlag = 0;

/* Fault status */
uint16_t faultStatusValue[2]={0, 0}; // [0]: overvoltage [1]: undervoltage

/* ISENSE voltage */
int32_t isenseVolt;

/* Buffer used to receive data from the console */
uint8_t receivedBuffer[BUFFER_SIZE];
uint8_t bufferIdx;

/* Cell balancing control flag. */
bool cellBalancingFlag = false;

/* SoC update flag, used to reset the SoC value*/
bool cellBalancingSoCUpdateFlag = false;

/* Final transmitted data */
/*
 * [0] Pack voltage
 * [1:14] Cell voltage 1 to 14
 * [15] IC temperature
 * [16] Current
 * [17:30] Cell 1 to 14 SoC
 * [31:44] Cell 1 to 14 SoH
 * [45] EFC: Equivalent Full Cycle
 * [46:59] Cell 1 to 14 CB Control 
 * [60] System status
 * [61] Cell balancing status
 */
uint32_t transmittedData[62];

/*******************************************************************************
 * Function prototypes
 ******************************************************************************/

static bcc_status_t initRegisters(void);
static bcc_status_t clearFaultRegs(void);

static void initTimeout(int32_t timeoutMs);
static bool timeoutExpired(void);

static void fillOcvTable(const ocv_config_t* const ocvConfig);
static void getSOCResult(uint32_t cellVoltage, int16_t *soc);

static status_t initAlgorithm(void);
static bcc_status_t initAlgorithmValues(void);
static bcc_status_t updateThreshold(void);

static bcc_status_t updateMeasurements(void);

static void integrateCurrent(void);

static void getCurrentDOD(void);
static void getCurrentSOC(void);
static void updateIntegratedCurrent(int16_t SoC, int8_t cellIndex);

void bubbleSort(uint32_t cellVoltage[], uint8_t cellLabel[], uint8_t len);
static void cellBalancing(void);
static void cellBalancingControl(void);

static void DischargeHandler(void);
static void ChargeHandler(void);
static void OpenCircuitHandler(void);
static bmsSystemState FaultHandler(void);

static bmsSystemEvent monitorBattery(void);

void communicateWithPc(bmsSystemState bmsNextState);
void dataTransmit(bmsSystemState bmsNextState);

static bcc_status_t updateFaultStatus(void);
static void displayStatus(bmsSystemState bmsNextState);

/*******************************************************************************
 * Functions
 ******************************************************************************/

/*!
 * @brief Initializes BCC device registers according to BCC_INIT_CONF.
 * Registers having the wanted content already after POR are not rewritten.
 */
static bcc_status_t initRegisters(void)
{
    uint8_t i;
    bcc_status_t status;

    for (i = 0; i < BCC_INIT_CONF_REG_CNT; i++)
    {
        if (s_initRegsMc33771c[i].value != s_initRegsMc33771c[i].defaultVal)
        {
            status = BCC_Reg_Write(&drvConfig, BCC_CID_DEV1,
                    s_initRegsMc33771c[i].address, s_initRegsMc33771c[i].value);
            if (status != BCC_STATUS_SUCCESS)
            {
                return status;
            }
        }
    }
    return BCC_STATUS_SUCCESS;
}

/*!
 * @brief Clears all fault registers of BCC devices.
 */
static bcc_status_t clearFaultRegs(void)
{
    bcc_status_t status;

    status = BCC_Fault_ClearStatus(&drvConfig, BCC_CID_DEV1, BCC_FS_CELL_OV);
    if (status != BCC_STATUS_SUCCESS)
    {
        return status;
    }

    status = BCC_Fault_ClearStatus(&drvConfig, BCC_CID_DEV1, BCC_FS_CELL_UV);
    if (status != BCC_STATUS_SUCCESS)
    {
        return status;
    }

    status = BCC_Fault_ClearStatus(&drvConfig, BCC_CID_DEV1, BCC_FS_CB_OPEN);
    if (status != BCC_STATUS_SUCCESS)
    {
        return status;
    }

    status = BCC_Fault_ClearStatus(&drvConfig, BCC_CID_DEV1, BCC_FS_CB_SHORT);
    if (status != BCC_STATUS_SUCCESS)
    {
        return status;
    }

    status = BCC_Fault_ClearStatus(&drvConfig, BCC_CID_DEV1, BCC_FS_GPIO_STATUS);
    if (status != BCC_STATUS_SUCCESS)
    {
        return status;
    }

    status = BCC_Fault_ClearStatus(&drvConfig, BCC_CID_DEV1, BCC_FS_AN_OT_UT);
    if (status != BCC_STATUS_SUCCESS)
    {
        return status;
    }

    status = BCC_Fault_ClearStatus(&drvConfig, BCC_CID_DEV1, BCC_FS_GPIO_SHORT);
    if (status != BCC_STATUS_SUCCESS)
    {
        return status;
    }

    status = BCC_Fault_ClearStatus(&drvConfig, BCC_CID_DEV1, BCC_FS_COMM);
    if (status != BCC_STATUS_SUCCESS)
    {
        return status;
    }

    status = BCC_Fault_ClearStatus(&drvConfig, BCC_CID_DEV1, BCC_FS_FAULT1);
    if (status != BCC_STATUS_SUCCESS)
    {
        return status;
    }

    status = BCC_Fault_ClearStatus(&drvConfig, BCC_CID_DEV1, BCC_FS_FAULT2);
    if (status != BCC_STATUS_SUCCESS)
    {
        return status;
    }

    return BCC_Fault_ClearStatus(&drvConfig, BCC_CID_DEV1, BCC_FS_FAULT3);
}

/*!
* @brief This function initializes timeout.
*
* @param timeoutMs timeout delay in [ms].
*/
static void initTimeout(int32_t timeoutMs)
{
    timeout = timeoutMs;
}

/*!
* @brief This function indicates if the timeout expired.
*
* @return True if timeout expired, otherwise false.
*/
static bool timeoutExpired(void)
{
    return (timeout <= 0);
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

    for (soc = OCV_MINSOC; soc <= OCV_MAXSOC; soc++)
    {
        term_1 = ocvConfig->coefficient_4th * (soc * 0.1) * (soc * 0.1) * (soc * 0.1) * (soc * 0.1);
        term_2 = ocvConfig->coefficient_3rd * (soc * 0.1) * (soc * 0.1) * (soc * 0.1);
        term_3 = ocvConfig->coefficient_2nd * (soc * 0.1) * (soc * 0.1);
        term_4 = ocvConfig->coefficient_1st * (soc * 0.1);

        sum = (term_1 + term_2 + term_3 + term_4 + ocvConfig->constant) * 1000000;

        g_ocvTable[i] = (uint32_t)round(sum); // Round the result of the function so that all the value will be integer

        i++;
    }
}

/*!
 * @brief Get the SOC value from the Lookup table.
 * The searching method is binary search.
 */
static void getSOCResult(uint32_t cellVoltage, int16_t *soc)
{
    int16_t left = 0;
    int16_t right = OCV_TABLE_SIZE - 1;
    int16_t middle;

    /* Set the SOC value if the value can't be found in the lookup table */
    if (g_ocvTable[OCV_TABLE_SIZE - 1] <= cellVoltage)
    {
        *soc = OCV_TABLE_SIZE - 1;
    }

    if (g_ocvTable[0] >= cellVoltage)
    {
        *soc = 0;
    }

    /* Search for an element that is close to the input voltage */
    while ((left + 1) != right)
    {
        /* Split interval into halves */
        middle = (left + right) >> 1U;
        if (g_ocvTable[middle] > cellVoltage)
        {
            /* Select right half */
            right = middle;
        }
        else
        {
            left = middle;
        }
    }

    *soc = left;
}

/*!
* @brief This function is used to calculate the initial SOC.
*
* @return bccStatus.
*/
static bcc_status_t initAlgorithmValues(void)
{
	bcc_status_t error;
    ocv_config_t ocvConfig;
    int16_t soc;
    int16_t i;

    /* Start the first measurement */
	error = updateMeasurements();
	if (error != BCC_STATUS_SUCCESS)
	{
		return error;
	}

    /* Initialise lookup table settings */
	#ifdef POLYNOMIAL
        // Polynomial
		ocvConfig.coefficient_4th = -6.712e-08;
		ocvConfig.coefficient_3rd = 1.544e-05;
		ocvConfig.coefficient_2nd = -0.001193;
		ocvConfig.coefficient_1st = 0.04342;
		ocvConfig.constant = 3.025;
	#else
        // Linear
		ocvConfig.coefficient_4th = 0;
		ocvConfig.coefficient_3rd = 0;
		ocvConfig.coefficient_2nd = 0;
		ocvConfig.coefficient_1st = 0.00211;
		ocvConfig.constant = 1.95;
	#endif

	balanceTimeout = 0;

	/* Initialize the OCV-SOC look up table */
	fillOcvTable(&ocvConfig);

	for (i = 0; i < BATTERY_NUMBER; i++){
		/* Get the initial SOC value */
		getSOCResult(cellData[i + 1],&soc);
		AhData.SOC_0[i] = soc;
		AhData.SOC_c[i] = AhData.SOC_0[i];

        AhData.SOH[i] = 1000; // Assume the initial health is 100%

        /* Calculate the initial DOD value */
        AhData.DOD_0[i] = AhData.SOH[i] - AhData.SOC_0[i];
        AhData.DOD_c[i] = AhData.DOD_0[i];

        /* Cet the initial CB control status value */
        AhData.CB_ControlStatus[i] = 0.0;

        /* Set the integrated current value */
        AhData.integratedCurrent[i] = 0.0;
        AhData.absIntegratedCurent[i] = 0.0;
	}

    /* Reset AhData values */
    AhData.efcCounter = 0;

    /* Reset cell balancing control flag */
    cellBalancingFlag = false;

	return BCC_STATUS_SUCCESS;
}

/*!
* @brief This function is used to update threshold value register on MC33771C.
*
* @return bccStatus.
*/
static bcc_status_t updateThreshold(void)
{
	bcc_status_t error;

    error = BCC_Reg_Update(&drvConfig, BCC_CID_DEV1, MC33771C_TH_ALL_CT_OFFSET,
            MC33771C_TH_ALL_CT_ALL_CT_OV_TH_MASK, MC33771C_TH_ALL_CT_ALL_CT_OV_TH(BCC_GET_TH_CTX((int32_t)MC33771C_TH_ALL_CT_OV_TH)));
#ifdef CELL14
    error = BCC_Reg_Update(&drvConfig, BCC_CID_DEV1, MC33771C_TH_ALL_CT_OFFSET,
            MC33771C_TH_ALL_CT_ALL_CT_UV_TH_MASK, MC33771C_TH_ALL_CT_ALL_CT_UV_TH(BCC_GET_TH_CTX((int32_t)MC33771C_TH_ALL_CT_UV_TH)));
#else
    error = BCC_Reg_Update(&drvConfig, BCC_CID_DEV1, MC33771C_TH_ALL_CT_OFFSET,
                MC33771C_TH_ALL_CT_ALL_CT_UV_TH_MASK, MC33771C_TH_ALL_CT_ALL_CT_UV_TH(BCC_GET_TH_CTX((int32_t)MC33771C_TH_ALL_CT_UV_TH)));

	 // Set the undervoltage threshold for CT5 to CT11 to 0V
    error = BCC_Reg_Update(&drvConfig, BCC_CID_DEV1, MC33771C_OV_UV_EN_OFFSET, MC33771C_OV_UV_EN_CT11_OVUV_EN_MASK, MC33771C_OV_UV_EN_CT11_OVUV_EN_DISABLED_ENUM_VAL);
    error = BCC_Reg_Update(&drvConfig, BCC_CID_DEV1, MC33771C_OV_UV_EN_OFFSET, MC33771C_OV_UV_EN_CT10_OVUV_EN_MASK, MC33771C_OV_UV_EN_CT10_OVUV_EN_DISABLED_ENUM_VAL);
    error = BCC_Reg_Update(&drvConfig, BCC_CID_DEV1, MC33771C_OV_UV_EN_OFFSET, MC33771C_OV_UV_EN_CT9_OVUV_EN_MASK, MC33771C_OV_UV_EN_CT9_OVUV_EN_DISABLED_ENUM_VAL);
    error = BCC_Reg_Update(&drvConfig, BCC_CID_DEV1, MC33771C_OV_UV_EN_OFFSET, MC33771C_OV_UV_EN_CT8_OVUV_EN_MASK, MC33771C_OV_UV_EN_CT8_OVUV_EN_DISABLED_ENUM_VAL);
    error = BCC_Reg_Update(&drvConfig, BCC_CID_DEV1, MC33771C_OV_UV_EN_OFFSET, MC33771C_OV_UV_EN_CT7_OVUV_EN_MASK, MC33771C_OV_UV_EN_CT7_OVUV_EN_DISABLED_ENUM_VAL);
    error = BCC_Reg_Update(&drvConfig, BCC_CID_DEV1, MC33771C_OV_UV_EN_OFFSET, MC33771C_OV_UV_EN_CT6_OVUV_EN_MASK, MC33771C_OV_UV_EN_CT6_OVUV_EN_DISABLED_ENUM_VAL);
    error = BCC_Reg_Update(&drvConfig, BCC_CID_DEV1, MC33771C_OV_UV_EN_OFFSET, MC33771C_OV_UV_EN_CT5_OVUV_EN_MASK, MC33771C_OV_UV_EN_CT5_OVUV_EN_DISABLED_ENUM_VAL);
#endif

    if (error != BCC_STATUS_SUCCESS)
    {
        return error;
    }

    return BCC_STATUS_SUCCESS;
}

/*!
 * @brief MCU and BCC initialization.
 */
static status_t initAlgorithm(void)
{
    status_t status;
    bcc_status_t bccStatus;
    
    /* Reset cell balancing */
    BCC_CB_Pause(&drvConfig, BCC_CID_DEV1, true);

    /* Init system clock */
    CLOCK_SYS_Init(g_clockManConfigsArr, CLOCK_MANAGER_CONFIG_CNT,
            g_clockManCallbacksArr, CLOCK_MANAGER_CALLBACK_CNT);
    CLOCK_SYS_UpdateConfiguration(0U, CLOCK_MANAGER_POLICY_FORCIBLE);

    /* Pin-muxing + GPIO pin direction and initial value settings. */
    PINS_DRV_Init(NUM_OF_CONFIGURED_PINS, g_pin_mux_InitConfigArr);

    /* Initialize LPUART instance */
    status = LPUART_DRV_Init(INST_LPUART1, &lpuart1_State, &lpuart1_InitConfig0);
    if (status != STATUS_SUCCESS)
    {
        return STATUS_ERROR;
    }

    /* Initialize LPIT instance */
    LPIT_DRV_Init(INST_LPIT1, &lpit1_InitConfig);
    status = LPIT_DRV_InitChannel(INST_LPIT1, LPIT0_CHANNEL_TYPGUI, &lpit1_ChnConfig0);
    if (status != STATUS_SUCCESS)
    {
        return STATUS_ERROR;
    }
    LPIT_DRV_InitChannel(INST_LPIT1, LPIT0_CHANNEL_BCCDRV, &lpit1_ChnConfig3);
    if (status != STATUS_SUCCESS)
    {
        return STATUS_ERROR;
    }

    /* Initialize LPSPI instance. */
    status = LPSPI_DRV_MasterInit(LPSPICOM1,&lpspiCom1State,&lpspiCom1_MasterConfig0);
    if (status != STATUS_SUCCESS)
    {
        return status;
    }

#ifdef CELL14
    /* Initialize BCC driver configuration structure. */
    drvConfig.drvInstance = 0U;
    drvConfig.commMode = BCC_MODE_SPI;
    drvConfig.devicesCnt = 1U;
    drvConfig.device[0] = BCC_DEVICE_MC33771C;
    drvConfig.cellCnt[0] = 14U;
    drvConfig.loopBack = false;
#else
    /* Initialize BCC driver configuration structure. */
    drvConfig.drvInstance = 0U;
    drvConfig.commMode = BCC_MODE_SPI;
    drvConfig.devicesCnt = 1U;
    drvConfig.device[0] = BCC_DEVICE_MC33771C;
    drvConfig.cellCnt[0] = 7U;
    drvConfig.loopBack = false;
#endif
    LPIT_DRV_StartTimerChannels(INST_LPIT1, (1 << LPIT0_CHANNEL_TYPGUI));

    PINS_DRV_SetPins(RED_LED_PORT, 1U << RED_LED_PIN);
    PINS_DRV_SetPins(BLUE_LED_PORT, 1U << BLUE_LED_PIN);
    PINS_DRV_SetPins(GREEN_LED_PORT, 1U << GREEN_LED_PIN);
    PINS_DRV_SetPins(RELAY_PORT, 1U << RELAY_PIN);

    bccStatus = BCC_Init(&drvConfig);
    if (bccStatus != BCC_STATUS_SUCCESS)
    {
        return STATUS_ERROR;
    }

    bccStatus = initRegisters();
    if (bccStatus != BCC_STATUS_SUCCESS)
    {
        return STATUS_ERROR;
    }

    bccStatus = clearFaultRegs();
    if (bccStatus != BCC_STATUS_SUCCESS)
    {
        return STATUS_ERROR;
    }

    bccStatus = updateThreshold();
    if (bccStatus != BCC_STATUS_SUCCESS)
    {
        return STATUS_ERROR;
    }

    return STATUS_SUCCESS;
}

/*!
 * @brief This function reads values measured and provided via SPI
 * by BCC device (ISENSE, cell voltages, temperatures).
 *
 * @return bcc_status_t Error code.
 */
static bcc_status_t updateMeasurements(void)
{
    bcc_status_t error;

    /* Step 1: Start conversion and wait for the conversion time. */
    error = BCC_Meas_StartAndWait(&drvConfig, BCC_CID_DEV1, BCC_AVG_1);
    if (error != BCC_STATUS_SUCCESS)
    {
        return error;
    }

    /* Step 2: Convert raw measurements to appropriate units. */
    error = BCC_Meas_GetRawValues(&drvConfig, BCC_CID_DEV1, measurements);
    if (error != BCC_STATUS_SUCCESS)
    {
        return error;
    }

    /* You can use bcc_measurements_t enumeration to index array with raw values. */
    /* Useful macros can be found in bcc.h or bcc_MC3377x.h. */
#ifdef CELL14
    cellData[0]= BCC_GET_STACK_VOLT(measurements[BCC_MSR_STACK_VOLT]);
	cellData[1]= BCC_GET_VOLT(measurements[BCC_MSR_CELL_VOLT1]);
	cellData[2]= BCC_GET_VOLT(measurements[BCC_MSR_CELL_VOLT2]);
	cellData[3]= BCC_GET_VOLT(measurements[BCC_MSR_CELL_VOLT3]);
	cellData[4]= BCC_GET_VOLT(measurements[BCC_MSR_CELL_VOLT4]);
	cellData[5]= BCC_GET_VOLT(measurements[BCC_MSR_CELL_VOLT5]);
	cellData[6]= BCC_GET_VOLT(measurements[BCC_MSR_CELL_VOLT6]);
	cellData[7]= BCC_GET_VOLT(measurements[BCC_MSR_CELL_VOLT7]);
	cellData[8]= BCC_GET_VOLT(measurements[BCC_MSR_CELL_VOLT8]);
	cellData[9]= BCC_GET_VOLT(measurements[BCC_MSR_CELL_VOLT9]);
	cellData[10]= BCC_GET_VOLT(measurements[BCC_MSR_CELL_VOLT10]);
	cellData[11]= BCC_GET_VOLT(measurements[BCC_MSR_CELL_VOLT11]);
	cellData[12]= BCC_GET_VOLT(measurements[BCC_MSR_CELL_VOLT12]);
	cellData[13]= BCC_GET_VOLT(measurements[BCC_MSR_CELL_VOLT13]);
	cellData[14]= BCC_GET_VOLT(measurements[BCC_MSR_CELL_VOLT14]);
	cellData[15] = BCC_GET_IC_TEMP_C(measurements[BCC_MSR_ICTEMP]);
#else
    cellData[0]= BCC_GET_STACK_VOLT(measurements[BCC_MSR_STACK_VOLT]);
	cellData[1]= BCC_GET_VOLT(measurements[BCC_MSR_CELL_VOLT1]);
	cellData[2]= BCC_GET_VOLT(measurements[BCC_MSR_CELL_VOLT2]);
	cellData[3]= BCC_GET_VOLT(measurements[BCC_MSR_CELL_VOLT3]);
	cellData[4]= BCC_GET_VOLT(measurements[BCC_MSR_CELL_VOLT4]);
	cellData[5]= 3600000;
	cellData[6]= 3600000;
	cellData[7]= 3600000;
	cellData[8]= 3600000;
	cellData[9]= 3600000;
	cellData[10]= 3600000;
	cellData[11]= 3600000;
	cellData[12]= BCC_GET_VOLT(measurements[BCC_MSR_CELL_VOLT12]);
	cellData[13]= BCC_GET_VOLT(measurements[BCC_MSR_CELL_VOLT13]);
	cellData[14]= BCC_GET_VOLT(measurements[BCC_MSR_CELL_VOLT14]);
	cellData[15] = BCC_GET_IC_TEMP_C(measurements[BCC_MSR_ICTEMP]);
#endif
	/* ISENSE data (current measurement) */
	isenseVolt = BCC_GET_ISENSE_VOLT(measurements[BCC_MSR_ISENSE1], measurements[BCC_MSR_ISENSE2]);
	cellData[16] = BCC_GET_ISENSE_AMP(DEMO_RSHUNT, measurements[BCC_MSR_ISENSE1], measurements[BCC_MSR_ISENSE2]);

	if (isenseVolt > ISENSETHRESHOLD){
		cellData[16] = cellData[16] * KD;
		currentDirectionFlag = 0; // Discharge
        EFCFlag = 0;
	}
	else if(abs(isenseVolt) <= ISENSETHRESHOLD){
		currentDirectionFlag = 2; // Open circuit
	}
    else{
        currentDirectionFlag = 1; // Charge
        EFCFlag = 0;
    }

	return BCC_STATUS_SUCCESS;
}

/*!
 * @brief Model step function 
 */
void integrateCurrent(void)
{
    int16_t current_c; // Current current
    uint8_t i;

    current_c = cellData[16];

    for(i = 0; i < BATTERY_NUMBER; i++){
        AhData.integratedCurrent[i] += 0.001 * current_c * 0.2; //convert to 1A, and 200ms = 0.2s

        if (currentDirectionFlag == 1){
            AhData.absIntegratedCurent[i] -= 0.001 * current_c * 0.2;
        }
        else if (currentDirectionFlag == 0){
            AhData.absIntegratedCurent[i] += 0.001 * current_c * 0.2;
        }
        else{
            AhData.absIntegratedCurent[i] += 0;
        }
    }

}

/*
 * @brief Function used to get current DOD value
 */
static void getCurrentDOD(void)
{
	float deltaDOD[BATTERY_NUMBER];
	int i;

	for (i = 0; i < BATTERY_NUMBER; i++){

		deltaDOD[i] = AhData.integratedCurrent[i] * 1000 / (RATEDCAPACITANCE * 3600);

        if (currentDirectionFlag == 0){
            AhData.DOD_c[i] = AhData.DOD_0[i] + deltaDOD[i]; // Discharge DOD
        }
        else{
            AhData.DOD_c[i] = AhData.DOD_0[i] + deltaDOD[i]; // Charge DOD
        }
	}
}

/*
 * @brief Function used to get current SOC value
 */
static void getCurrentSOC(void)
{
	int i;

	for (i = 0; i < BATTERY_NUMBER; i++){
		AhData.SOC_c[i] = AhData.SOH[i] - AhData.DOD_c[i];
	}
}

/*
 * @brief Function used to get integrated current value based on SOC value
 */
static void updateIntegratedCurrent(int16_t SoC, int8_t cellIndex)
{
	int16_t changedSoC;

	changedSoC = AhData.SOC_0[cellIndex] - SoC;

	// Integrated current in A*s = changedSoC (in permille) / 1000  * 3600 (change to As)
	AhData.integratedCurrent[cellIndex] = changedSoC * 0.001 * RATEDCAPACITANCE * 3600;
	AhData.absIntegratedCurent[cellIndex] = changedSoC * 0.001 * RATEDCAPACITANCE * 3600;
}

/*!
 * @brief Function used for sorting the cell voltage as well as cell number
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

/*!
 * @brief Function used for cell balancing
 */
static void cellBalancing(void)
{
    uint8_t balancingCellNumber = 0; // Number of cells require balancing
    uint16_t balanceTime = BALANCE_TIME; // Balancing time in minute
#ifdef CELL14
    uint32_t cellVoltage[BATTERY_NUMBER]; // Cell voltages for 14 cells
    uint8_t cellLabel[BATTERY_NUMBER]; // Cell number label
#else
    uint32_t cellVoltage[7];
    uint8_t cellLabel[7]; // Cell number label
#endif

    uint8_t i;

    cellBalancingSoCUpdateFlag = true;

#ifdef CELL14
    for(i = 0; i < BATTERY_NUMBER; i++){
        cellVoltage[i] = cellData[i + 1];
        cellLabel[i] = i;
    }
    bubbleSort(cellVoltage, cellLabel, BATTERY_NUMBER);

	if((cellVoltage[BATTERY_NUMBER - 1] - cellVoltage[0]) > VOLTAGE_DIFFERENCE_THRESHOLD){
		BCC_CB_Enable(&drvConfig, BCC_CID_DEV1, true);

		for(i = BATTERY_NUMBER - 1; i > 0; i--){
			if((cellVoltage[i] - cellVoltage[0]) > VOLTAGE_DIFFERENCE_THRESHOLD){
				balancingCellNumber++;
			}

			if((balancingCellNumber <= MAX_BALANCED_CELL_NUMBER) && ((BATTERY_NUMBER - i) <= balancingCellNumber)){
				BCC_CB_SetIndividual(&drvConfig, BCC_CID_DEV1, cellLabel[i], true, balanceTime);
			}
		}
	}
	else{
		BCC_CB_Enable(&drvConfig, BCC_CID_DEV1, false);
	}
#else
	cellVoltage[0] = cellData[1];
	cellVoltage[1] = cellData[2];
	cellVoltage[2] = cellData[3];
	cellVoltage[3] = cellData[4];
	cellVoltage[4] = cellData[12];
	cellVoltage[5] = cellData[13];
	cellVoltage[6] = cellData[14];

	cellLabel[0] = 0;
	cellLabel[1] = 1;
	cellLabel[2] = 2;
	cellLabel[3] = 3;
	cellLabel[4] = 11;
	cellLabel[5] = 12;
	cellLabel[6] = 13;

    bubbleSort(cellVoltage, cellLabel, 7);

	if((cellVoltage[6] - cellVoltage[0]) > VOLTAGE_DIFFERENCE_THRESHOLD){
		BCC_CB_Enable(&drvConfig, BCC_CID_DEV1, true);

		for(i = 6; i > 0; i--){
			if((cellVoltage[i] - cellVoltage[0]) > VOLTAGE_DIFFERENCE_THRESHOLD){
				balancingCellNumber++;
			}

			if((balancingCellNumber <= MAX_BALANCED_CELL_NUMBER) && ((7 - i) <= balancingCellNumber)){
				BCC_CB_SetIndividual(&drvConfig, BCC_CID_DEV1, cellLabel[i], true, balanceTime);
			}
		}
	}
	else{
		BCC_CB_Enable(&drvConfig, BCC_CID_DEV1, false);
	}
#endif
}

/*!
 * @brief Function used for cell balancing control
 */
static void cellBalancingControl(void)
{
	uint8_t cellIndex;
	uint16_t readVal;
	int16_t SoC;

	// Read cell balancing status registers
	BCC_Reg_Read(&drvConfig, BCC_CID_DEV1, MC33771C_CB_DRV_STS_OFFSET, 1U, &readVal);

	for(cellIndex = 0; cellIndex < BATTERY_NUMBER; cellIndex++){
		AhData.CB_ControlStatus[cellIndex] = (readVal & (1 << cellIndex)) >> cellIndex;
	}

	if(balanceTimeout < 0){
		for(cellIndex = 0; cellIndex < BATTERY_NUMBER; cellIndex++){
			getSOCResult(cellData[cellIndex + 1],&SoC); // Update SoC value when the balancing is stopped
			AhData.SOC_c[cellIndex] = SoC;
			updateIntegratedCurrent(SoC, cellIndex);
		}
	}

    /*
     * If the batteries had rested, start the next balancing round
    */
	if(balanceTimeout >= (BALANCE_TIME * 60 * 1000 + REST_TIME)){ // If the balancing process is ended and the battery is rested
		balanceTimeout = 0; // Reset balance time out to 0

		if((cellBalancingFlag == false) && (cellBalancingSoCUpdateFlag == true)){
			balanceTimeout = BALANCEING_SOC_CALIBRATE_TIME; // Set two mins rest time
		}

		if(cellBalancingSoCUpdateFlag == true){
			for(cellIndex = 0; cellIndex < BATTERY_NUMBER; cellIndex++){
				getSOCResult(cellData[cellIndex + 1],&SoC); // Update SoC value
				AhData.SOC_c[cellIndex] = SoC;
				updateIntegratedCurrent(SoC, cellIndex);
			}
			cellBalancingSoCUpdateFlag = false;
		}

		if(cellBalancingFlag == true){
			cellBalancing();
		}
    }
}

/*
 * @brief Handler for discharge state
 */
static void DischargeHandler(void)
{
#ifdef CELL7
	int8_t cellNumber = 7;
#else
	int8_t cellNumber = 14;
#endif
    int16_t i;
    int16_t flag;
    BCC_CB_Enable(&drvConfig, BCC_CID_DEV1, false);
    for (i = 0; i < BATTERY_NUMBER; i++){
    	// 200mV margin
        if (cellData[i + 1] <= (MC33771C_TH_ALL_CT_UV_TH + 200 + 200) * 1000){
        	// DoD is equal to the maximum releasable capacity
            AhData.SOH[i] = AhData.DOD_c[i];
            // When the cell is fully discharged, the SoC is 0, DoD is not 0
            AhData.SOC_c[i] = 0;
            flag = 1;
        }
        else{
        	flag = 0;
        }
    }

    if ((flag == 0) && (cellData[0] >= (MC33771C_TH_ALL_CT_UV_TH + 200 + 202) * 1000 * cellNumber)){
    	// 202mV margin
    	integrateCurrent();
		getCurrentDOD();
		getCurrentSOC();
    }
}

/*
 * @brief Handler for charge state
 */
static void ChargeHandler(void)
{
    int16_t i;
    int16_t flag;
    BCC_CB_Enable(&drvConfig, BCC_CID_DEV1, false);
    for (i = 0; i < BATTERY_NUMBER; i++){
    	// 0.5mV margin between switching states
        if ((cellData[i + 1] >= (MC33771C_TH_ALL_CT_OV_TH - 300) * 1000) && (-isenseVolt <= ISENSETHRESHOLD + 500)){
        	// Calibrate SOH for each cell
            AhData.SOH[i] = AhData.SOC_c[i] - AhData.DOD_c[i];
            // SoC equals to SoH
            AhData.SOC_c[i] = AhData.SOH[i];
            // When the battery is fully charged, the DoD is 0
            AhData.DOD_c[i] = 0;

            flag = 1;
        }
        else{
        	flag = 0;
        }
    }

    // 2.5mV margin added between calibration and DoC and SoC calculation
    if ((flag == 0) && (-isenseVolt > ISENSETHRESHOLD + 2500)){
    	integrateCurrent();
		getCurrentDOD();
		getCurrentSOC();
    }
}

/*
 * @brief Handler for open circuit state calculation
 */
static void OpenCircuitHandler(void)
{
	uint8_t cellIndex;

	if (EFCFlag == 0){
        EFCFlag = 1;
        AhData.efcCounter += AhData.absIntegratedCurent[1] / (2 * RATEDCAPACITANCE * 3600);

		// Update the SoH of each cell based on EFC
		for(cellIndex = 0; cellIndex < BATTERY_NUMBER; cellIndex++){
			AhData.SOH[cellIndex] -= (AhData.absIntegratedCurent[cellIndex] / (2 * RATEDCAPACITANCE*3600)) / CYCLELIFE * 1000;
			AhData.absIntegratedCurent[cellIndex] = 0.0;
		}
    }

    cellBalancingControl();
}

/*
 * @brief Handler for fault state
 */
static bmsSystemState FaultHandler(void)
{
	uint8_t i;
	uint8_t cellIndex;
	uint16_t readVal;

	// Turn off cell balancing
	BCC_CB_Enable(&drvConfig, BCC_CID_DEV1, false);

	// Read cell balancing status registers
	BCC_Reg_Read(&drvConfig, BCC_CID_DEV1, MC33771C_CB_DRV_STS_OFFSET, 1U, &readVal);

	for(cellIndex = 0; cellIndex < BATTERY_NUMBER; cellIndex++){
		AhData.CB_ControlStatus[cellIndex] = (readVal & (1 << cellIndex)) >> cellIndex;
	}

	// Open relay
	PINS_DRV_ClearPins(RELAY_PORT, 1U << RELAY_PIN);

	if(PTC->PDIR & (1<<12)){
		clearFaultRegs();
		PINS_DRV_SetPins(RELAY_PORT, 1U << RELAY_PIN);
		for (i = 0; i < 2; i++){
			faultStatusValue[i] = 0;
		}
		return Idle_State;
	}
	return Fault_State;
}

/*
 * @brief Handler for battery monitoring
 */
static bmsSystemEvent monitorBattery(void)
{
    updateMeasurements();
    updateFaultStatus();

	if (faultStatusValue[0] > 0 || faultStatusValue[1] > 0){
		return Fault_Event;
	}
	else{
	    if (currentDirectionFlag == 0){
	        return Discharge_Event;
	    }
	    else if (currentDirectionFlag == 1){
	        return Charge_Event;
	    }
	    else{
	        return OpenCircuit_Event;
	    }
	}
}

/*
 * @brief Function used to transmit data
 */
void dataTransmit(bmsSystemState bmsNextState)
{
    int16_t i;

    /* Rearrange data */
    for (i = 0; i < 17; i++){
        transmittedData[i] = cellData[i]; // Cell data
    }

    for (i = 17; i < 31; i++){
        transmittedData[i] = AhData.SOC_c[i - 17]; // SOC data
    }

    for (i = 31; i < 45; i++){
        transmittedData[i] = AhData.SOH[i - 31]; // SOH data
    }

    transmittedData[45] = (uint32_t)round(AhData.efcCounter); // Round the EFC number

    for (i = 46; i < 60; i++){
        transmittedData[i] = AhData.CB_ControlStatus[i - 46]; // CB control data
    }

    transmittedData[60] = bmsNextState;

    transmittedData[61] = cellBalancingFlag;

    LPUART_DRV_SendData(INST_LPUART1, (uint8_t *)transmittedData, sizeof(transmittedData)); // Transmit the data through UART
}

/*!
 * @brief This function reads summary fault status registers of BCC
 * device via SPI.
 *
 * @return bcc_status_t Error code.
 */
static bcc_status_t updateFaultStatus(void)
{
    bcc_status_t error;
    uint16_t faultStatus[BCC_STAT_CNT];

    error = BCC_Fault_GetStatus(&drvConfig, BCC_CID_DEV1, faultStatus);
    if (error != BCC_STATUS_SUCCESS)
    {
        return error;
    }

    faultStatusValue[0] = faultStatus[BCC_FS_CELL_OV];
    faultStatusValue[1] = faultStatus[BCC_FS_CELL_UV];

    return BCC_STATUS_SUCCESS;
}

/*
 * @brief Function used for status display
 */
static void displayStatus(bmsSystemState bmsNextState)
{
    switch(bmsNextState){
    case Idle_State:
                        {
                            PINS_DRV_SetPins(RED_LED_PORT, 1U << RED_LED_PIN);
                            PINS_DRV_SetPins(BLUE_LED_PORT, 1U << BLUE_LED_PIN);
                            PINS_DRV_SetPins(GREEN_LED_PORT, 1U << GREEN_LED_PIN);
                        }
                        break;
    case Discharge_State:
                        {
                            PINS_DRV_SetPins(RED_LED_PORT, 1U << RED_LED_PIN);
                            PINS_DRV_SetPins(BLUE_LED_PORT, 1U << BLUE_LED_PIN);
                            PINS_DRV_SetPins(GREEN_LED_PORT, 1U << GREEN_LED_PIN);

                            PINS_DRV_ClearPins(GREEN_LED_PORT, 1U << GREEN_LED_PIN);
                        }
                        break;
    case Charge_State:
                        {
                            PINS_DRV_SetPins(RED_LED_PORT, 1U << RED_LED_PIN);
                            PINS_DRV_SetPins(BLUE_LED_PORT, 1U << BLUE_LED_PIN);
                            PINS_DRV_SetPins(GREEN_LED_PORT, 1U << GREEN_LED_PIN);

                            PINS_DRV_ClearPins(BLUE_LED_PORT, 1U << BLUE_LED_PIN);
                        }
                        break;
    case OpenCircuit_State:
                        {
                            PINS_DRV_SetPins(RED_LED_PORT, 1U << RED_LED_PIN);
                            PINS_DRV_SetPins(BLUE_LED_PORT, 1U << BLUE_LED_PIN);
                            PINS_DRV_SetPins(GREEN_LED_PORT, 1U << GREEN_LED_PIN);

                            PINS_DRV_ClearPins(RED_LED_PORT, 1U << RED_LED_PIN);
                            PINS_DRV_ClearPins(BLUE_LED_PORT, 1U << BLUE_LED_PIN);
                            PINS_DRV_ClearPins(GREEN_LED_PORT, 1U << GREEN_LED_PIN);
                        }
                        break;
    case Fault_State:
                        {
                            PINS_DRV_SetPins(RED_LED_PORT, 1U << RED_LED_PIN);
                            PINS_DRV_SetPins(BLUE_LED_PORT, 1U << BLUE_LED_PIN);
                            PINS_DRV_SetPins(GREEN_LED_PORT, 1U << GREEN_LED_PIN);

                            PINS_DRV_ClearPins(RED_LED_PORT, 1U << RED_LED_PIN);
                        }
    }
}

/*
* @brief Function used for status display
*/
void communicateWithPc(bmsSystemState bmsNextState)
{
    /* Declare a buffer used to store the received data */

    LPUART_DRV_ReceiveData(INST_LPUART1, receivedBuffer, 5U);

    dataTransmit(bmsNextState);

    if(strcmp((char *)receivedBuffer, "OPEN\t") == 0)
    {
        cellBalancingFlag = true;
    }
    else if(strcmp((char *)receivedBuffer, "OVER\t") == 0)
    {
        cellBalancingFlag = false;
    }
    else
    {
    	receivedBuffer[bufferIdx] = '\n';
        bufferIdx++;
        /* Append string terminator to the received data */
        receivedBuffer[bufferIdx] = 0U;
    }

    /* Reset the buffer index to start a new reception */
    bufferIdx = 0U;
}

int main(void)
{
  /* Write your local variable definition here */
	bmsSystemState bmsNextState = Idle_State;

  /*** Processor Expert internal initialization. DON'T REMOVE THIS CODE!!! ***/
  #ifdef PEX_RTOS_INIT
    PEX_RTOS_INIT();                   /* Initialization of the selected RTOS. Macro is defined by the RTOS component. */
  #endif
  /*** End of Processor Expert internal initialization.                    ***/

  /* Write your code here */
  /* For example: for(;;) { } */
  if (initAlgorithm() == STATUS_SUCCESS) // Initialize peripherals
  {
      /* Get the initial value of SoC through lookup table */
      initAlgorithmValues();

      /* Infinite loop for the real-time processing routines. */
      while (1)
      {
    	  /* The initial timeout value is set to 200, since the lpit period is set to 1000 (1ms)
    	   * 200*1ms = 200ms, so the do while will be ended every 200ms
    	   */
          initTimeout(196);
        
          if (PTC->PDIR & (1<<12)){ /* If Pad Data Input = 1 (BTN0 [SW2] pushed) */
              EFCFlag = 0; /* Reset EFC flag */
              balanceTimeout = 0;

              // Turn off the LED for a short period to represent that the data has cleared
  	  		  PINS_DRV_SetPins(RED_LED_PORT, 1U << RED_LED_PIN);
  	  		  PINS_DRV_SetPins(BLUE_LED_PORT, 1U << BLUE_LED_PIN);
  	  		  PINS_DRV_SetPins(GREEN_LED_PORT, 1U << GREEN_LED_PIN);
          }

          // Read system Events
          bmsSystemEvent bmsNewEvent = monitorBattery();
          /* Loops until specified timeout expires, loop ends every 200ms */
          do
          {
        	  displayStatus(bmsNextState);

              if (!sleepMode)
              {
                  /* To prevent communication loss */
                  if (BCC_SendNop(&drvConfig, BCC_CID_DEV1) != BCC_STATUS_SUCCESS)
                  {
                	  PINS_DRV_ClearPins(RED_LED_PORT, 1U << RED_LED_PIN);
                  }
              }
          } while (timeoutExpired() == false);

          if (!sleepMode)
          {
              switch(bmsNextState)
                {
                case Idle_State:
                {
                    if (bmsNewEvent == Discharge_Event)
                    {
                        bmsNextState = Discharge_State;
                        DischargeHandler();
                    }
                    else if (bmsNewEvent == Charge_Event)
                    {
                        bmsNextState = Charge_State;
                        ChargeHandler();
                    }
                    else if (bmsNewEvent == OpenCircuit_Event)
                    {
                        bmsNextState = OpenCircuit_State;
                        OpenCircuitHandler();
                    }
                    else if (bmsNewEvent == Fault_Event)
					{
						bmsNextState = FaultHandler();
					}
                }
                break;

                case Discharge_State:
                {
                    DischargeHandler();

                    if(bmsNewEvent == Charge_Event)
                    {
                        bmsNextState = Charge_State;
                    }
                    else if (bmsNewEvent == OpenCircuit_Event)
                    {
                        bmsNextState = OpenCircuit_State;
                    }
                    else if (bmsNewEvent == Fault_Event)
					{
						bmsNextState = Fault_State;
					}
                }
                break;

                case Charge_State:
                {
                    ChargeHandler();

                    if(bmsNewEvent == Discharge_Event)
                    {
                        bmsNextState = Discharge_State;
                    }
                    else if (bmsNewEvent == OpenCircuit_Event)
                    {
                        bmsNextState = OpenCircuit_State;
                    }
                    else if (bmsNewEvent == Fault_Event)
					{
						bmsNextState = Fault_State;
					}
                }
                break;

                case OpenCircuit_State:
                {
                    OpenCircuitHandler();

                    if(bmsNewEvent == Charge_Event)
                    {
                        bmsNextState = Charge_State;
                    }
                    else if (bmsNewEvent == Discharge_Event)
                    {
                        bmsNextState = Discharge_State;
                    }
                    else if (bmsNewEvent == Fault_Event)
					{
						bmsNextState = Fault_State;
					}
                }
                break;

                case Fault_State:
				{
					bmsNextState = FaultHandler();
				}
                break;

                default:
                    break;
                }

                communicateWithPc(bmsNextState);
                //resetData();
          }
      }
  }
  else
  {
	  PINS_DRV_ClearPins(RED_LED_PORT, 1U << RED_LED_PIN);
  }
  /*** Don't write any code pass this line, or it will be deleted during code generation. ***/
  /*** RTOS startup code. Macro PEX_RTOS_START is defined by the RTOS component. DON'T MODIFY THIS CODE!!! ***/
  #ifdef PEX_RTOS_START
    PEX_RTOS_START();                  /* Startup of the selected RTOS. Macro is defined by the RTOS component. */
  #endif
  /*** End of RTOS startup code.  ***/
  /*** Processor Expert end of main routine. DON'T MODIFY THIS CODE!!! ***/
  for(;;) {
    if(exit_code != 0) {
      break;
    }
  }
  return exit_code;
  /*** Processor Expert end of main routine. DON'T WRITE CODE BELOW!!! ***/
} /*** End of main routine. DO NOT MODIFY THIS TEXT!!! ***/

/* END main */
/*!
** @}
*/
/*
** ###################################################################
**
**     This file was created by Processor Expert 10.1 [05.21]
**     for the NXP S32K series of microcontrollers.
**
** ###################################################################
*/
