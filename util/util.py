
def listData2strData(dataList):
    """This function is used to transfer the bcc UART data to bcc data list"""
    dataList.reverse()  # reverse the UART data list
    outputData = []

    for i in range(0, len(dataList), 4):
        # This is used to separate the UART data list since every 4 elements consist of 1 hex number
        data = int(dataList[i], 16)*(2**24) + int(dataList[i+1], 16)*(2**16) + \
            int(dataList[i+2], 16)*(2**8) + int(dataList[i+3], 16)*(2**0)
        
        if data > 4000000000:
            data = data - 2**32

        outputData.append(data)
    outputData.reverse()  # reverse the data list again to correct order
    
    return outputData
