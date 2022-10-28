# Import built-in functions
import sys

# Import PyQt widgets: PySide6
from PySide6.QtWidgets import *
from PySide6.QtGui import QIcon

from BMS_GUI import Ui_MainWindow

class mainWindow(QMainWindow):
    """Main window widget for BMS GUI"""
    def __init__(self):
        super(mainWindow, self).__init__()
        ui = Ui_MainWindow()
        ui.setupUi(self)
        self.setWindowIcon(QIcon("sheffield_logo.jpg"))
        self.setFixedSize(self.width(), self.height())

# Main

if __name__ == "__main__":
    application = QApplication(sys.argv)
    gui = mainWindow()
    gui.show()
    sys.exit(application.exec())
