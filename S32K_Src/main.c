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
** @version 03.00
** @brief
**         Main module.
**         Enhanced CC method.
*/         
/*!
**  @addtogroup main_module main module documentation
**  @{
*/
/*
 * Copyright 2016 - 2020 NXP
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 *
 * o Redistributions of source code must retain the above copyright notice, this list
 *   of conditions and the following disclaimer.
 *
 * o Redistributions in binary form must reproduce the above copyright notice, this
 *   list of conditions and the following disclaimer in the documentation and/or
 *   other materials provided with the distribution.
 *
 * o Neither the name of the copyright holder nor the names of its
 *   contributors may be used to endorse or promote products derived from this
 *   software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
 * ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
 * ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

/* MODULE main */


/* Including necessary module. Cpu.h contains other modules needed for compiling.*/
#include "Cpu.h"

  volatile int exit_code = 0;

/* User includes (#include below this line is not maintained by Processor Expert) */
#include <math.h>
#include "bcc/bcc.h"
#include "bcc_s32k144/bcc_wait.h"
#include "common.h"

/*******************************************************************************
* Definitions
******************************************************************************/

/* Red on-board LED. */
#define RED_LED_PORT         PTD
#define RED_LED_PIN          15U

/* LPSPI_TX configuration. */
#define BCC_TX_LPSPI_DELAY_PCS_TO_SCLK         3U  /* 3us (f >= 1.75us) */
#define BCC_TX_LPSPI_DELAY_SCLK_TO_PCS         1U  /* 1us (g >= 0.60us) */
#define BCC_TX_LPSPI_DELAY_BETWEEN_TRANSFERS   5U  /* 5us (t_MCU_RES >= 4us) */

/* Used channel of LPIT0 for GUI timing. */
#define LPIT0_CHANNEL_TYPGUI  0U

/* Used channel of LPIT0 for BCC SW driver timing. */
#define LPIT0_CHANNEL_BCCDRV   3U

/* Battery rated capacitance */
#define RATEDCAPACITANCE 0.5

/* The minimum value of OCV */
#define OCV_MINSOC          0

/* The maximum value of OCV */
#define OCV_MAXSOC          1000 // 100 permille

/* The size of the lookup table*/
#define OCV_TABLE_SIZE      (OCV_MAXSOC - OCV_MINSOC + 1) // 1000 sets of data in the lookupTable

/* Operation efficiency */
#define KC 1 // Charging efficiency
#define KD 1 // Discharging efficiency

/* Battery minimum and maximum voltages */
#define MIN_VOLTAGE 3000000 // In micro volt
#define MAX_VOLTAGE 4200000 // In micro volt

/*******************************************************************************
* Enum definition
******************************************************************************/
//Different state of bms system
typedef enum
{   
    Idle_State,
    Charge_State,
    Discharge_State,
    OpenCircuit_State
} bmsSystemState;

//Different type events
typedef enum
{
    Discharge_Event,
    Charge_Event,
    OpenCircuit_Event
} bmsSystemEvent;

/*******************************************************************************
* Structure definition
******************************************************************************/

typedef struct
{
	int16_t SOC_0[14]; // Initial SoC value: 100 permille

	int16_t SOC_c[14]; // Current SoC value: 100 permille

    int16_t DOD_0[14]; // Inital depth of Discharge: 100 permille

    int16_t DOD_c[14]; // Current depth of Discharge: 100 permille

    int16_t SOH[14]; // State of health: 100 permille

	double integratedCurrent; // The integral value of current: A*s
} Ah_integral_data;

