void communicateWithPc(bmsSystemState bmsNextState)
{
    /* Declare a buffer used to store the received data */
    uint8_t receivedBuffer[13];
    uint32_t bufferIdx = 0U;
    uint32_t commandSize = 13;
    status_t status;

    /* Receive the command */
    status = LPUART_DRV_ReceiveData(LPUART_INSTANCE, receivedBuffer, commandSize);
    if (status != STATUS_SUCCESS) {
        // Handle error
    }

    /* Interpret the command */
    uint16_t balancingVoltageThreshold = (receivedBuffer[0] - '0') * 1000 + (receivedBuffer[1] - '0') * 100;
    uint16_t maxVoltageThreshold = (receivedBuffer[2] - '0') * 1000 + (receivedBuffer[3] - '0') * 100 + (receivedBuffer[4] - '0') * 10;
    uint16_t minVoltageThreshold = (receivedBuffer[5] - '0') * 1000 + (receivedBuffer[6] - '0') * 100 + (receivedBuffer[7] - '0') * 10;
    bool cellBalancingFlag = strncmp((char *)&receivedBuffer[8], "OPEN", 4) == 0;

    /* Update the threshold values */
    uint16_t ovThreshold = maxVoltageThreshold;
    uint16_t uvThreshold = minVoltageThreshold;
    bcc_status_t error;
    error = BCC_Reg_Update(&drvConfig, BCC_CID_DEV1, MC33771C_TH_ALL_CT_OFFSET,
            MC33771C_TH_ALL_CT_ALL_CT_OV_TH_MASK, MC33771C_TH_ALL_CT_ALL_CT_OV_TH(BCC_GET_TH_CTX((int32_t)ovThreshold)));
    error = BCC_Reg_Update(&drvConfig, BCC_CID_DEV1, MC33771C_TH_ALL_CT_OFFSET,
            MC33771C_TH_ALL_CT_ALL_CT_UV_TH_MASK, MC33771C_TH_ALL_CT_ALL_CT_UV_TH(BCC_GET_TH_CTX((int32_t)uvThreshold)));
    if (error != BCC_STATUS_SUCCESS)
    {
        // Handle error
    }

    /* Set the cell balancing flag */
    if (cellBalancingFlag) {
        uint16_t voltageDiffThreshold = VOLTAGE_DIFFERENCE_THRESHOLD;
        updateThreshold(TH_GPIOx_OT, ovThreshold - voltageDiffThreshold);
        updateThreshold(TH_GPIOx_UT, uvThreshold + voltageDiffThreshold);
    } else {
        updateThreshold(TH_GPIOx_OT, ovThreshold);
        updateThreshold(TH_GPIOx_UT, uvThreshold);
    }

    /* Use the interpreted values in your program */
    printf("Balancing Voltage Threshold: %d mV\n", balancingVoltageThreshold);
    printf("Max Voltage Threshold: %d mV\n", maxVoltageThreshold);
    printf("Min Voltage Threshold: %d mV\n", minVoltageThreshold);
    printf("Cell Balancing Flag: %s\n", cellBalancingFlag ? "On" : "Off");
}
