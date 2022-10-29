# Import time library
import time

# Import PySide6 widgets
from PySide6.QtWidgets import QMessageBox
# from BMS_mainWindow import mainWindow

def receiveData(BMS_mainWindow):
    try:
        # Get the data bits in waiting
        waitBits = BMS_mainWindow.serial.in_waiting

        # Wait and receive the data again to avoid error
        if waitBits > 0:
            time.sleep(0.1)
            waitBits = BMS_mainWindow.serial.in_waiting
    except:
        QMessageBox.critical(BMS_mainWindow,'COM error','COM data error, please reconnect the port')
        BMS_mainWindow.close()
        return None

    if waitBits > 0:
        bccData = BMS_mainWindow.serial.read(waitBits)
    else:
        pass