/* Define a struct used in OCV_SOC lookup table */
typedef struct
{
    double coefficient_4th; // 4th order coefficient

    double coefficient_3rd; // 3rd order coefficient

    double coefficient_2nd; // 2nd order coefficient

    double coefficient_1st; // 1st order coefficient

    double constant; // constant value
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
/* Final transmitted data */
/*
 * [0] Pack voltge
 * [1:14] Cell voltage 1 to 14
 * [15] IC temperature
 * [16] Current
 * [17:30] SOC: Cell 1 to 14
 * [31:44] SOH: Cell 1 to `4
 */
uint32_t transmittedData[45];

/* BCC driver configuration. */
bcc_drv_config_t drvConfig;

/* Array used in UART communication */
uint32_t cellData[17];

/* Array needed to store all measured values. */
uint16_t measurements[BCC_MEAS_CNT];

/* Ah intergal data*/
Ah_integral_data AhData;

/* The OCV-SOC lookup table */
uint32_t g_ocvTable[OCV_TABLE_SIZE];

/* State variable (used as indication if SPI is accessible or not). */
bool sleepMode = false;

/* Timeout value of the lpit */
int32_t timeout = 0;

/* Current direction flag: 0 is discharge, 1 is charge */
int16_t currentDirectionFlag = 0;

/*******************************************************************************
 * Function prototypes
 ******************************************************************************/

static bcc_status_t initRegisters(void);
static bcc_status_t clearFaultRegs(void);

static void initTimeout(int32_t timeoutMs);
static bool timeoutExpired(void);

static void fillOcvTable(const ocv_config_t* const ocvConfig);
static void getSOCResult(uint32_t cellVoltage, int16_t *soc);

static status_t initDemo(void);
static bcc_status_t Ah_integral_initialize(void);

static bcc_status_t updateMeasurements(void);

static void Ah_integral_step(void);

static void getCurrentDOD(void);
static void getCurrentSOC(void);

static void DischargeHandler(void);
static void ChargeHandler(void);
static void OpenCircuitHandler(void);

static bmsSystemEvent monitorBattery(void);

static void dataTransmit(void);
static void resetData(void);

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
    double term_1, term_2, term_3, term_4, sum;

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
static bcc_status_t Ah_integral_initialize(void)
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
	if (currentDirectionFlag == 0){ 
        // Discharge
		ocvConfig.coefficient_4th = -6.539e-08;
		ocvConfig.coefficient_3rd = 1.512e-05;
		ocvConfig.coefficient_2nd = -0.001177;
		ocvConfig.coefficient_1st = 0.04344;
		ocvConfig.constant = 3.006;
	}
	else{ 
        // Charge
		ocvConfig.coefficient_4th = -6.884e-08;
		ocvConfig.coefficient_3rd = 1.577e-05;
		ocvConfig.coefficient_2nd = -0.00121;
		ocvConfig.coefficient_1st = 0.04339;
		ocvConfig.constant = 3.044;
	}

	/* Initialize the OCV-SOC look up table */
	fillOcvTable(&ocvConfig);

	for (i = 0; i < 14; i++){
		/* Get the initial SOC value */
		getSOCResult(cellData[i + 1],&soc);
		AhData.SOC_0[i] = soc;
        
        AhData.SOH[i] = 1000; // Assume the initial health is 100%

        /* Calculate the initial DOD value */
        AhData.DOD_0[i] = 1000 - AhData.SOC_0[i];
        AhData.DOD_c[i] = 1000 - AhData.SOC_0[i];
	}
    
    AhData.integratedCurrent = 0.0;

	return BCC_STATUS_SUCCESS;
}

/*!
 * @brief MCU and BCC initialization.
 */
static status_t initDemo(void)
{
    status_t status;
    bcc_status_t bccStatus;

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

    /* Initialize BCC driver configuration structure. */
    drvConfig.drvInstance = 0U;
    drvConfig.commMode = BCC_MODE_SPI;
    drvConfig.devicesCnt = 1U;
    drvConfig.device[0] = BCC_DEVICE_MC33771C;
    drvConfig.cellCnt[0] = 14U;
    drvConfig.loopBack = false;

    LPIT_DRV_StartTimerChannels(INST_LPIT1, (1 << LPIT0_CHANNEL_TYPGUI));

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
    int16_t currentValue; // In mA with sign

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

	/* ISENCE data (current measurement) */
	cellData[16] = BCC_GET_ISENSE_AMP(DEMO_RSHUNT, measurements[BCC_MSR_ISENSE1], measurements[BCC_MSR_ISENSE2]);

	currentValue = cellData[16];
	if (currentValue >= 0){
		currentDirectionFlag = 0; // Discharge
	}
	else{
		currentDirectionFlag = 1; // Charge
	}

	return BCC_STATUS_SUCCESS;
}

/*!
 * @brief Model step function 
 */
