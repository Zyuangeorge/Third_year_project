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

/*!
** @file main.c
** @version 01.00
** @brief
**         Main module.
**         This module contains user's application code.
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
/*This project include components:
    1. LPSPI
    2. LPuart
    3. LPIT
*/

#include <math.h>
/* Include bcc basic functions */
#include "bcc/bcc.h"
/* Include bcc communication delays */
#include "bcc_s32k144/bcc_wait.h"
/* Set up communication registers */
#include "common.h"

#include "S32K144.h"
/* Definitions */

/* LED definitions */
#define RED_LED_PORT PTD
#define RED_LED_PIN 15U

#define BLUE_LED_PORT PTD
#define BLUE_LED_PIN 0U

/* LPSPI_TX delay configuration */
#define BCC_TX_LPSPI_DELAY_PCS_TO_SCLK 3U
#define BCC_TX_LPSPI_DELAY_SCLK_TO_PCS 1U
#define BCC_TX_LPSPI_DELAY_BETWEEN_TRANSFERS 5U

/* Used channel of LPIT0 for TYP_GUI timing. */
#define LPIT0_CHANNEL_TYP_GUI 0U

/* Used channel of LPIT0 for BCC SW driver timing. */
#define LPIT0_CHANNEL_BCCDRV 3U

/* NTC precomputed table configuration. */
/*! @brief Minimal temperature in NTC table.
 *
 * It directly influences size of the NTC table (number of precomputed values).
 * Specifically lower boundary.
 */
#define NTC_MINTEMP (-40)

/*! @brief Maximal temperature in NTC table.
 *
 * It directly influences size of the NTC table (number of precomputed values).
 * Specifically higher boundary.
 */
#define NTC_MAXTEMP (120)

/*! @brief Size of NTC look-up table. */
#define NTC_TABLE_SIZE (NTC_MAXTEMP - NTC_MINTEMP + 1)

/*! @brief 0 degree Celsius converted to Kelvin. */
#define NTC_DEGC_0 273.15

/*!
 * @brief Calculates final temperature value.
 *
 * @param tblIdx Index of value in NTC table which is close
 *        to the register value provided by user.
 * @param degTenths Fractional part of temperature value.
 * @return Temperature.
 */
#define NTC_COMP_TEMP(tblIdx, degTenths) \
    ((((tblIdx) + NTC_MINTEMP) * 10) + (degTenths))

/* Define GPIOs and CTx constants that are used in setting threshold values */
typedef enum
{
    TH_GPIOx_OT = 0, /* Common GPIOx in analog input mode, overtemperature threshold. */
    TH_GPIOx_UT = 1, /* Common GPIOx in analog input mode, undertemperature threshold. */
    TH_CTx_OV = 2,   /* Common CTx overvoltage threshold. */
    TH_CTx_UV = 3    /* Common CTx undervoltage threshold. */
} threshSel_t;

/* Timeout in ms for blocking operations */
#define TIMEOUT     200U

/* Structure definition */
/*!
 * @brief NTC Configuration.
 *
 * The device has seven GPIOs which enable temperature measurement.
 * NTC thermistor and fixed resistor are external components and must be set
 * by the user. These values are used to calculate temperature. Beta parameter
 * equation is used to calculate temperature. GPIO port of BCC device must be
 * configured as Analog Input to measure temperature.
 * This configuration is common for all GPIO ports and all devices (in case of
 * daisy chain).
 */
typedef struct
{
    uint32_t beta;   /*!< Beta parameter of NTC thermistor in [K].
                          Admissible range is from 1 to 1000000. */
    uint32_t rntc;   /*!< R_NTC - NTC fixed resistance in [Ohm].
                          Admissible range is from 1 to 1000000. */
    uint32_t refRes; /*!< NTC Reference Resistance in [Ohm].
                          Admissible range is from 1 to 1000000. */
    uint8_t refTemp; /*!< NTC Reference Temperature in degrees [Celsius].
                          Admissible range is from 0 to 200. */
} ntc_config_t;

struct uart_transfer_status
{
    bcc_status_t bccStatus; /* bcc chip status */
	status_t uartStatus; /* uart transfer status */
};

/* Initial BCC configuration */

/*! @brief  Number of MC33771 registers configured in the initialization with
 * user values. */
#define BCC_INIT_CONF_REG_CNT 56U

/* Structure containing a register name and its address. */
/* This structure is used to configure the MC3371C registers */
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

/* Global variables */

bcc_drv_config_t drvConfig;          /* BCC driver configuration. */
uint16_t g_ntcTable[NTC_TABLE_SIZE]; /* NTC look-up table. */

int32_t thresholdsLast[TH_CTx_UV + 1] = {-1, -1, -1, -1};
bool cbIndividual[BCC_MAX_CELLS] = {false, false, false, false, false,
                                    false, false, false, false, false, false, false, false, false};
