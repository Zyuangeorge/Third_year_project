# Import built-in functions
import sys

# Import PyQt widgets: PySide6
from PySide6.QtWidgets import *
from PySide6.QtGui import QIcon

class mainWindow(QTableWidget):
    """Main window widget for BMS GUI"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Third  Year Project - Battery Management System GUI")
        self.setWindowIcon(QIcon("sheffield_logo.jpg"))
        self.resize(500,400)
        self.addMenuBar()
        self.setDisplayWindow()
        self.setPortConfigBox()

    def addMenuBar(self):
        """Menu bar handler-used for showing descriptions"""
        MenuBar = QMenuBar(self)
        self.setMenuBar(MenuBar)

        # Setting menu
        settingMenu = MenuBar.addMenu("&Setting")
        settingMenu.addAction(self.selectPortAction)
        settingMenu.addAction(self.connectAction)

        # View menu
        viewMenu = MenuBar.addMenu("&View")
        viewMenu.addAction(self.changeDisplayAction)
        viewMenu.addAction(self.setUnitAction)

        # Info menu
        InfoMenu = MenuBar.addMenu("&Info")
        InfoMenu.addAction(self.displayHelpAction)
        InfoMenu.addAction(self.displayAboutAction)

    def setPortConfigBox(self):
        """Tool bar handler-used for communication settings"""




# Main

if __name__ == "__main__":
    application = QApplication(sys.argv)
    gui = mainWindow()
    gui.show()
    sys.exit(application.exec())