void Ah_integral_step(void)
{
    int32_t current_c; // Current current

    current_c = cellData[16];

	AhData.integratedCurrent += 0.001 * current_c * 0.2; //convert to 1A, and 200ms = 0.2s
}

/*
 * @brief Function used to get current DOD value
 */
static void getCurrentDOD(void)
{
	double deltaDOD;
	int i;

	deltaDOD = AhData.integratedCurrent / (RATEDCAPACITANCE * 3600.0) * 1000;
    
	for (i = 0; i < 14; i++){
        if (currentDirectionFlag == 0){
            AhData.DOD_c[i] = AhData.DOD_0[i] + KD * deltaDOD; // Discharge DOD
        }
        else{
            AhData.DOD_c[i] = AhData.DOD_0[i] + KC * deltaDOD; // Charge DOD
        }
	}
}

/*
 * @brief Function used to get current SOC value
 */
static void getCurrentSOC(void)
{
	int i;

	for (i = 0; i < 14; i++){
		AhData.SOC_c[i] = AhData.SOH[i] - AhData.DOD_c[i];
	}
}

/*
 * @brief Handler for discharge state
 */
static void DischargeHandler(void)
{
    int16_t i;
    int16_t flag;

    for (i = 0; i < 14; i++){
        if (cellData[i + 1] <= MIN_VOLTAGE){
            AhData.SOH[i] = AhData.DOD_c[i]; // Calibrate SOH for each cell
            flag = 1;
        }
        else{
        	flag = 0;
        }
    }
    if (flag == 0){
    	Ah_integral_step();
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

    for (i = 0; i < 14; i++){
        if (cellData[i + 1] >= MAX_VOLTAGE){
            AhData.SOH[i] = AhData.SOC_c[i] - AhData.DOD_c[i];
            AhData.DOD_c[i] = 0.0;
        }
        else{
        	flag = 0;
        }
    }
    if (flag == 0){
    	Ah_integral_step();
		getCurrentDOD();
		getCurrentSOC();
    }
}

/*
 * @brief Handler for open circuit state
 */
static void OpenCircuitHandler(void)
{
    // Compensation of self-discharging loss
    BCC_SendNop(&drvConfig, BCC_CID_DEV1);
}

/*
 * @brief Handler for battery monitoring
 */
static bmsSystemEvent monitorBattery(void)
{
    updateMeasurements();

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

/*
 * @brief Function used to transmit data
 */
void dataTransmit(void)
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

    LPUART_DRV_SendData(INST_LPUART1, (uint8_t *)transmittedData, sizeof(transmittedData)); // Transmit the data through UART
}

/*
 * @brief Function used to reset data
 */
static void resetData(void){
    int16_t i;

    for (i = 0; i < 14; i++){
        AhData.DOD_c[i] = AhData.DOD_0[i];
    }
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
  PINS_DRV_SetPins(RED_LED_PORT, 1U << RED_LED_PIN);

  if (initDemo() == STATUS_SUCCESS) // Initialize peripherals
  {
      /* Get the initial value of SoC through lookup table */
      Ah_integral_initialize();

      /* Infinite loop for the real-time processing routines. */
      while (1)
      {
    	  /* The initial timeout value is set to 200, since the lpit period is set to 1000 (1ms)
    	   * 200*1ms = 200ms, so the do while will be ended every 200ms
    	   */
          initTimeout(200);
        
          //Read system Events
          bmsSystemEvent bmsNewEvent = monitorBattery();

          /* Loops until specified timeout expires. */
          do
          {
        	  PINS_DRV_TogglePins(RED_LED_PORT, 1U << RED_LED_PIN);

              if (!sleepMode)
              {
                  /* To prevent communication loss. */
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
                    if (Discharge_Event == bmsNewEvent)
                    {
                        bmsNextState = Discharge_State;
                        DischargeHandler();
                    }
                    else if (Charge_Event == bmsNewEvent)
                    {
                        bmsNextState = Charge_State;
                        ChargeHandler();
                    }
                    else if (OpenCircuit_Event == bmsNewEvent)
                    {
                        bmsNextState = OpenCircuit_State;
                        OpenCircuitHandler();
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
                }
                break;

                default:
                    break;
                }
                
                dataTransmit();
                resetData();
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