int32_t cbTimeoutLast = -1;
int32_t cbEnabledLast = -1;

/* Faults */
uint16_t faultStatus1;
uint16_t faultStatus2;
uint16_t faultStatus3;

/* State variable (used as indication if SPI is accessible or not). */
bool sleepMode = false;

int32_t timeout = 0;

/* Function prototypes */

/* Register handlers */
static bcc_status_t initRegisters();
static bcc_status_t clearFaultRegs();

/* Timeout handlers */
static void initTimeout(int32_t timeoutMs);
//static bool timeoutExpired(void);

/* Project initialisation */
static status_t initProject();

/* NTC handlers */
static void fillNtcTable(const ntc_config_t *const ntcConfig);

/* Update and transfer measurements */
struct uart_transfer_status updateMeasurements(void);
//static bcc_status_t updateFaultStatus(void);

/* Cell balancing timeout update */
/* Used in GUI control */
//static bcc_status_t updateCBTimeout(uint16_t cbTimeout);

/* Thresholds values update, used to control the temperature and voltage status update */
//static bcc_status_t updateThreshold(threshSel_t threshSel, uint16_t threshVal);

/* Functions */

/*!
 * @brief LPIT0 IRQ handler.
 */
void LPIT0_Ch0_IRQHandler(void)
{
    LPIT_DRV_ClearInterruptFlagTimerChannels(INST_LPIT1, (1 << LPIT0_CHANNEL_TYP_GUI));

    timeout--;
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
//static bool timeoutExpired(void)
//{
//    return (timeout <= 0);
//}

/*!
 * @brief Initializes BCC device registers according to BCC_INIT_CONF.
 * Registers having the wanted content already after POR are not rewritten.
 */
static bcc_status_t initRegisters()
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
static bcc_status_t clearFaultRegs()
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

/* MCU and BCC initialisation */
static status_t initProject()
{
    ntc_config_t ntcConfig;
    status_t status;
    bcc_status_t bccStatus;

    // Clock initialisation
    CLOCK_SYS_Init(g_clockManConfigsArr, CLOCK_MANAGER_CONFIG_CNT,
                   g_clockManCallbacksArr, CLOCK_MANAGER_CALLBACK_CNT);
    CLOCK_SYS_UpdateConfiguration(0U, CLOCK_MANAGER_POLICY_FORCIBLE);

    // Pin muxing, GPIO pin direction and initial value settings
    PINS_DRV_Init(NUM_OF_CONFIGURED_PINS, g_pin_mux_InitConfigArr);

    // Initialise LPUART instance
    status = LPUART_DRV_Init(INST_LPUART1, &lpuart1_State, &lpuart1_InitConfig0);
    if (status != STATUS_SUCCESS)
    {
        return STATUS_ERROR;
    }

    INT_SYS_EnableIRQ(LPUART1_RxTx_IRQn);

    /* Initialize LPIT instance */
    LPIT_DRV_Init(INST_LPIT1, &lpit1_InitConfig);
    status = LPIT_DRV_InitChannel(INST_LPIT1, LPIT0_CHANNEL_TYP_GUI, &lpit1_ChnConfig0);
    if (status != STATUS_SUCCESS)
    {
        return STATUS_ERROR;
    }
    LPIT_DRV_Init(INST_LPIT1, &lpit1_InitConfig);
    status = LPIT_DRV_InitChannel(INST_LPIT1, LPIT0_CHANNEL_BCCDRV, &lpit1_ChnConfig3);
    if (status != STATUS_SUCCESS)
    {
        return STATUS_ERROR;
    }

    /* Initialize LPSPI instance. */
    status = LPSPI_DRV_MasterInit(LPSPICOM1, &lpspiCom1State, &lpspiCom1_MasterConfig0);
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

    /* Precalculate NTC look up table for fast temperature measurement. */
    ntcConfig.rntc = 6800U;    /* NTC pull-up 6.8kOhm */
    ntcConfig.refTemp = 25U;   /* NTC resistance 10kOhm at 25 degC */
    ntcConfig.refRes = 10000U; /* NTC resistance 10kOhm at 25 degC */
    ntcConfig.beta = 3900U;

    fillNtcTable(&ntcConfig);

    LPIT_DRV_StartTimerChannels(INST_LPIT1, (1 << LPIT0_CHANNEL_TYP_GUI));

    /* Run initialisation functions */
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
 * @brief This function fills the NTC look up table.
 *
 * NTC look up table is intended for resistance to temperature conversion.
 * An array item contains raw value from a register. Index of the item is
 * temperature value.
 *
 * ArrayItem = (Vcom * Rntc) / (0.00015258789 * (NTC + Rntc))
 * Where:
 *  - ArrayItem is an item value of the table,
 *  - Vcom is maximal voltage (5V),
 *  - NTC is the resistance of NTC thermistor (Ohm),
 *  - 0.00015258789 is resolution of measured voltage in Volts
 *    (V = 152.58789 uV * Register_value),
 *  - Rntc is value of a resistor connected to Vcom (see MC3377x datasheet,
 *    section MC3377x PCB components).
 *
 * Beta formula used to calculate temperature based on NTC resistance:
 *   1 / T = 1 / T0 + (1 / Beta) * ln(Rt / R0)
 * Where:
 *  - R0 is the resistance (Ohm) at temperature T0 (Kelvin),
 *  - Beta is material constant (Kelvin),
 *  - T is temperature corresponding to resistance of the NTC thermistor.
 *
 * Equation for NTC value is given from the Beta formula:
 *   NTC = R0 * exp(Beta * (1/T - 1/T0))
 *
 * @param ntcConfig Pointer to NTC components configuration.
 */
void fillNtcTable(const ntc_config_t *const ntcConfig)
{
    double ntcVal, expArg;
    uint16_t i = 0;
    int32_t temp;

    for (temp = NTC_MINTEMP; temp <= NTC_MAXTEMP; temp++)
    {
        expArg = ntcConfig->beta * ((1.0 / (NTC_DEGC_0 + temp)) -
                                    (1.0 / (NTC_DEGC_0 + ntcConfig->refTemp)));
        ntcVal = exp(expArg) * ntcConfig->refRes;
        g_ntcTable[i] = (uint16_t)round((ntcVal /
                                         (ntcVal + ntcConfig->rntc)) *
                                        MC33771C_MEAS_AN0_MEAS_AN_MASK);
        i++;
    }
}

/*!
 * @brief This function reads values measured and provided via SPI
 * by BCC device (ISENSE, cell voltages, temperatures).
 *
 * @return uart_transfer_status Error code.
 */
struct uart_transfer_status updateMeasurements(void)
{
    struct uart_transfer_status error;
    uint16_t measurements[BCC_MEAS_CNT]; /* Array needed to store all measured values. */
    uint32_t cellData[16] = {0}; /* Array used in UART communication */

    /* Step 1: Start conversion and wait for the conversion time. */
    error.bccStatus = BCC_Meas_StartAndWait(&drvConfig, BCC_CID_DEV1, BCC_AVG_1);
    if (error.bccStatus != BCC_STATUS_SUCCESS)
    {
        return error;
    }

    /* Step 2: Convert raw measurements to appropriate units. */
    error.bccStatus = BCC_Meas_GetRawValues(&drvConfig, BCC_CID_DEV1, measurements);
    if (error.bccStatus != BCC_STATUS_SUCCESS)
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

	error.uartStatus = LPUART_DRV_SendDataBlocking(INST_LPUART1,(uint8_t *)cellData, sizeof(cellData), TIMEOUT);

	if (error.uartStatus != STATUS_SUCCESS)
	{
		return error;
	}

    return error;
}

/*!
 * @brief This function reads summary fault status registers of BCC
 * device via SPI.
 *
 * @return bcc_status_t Error code.
 */
//static bcc_status_t updateFaultStatus(void)
//{
//    bcc_status_t error;
//    uint16_t faultStatus[BCC_STAT_CNT];
//
//    error = BCC_Fault_GetStatus(&drvConfig, BCC_CID_DEV1, faultStatus);
//    if (error != BCC_STATUS_SUCCESS)
//    {
//        return error;
//    }
//
//    faultStatus1 = faultStatus[BCC_FS_FAULT1];
//    faultStatus2 = faultStatus[BCC_FS_FAULT2];
//    faultStatus3 = faultStatus[BCC_FS_FAULT3];
//
//    return BCC_STATUS_SUCCESS;
//}

/*!
 * @brief This function updates cell balancing timeout.
 *
 * @param cbTimeout Cell balancing timeout in range [0 - 511] minutes
 *
 * @return bcc_status_t Error code.
 */
//static bcc_status_t updateCBTimeout(uint16_t cbTimeout)
//{
//    bcc_status_t error;
//    uint8_t cellId;
//
//    /* Change timers. */
//    cbTimeoutLast = (int32_t)cbTimeout;
//    for (cellId = 0; cellId < BCC_MAX_CELLS; cellId++)
//    {
//        /* Turn cell balancing off. */
//        if (cbIndividual[cellId])
//        {
//            error = BCC_CB_SetIndividual(&drvConfig, BCC_CID_DEV1, cellId, false, cbTimeout);
//            if (error != BCC_STATUS_SUCCESS)
//            {
//                return error;
//            }
//        }
//
//        /* Update the CB interval. */
//        error = BCC_CB_SetIndividual(&drvConfig, BCC_CID_DEV1, cellId, cbIndividual[cellId], cbTimeout);
//        if (error != BCC_STATUS_SUCCESS)
//        {
//            return error;
//        }
//    }
//
//    return BCC_STATUS_SUCCESS;
//}

/*!
 * @brief This function updates internal device threshold.
 *
 * @param threshSel Selection of threshold to be updated.
 * @param threshVal New threshold value.
 *
 * @return bcc_status_t Error code.
 */
//static bcc_status_t updateThreshold(threshSel_t threshSel, uint16_t threshVal)
//{
//    bcc_status_t error;
//    uint8_t regAddr;
//
//    switch (threshSel)
//    {
//    case TH_GPIOx_OT:
//        thresholdsLast[TH_GPIOx_OT] = (int32_t)threshVal;
//        for (regAddr = MC33771C_TH_AN6_OT_OFFSET; regAddr <= MC33771C_TH_AN0_OT_OFFSET; regAddr++)
//        {
//            error = BCC_Reg_Update(&drvConfig, BCC_CID_DEV1, regAddr,
//                                   MC33771C_TH_AN1_OT_AN_OT_TH_MASK, MC33771C_TH_AN1_OT_AN_OT_TH(BCC_GET_TH_ANX(threshVal)));
//            if (error != BCC_STATUS_SUCCESS)
//            {
//                return error;
//            }
//        }
//        break;
//
//    case TH_GPIOx_UT:
//        thresholdsLast[TH_GPIOx_UT] = (int32_t)threshVal;
//        for (regAddr = MC33771C_TH_AN6_UT_OFFSET; regAddr <= MC33771C_TH_AN0_UT_OFFSET; regAddr++)
//        {
//            error = BCC_Reg_Update(&drvConfig, BCC_CID_DEV1, regAddr,
//                                   MC33771C_TH_AN1_UT_AN_UT_TH_MASK, MC33771C_TH_AN1_UT_AN_UT_TH(BCC_GET_TH_ANX(threshVal)));
//            if (error != BCC_STATUS_SUCCESS)
//            {
//                return error;
//            }
//        }
//        break;
//
//    case TH_CTx_OV:
//        thresholdsLast[TH_CTx_OV] = (int32_t)threshVal;
//        error = BCC_Reg_Update(&drvConfig, BCC_CID_DEV1, MC33771C_TH_ALL_CT_OFFSET,
//                               MC33771C_TH_ALL_CT_ALL_CT_OV_TH_MASK, MC33771C_TH_ALL_CT_ALL_CT_OV_TH(BCC_GET_TH_CTX(threshVal)));
//        if (error != BCC_STATUS_SUCCESS)
//        {
//            return error;
//        }
//        break;
//
//    case TH_CTx_UV:
//        thresholdsLast[TH_CTx_UV] = (int32_t)threshVal;
//        error = BCC_Reg_Update(&drvConfig, BCC_CID_DEV1, MC33771C_TH_ALL_CT_OFFSET,
//                               MC33771C_TH_ALL_CT_ALL_CT_UV_TH_MASK, MC33771C_TH_ALL_CT_ALL_CT_UV_TH(BCC_GET_TH_CTX(threshVal)));
//        if (error != BCC_STATUS_SUCCESS)
//        {
//            return error;
//        }
//        break;
//
//    default:
//        return BCC_STATUS_PARAM_RANGE;
//    }
//
//    return BCC_STATUS_SUCCESS;
//}

int main(void)
{
    /* Write your local variable definition here */
    struct uart_transfer_status bccStatus;
/*** Processor Expert internal initialization. DON'T REMOVE THIS CODE!!! ***/
#ifdef PEX_RTOS_INIT
    PEX_RTOS_INIT(); /* Initialization of the selected RTOS. Macro is defined by the RTOS component. */
#endif
    /*** End of Processor Expert internal initialization.                    ***/

    if (initProject() == STATUS_SUCCESS)
    {
        /* Infinite loop for the real-time processing routines. */
        while (1)
        {
            initTimeout(200);

            if (!sleepMode)
            {
                /* Update measurements once per 200 ms. */
                bccStatus = updateMeasurements();
                if (bccStatus.bccStatus != BCC_STATUS_SUCCESS || bccStatus.uartStatus != STATUS_SUCCESS)
                {
                    PINS_DRV_ClearPins(RED_LED_PORT, 1U << RED_LED_PIN);
                }

//                /* Updates fault status once per 200 ms. */
//                bccStatus = updateFaultStatus();
//                if (bccStatus != BCC_STATUS_SUCCESS)
//                {
//                    PINS_DRV_ClearPins(RED_LED_PORT, 1U << RED_LED_PIN);
//                }
            }
        }
    }
    else
    {
        PINS_DRV_ClearPins(BLUE_LED_PORT, 1U << BLUE_LED_PIN);
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
