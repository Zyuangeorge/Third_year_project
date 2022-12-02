# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'BMS_GUI.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QPushButton, QRadioButton, QSizePolicy, QSpacerItem,
    QTabWidget, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(742, 737)
        font = QFont()
        font.setFamilies([u"Arial"])
        MainWindow.setFont(font)
        MainWindow.setLocale(QLocale(QLocale.English, QLocale.UnitedKingdom))
        self.actionConnect = QAction(MainWindow)
        self.actionConnect.setObjectName(u"actionConnect")
        self.actionDetectPort = QAction(MainWindow)
        self.actionDetectPort.setObjectName(u"actionDetectPort")
        self.actionChangeUnitV = QAction(MainWindow)
        self.actionChangeUnitV.setObjectName(u"actionChangeUnitV")
        self.actionChangeUnitmV = QAction(MainWindow)
        self.actionChangeUnitmV.setObjectName(u"actionChangeUnitmV")
        self.actionChangeUnitA = QAction(MainWindow)
        self.actionChangeUnitA.setObjectName(u"actionChangeUnitA")
        self.actionChangeUnitmA = QAction(MainWindow)
        self.actionChangeUnitmA.setObjectName(u"actionChangeUnitmA")
        self.actionChangeUnitC = QAction(MainWindow)
        self.actionChangeUnitC.setObjectName(u"actionChangeUnitC")
        self.action_2 = QAction(MainWindow)
        self.action_2.setObjectName(u"action_2")
        self.actionHelp = QAction(MainWindow)
        self.actionHelp.setObjectName(u"actionHelp")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralWidgetLayout = QHBoxLayout(self.centralwidget)
        self.centralWidgetLayout.setObjectName(u"centralWidgetLayout")
        self.leftLayout = QVBoxLayout()
        self.leftLayout.setObjectName(u"leftLayout")
        self.portConfigBox = QGroupBox(self.centralwidget)
        self.portConfigBox.setObjectName(u"portConfigBox")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.portConfigBox.sizePolicy().hasHeightForWidth())
        self.portConfigBox.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setBold(False)
        self.portConfigBox.setFont(font1)
        self.portConfigBoxLayout = QVBoxLayout(self.portConfigBox)
        self.portConfigBoxLayout.setObjectName(u"portConfigBoxLayout")
        self.portStatusDisplay = QCheckBox(self.portConfigBox)
        self.portStatusDisplay.setObjectName(u"portStatusDisplay")
        self.portStatusDisplay.setFocusPolicy(Qt.NoFocus)

        self.portConfigBoxLayout.addWidget(self.portStatusDisplay)

        self.serialPortConfigLayout = QGridLayout()
        self.serialPortConfigLayout.setObjectName(u"serialPortConfigLayout")
        self.baudRateLabel = QLabel(self.portConfigBox)
        self.baudRateLabel.setObjectName(u"baudRateLabel")

        self.serialPortConfigLayout.addWidget(self.baudRateLabel, 1, 0, 1, 2)

        self.portComboBox = QComboBox(self.portConfigBox)
        self.portComboBox.setObjectName(u"portComboBox")

        self.serialPortConfigLayout.addWidget(self.portComboBox, 0, 5, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.serialPortConfigLayout.addItem(self.horizontalSpacer_3, 2, 2, 1, 3)

        self.dataBitsComboBox = QComboBox(self.portConfigBox)
        self.dataBitsComboBox.addItem("")
        self.dataBitsComboBox.addItem("")
        self.dataBitsComboBox.addItem("")
        self.dataBitsComboBox.addItem("")
        self.dataBitsComboBox.setObjectName(u"dataBitsComboBox")

        self.serialPortConfigLayout.addWidget(self.dataBitsComboBox, 3, 5, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.serialPortConfigLayout.addItem(self.horizontalSpacer_5, 0, 2, 1, 3)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.serialPortConfigLayout.addItem(self.horizontalSpacer, 4, 2, 1, 3)

        self.parityLabel = QLabel(self.portConfigBox)
        self.parityLabel.setObjectName(u"parityLabel")

        self.serialPortConfigLayout.addWidget(self.parityLabel, 2, 0, 1, 2)

        self.stopBitsLabel = QLabel(self.portConfigBox)
        self.stopBitsLabel.setObjectName(u"stopBitsLabel")

        self.serialPortConfigLayout.addWidget(self.stopBitsLabel, 4, 0, 1, 2)

        self.stopBitsComboBox = QComboBox(self.portConfigBox)
        self.stopBitsComboBox.addItem("")
        self.stopBitsComboBox.addItem("")
        self.stopBitsComboBox.addItem("")
        self.stopBitsComboBox.setObjectName(u"stopBitsComboBox")

        self.serialPortConfigLayout.addWidget(self.stopBitsComboBox, 4, 5, 1, 1)

        self.portLabel = QLabel(self.portConfigBox)
        self.portLabel.setObjectName(u"portLabel")

        self.serialPortConfigLayout.addWidget(self.portLabel, 0, 0, 1, 2)

        self.dataBitsLabel = QLabel(self.portConfigBox)
        self.dataBitsLabel.setObjectName(u"dataBitsLabel")

        self.serialPortConfigLayout.addWidget(self.dataBitsLabel, 3, 0, 1, 2)

        self.parityComboBox = QComboBox(self.portConfigBox)
        self.parityComboBox.addItem("")
        self.parityComboBox.addItem("")
        self.parityComboBox.addItem("")
        self.parityComboBox.setObjectName(u"parityComboBox")

        self.serialPortConfigLayout.addWidget(self.parityComboBox, 2, 5, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.serialPortConfigLayout.addItem(self.horizontalSpacer_2, 3, 2, 1, 3)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.serialPortConfigLayout.addItem(self.horizontalSpacer_4, 1, 2, 1, 2)

        self.baudRateComboBox = QComboBox(self.portConfigBox)
        self.baudRateComboBox.addItem("")
        self.baudRateComboBox.addItem("")
        self.baudRateComboBox.addItem("")
        self.baudRateComboBox.addItem("")
        self.baudRateComboBox.addItem("")
        self.baudRateComboBox.addItem("")
        self.baudRateComboBox.addItem("")
        self.baudRateComboBox.addItem("")
        self.baudRateComboBox.addItem("")
        self.baudRateComboBox.addItem("")
        self.baudRateComboBox.addItem("")
        self.baudRateComboBox.addItem("")
        self.baudRateComboBox.addItem("")
        self.baudRateComboBox.addItem("")
        self.baudRateComboBox.setObjectName(u"baudRateComboBox")

        self.serialPortConfigLayout.addWidget(self.baudRateComboBox, 1, 4, 1, 2)


        self.portConfigBoxLayout.addLayout(self.serialPortConfigLayout)

        self.serialPortButtonLayout = QGridLayout()
        self.serialPortButtonLayout.setObjectName(u"serialPortButtonLayout")
        self.detectPortButton = QPushButton(self.portConfigBox)
        self.detectPortButton.setObjectName(u"detectPortButton")

        self.serialPortButtonLayout.addWidget(self.detectPortButton, 0, 0, 1, 1)

        self.startButton = QPushButton(self.portConfigBox)
        self.startButton.setObjectName(u"startButton")

        self.serialPortButtonLayout.addWidget(self.startButton, 0, 1, 1, 1)

        self.stopButton = QPushButton(self.portConfigBox)
        self.stopButton.setObjectName(u"stopButton")

        self.serialPortButtonLayout.addWidget(self.stopButton, 1, 0, 1, 2)


        self.portConfigBoxLayout.addLayout(self.serialPortButtonLayout)


        self.leftLayout.addWidget(self.portConfigBox)

        self.resetStatusButton = QPushButton(self.centralwidget)
        self.resetStatusButton.setObjectName(u"resetStatusButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.resetStatusButton.sizePolicy().hasHeightForWidth())
        self.resetStatusButton.setSizePolicy(sizePolicy1)

        self.leftLayout.addWidget(self.resetStatusButton)

        self.clearDataButton = QPushButton(self.centralwidget)
        self.clearDataButton.setObjectName(u"clearDataButton")
        sizePolicy1.setHeightForWidth(self.clearDataButton.sizePolicy().hasHeightForWidth())
        self.clearDataButton.setSizePolicy(sizePolicy1)

        self.leftLayout.addWidget(self.clearDataButton)

        self.recordGroupBox = QGroupBox(self.centralwidget)
        self.recordGroupBox.setObjectName(u"recordGroupBox")
        self.recordGroupBoxLayout = QVBoxLayout(self.recordGroupBox)
        self.recordGroupBoxLayout.setObjectName(u"recordGroupBoxLayout")
        self.startRecordButton = QRadioButton(self.recordGroupBox)
        self.startRecordButton.setObjectName(u"startRecordButton")

        self.recordGroupBoxLayout.addWidget(self.startRecordButton)

        self.stopRecordButton = QRadioButton(self.recordGroupBox)
        self.stopRecordButton.setObjectName(u"stopRecordButton")

        self.recordGroupBoxLayout.addWidget(self.stopRecordButton)


        self.leftLayout.addWidget(self.recordGroupBox)

        self.loadGroupBox = QGroupBox(self.centralwidget)
        self.loadGroupBox.setObjectName(u"loadGroupBox")
        self.verticalLayout_2 = QVBoxLayout(self.loadGroupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.loadingButton = QPushButton(self.loadGroupBox)
        self.loadingButton.setObjectName(u"loadingButton")

        self.verticalLayout_2.addWidget(self.loadingButton)


        self.leftLayout.addWidget(self.loadGroupBox)

        self.thresholdGroupBox = QGroupBox(self.centralwidget)
        self.thresholdGroupBox.setObjectName(u"thresholdGroupBox")
        sizePolicy.setHeightForWidth(self.thresholdGroupBox.sizePolicy().hasHeightForWidth())
        self.thresholdGroupBox.setSizePolicy(sizePolicy)
        self.thresholdGroupBoxLayout = QVBoxLayout(self.thresholdGroupBox)
        self.thresholdGroupBoxLayout.setObjectName(u"thresholdGroupBoxLayout")
        self.voltageThresholdLabel = QLabel(self.thresholdGroupBox)
        self.voltageThresholdLabel.setObjectName(u"voltageThresholdLabel")

        self.thresholdGroupBoxLayout.addWidget(self.voltageThresholdLabel)

        self.voltageThresholdLayout = QGridLayout()
        self.voltageThresholdLayout.setObjectName(u"voltageThresholdLayout")
        self.voltageMaxLabel = QLabel(self.thresholdGroupBox)
        self.voltageMaxLabel.setObjectName(u"voltageMaxLabel")

        self.voltageThresholdLayout.addWidget(self.voltageMaxLabel, 1, 0, 1, 1)

        self.voltageMiniLabel = QLabel(self.thresholdGroupBox)
        self.voltageMiniLabel.setObjectName(u"voltageMiniLabel")

        self.voltageThresholdLayout.addWidget(self.voltageMiniLabel, 0, 0, 1, 1)

        self.voltageMiniLineEdit = QLineEdit(self.thresholdGroupBox)
        self.voltageMiniLineEdit.setObjectName(u"voltageMiniLineEdit")
        self.voltageMiniLineEdit.setAcceptDrops(False)

        self.voltageThresholdLayout.addWidget(self.voltageMiniLineEdit, 0, 1, 1, 1)

        self.voltageMaxLineEdit = QLineEdit(self.thresholdGroupBox)
        self.voltageMaxLineEdit.setObjectName(u"voltageMaxLineEdit")
        self.voltageMaxLineEdit.setAcceptDrops(False)

        self.voltageThresholdLayout.addWidget(self.voltageMaxLineEdit, 1, 1, 1, 1)


        self.thresholdGroupBoxLayout.addLayout(self.voltageThresholdLayout)

        self.tempThresholdLabel = QLabel(self.thresholdGroupBox)
        self.tempThresholdLabel.setObjectName(u"tempThresholdLabel")

        self.thresholdGroupBoxLayout.addWidget(self.tempThresholdLabel)

        self.tempThresholdLayout = QGridLayout()
        self.tempThresholdLayout.setObjectName(u"tempThresholdLayout")
        self.tempMaxLabel = QLabel(self.thresholdGroupBox)
        self.tempMaxLabel.setObjectName(u"tempMaxLabel")

        self.tempThresholdLayout.addWidget(self.tempMaxLabel, 1, 0, 1, 1)

        self.tempMiniLabel = QLabel(self.thresholdGroupBox)
        self.tempMiniLabel.setObjectName(u"tempMiniLabel")

        self.tempThresholdLayout.addWidget(self.tempMiniLabel, 0, 0, 1, 1)

        self.tempMiniLineEdit = QLineEdit(self.thresholdGroupBox)
        self.tempMiniLineEdit.setObjectName(u"tempMiniLineEdit")
        self.tempMiniLineEdit.setAcceptDrops(False)

        self.tempThresholdLayout.addWidget(self.tempMiniLineEdit, 0, 1, 1, 1)

        self.tempMaxLineEdit = QLineEdit(self.thresholdGroupBox)
        self.tempMaxLineEdit.setObjectName(u"tempMaxLineEdit")
        self.tempMaxLineEdit.setAcceptDrops(False)

        self.tempThresholdLayout.addWidget(self.tempMaxLineEdit, 1, 1, 1, 1)


        self.thresholdGroupBoxLayout.addLayout(self.tempThresholdLayout)

        self.currentThresholdLabel = QLabel(self.thresholdGroupBox)
        self.currentThresholdLabel.setObjectName(u"currentThresholdLabel")

        self.thresholdGroupBoxLayout.addWidget(self.currentThresholdLabel)

        self.currentThresholdLayout = QGridLayout()
        self.currentThresholdLayout.setObjectName(u"currentThresholdLayout")
        self.currentMiniLabel = QLabel(self.thresholdGroupBox)
        self.currentMiniLabel.setObjectName(u"currentMiniLabel")

        self.currentThresholdLayout.addWidget(self.currentMiniLabel, 0, 0, 1, 1)

        self.currentMaxLabel = QLabel(self.thresholdGroupBox)
        self.currentMaxLabel.setObjectName(u"currentMaxLabel")

        self.currentThresholdLayout.addWidget(self.currentMaxLabel, 1, 0, 1, 1)

        self.currentMiniLineEdit = QLineEdit(self.thresholdGroupBox)
        self.currentMiniLineEdit.setObjectName(u"currentMiniLineEdit")
        self.currentMiniLineEdit.setAcceptDrops(False)

        self.currentThresholdLayout.addWidget(self.currentMiniLineEdit, 0, 1, 1, 1)

        self.currentMaxLineEdit = QLineEdit(self.thresholdGroupBox)
        self.currentMaxLineEdit.setObjectName(u"currentMaxLineEdit")
        self.currentMaxLineEdit.setAcceptDrops(False)

        self.currentThresholdLayout.addWidget(self.currentMaxLineEdit, 1, 1, 1, 1)


        self.thresholdGroupBoxLayout.addLayout(self.currentThresholdLayout)


        self.leftLayout.addWidget(self.thresholdGroupBox)


        self.centralWidgetLayout.addLayout(self.leftLayout)

        self.monitorGroupBox = QGroupBox(self.centralwidget)
        self.monitorGroupBox.setObjectName(u"monitorGroupBox")
        self.monitorGroupBoxLayout = QVBoxLayout(self.monitorGroupBox)
        self.monitorGroupBoxLayout.setObjectName(u"monitorGroupBoxLayout")
        self.monitorWindowTab = QTabWidget(self.monitorGroupBox)
        self.monitorWindowTab.setObjectName(u"monitorWindowTab")
        self.batteryData_1 = QWidget()
        self.batteryData_1.setObjectName(u"batteryData_1")
        self.batteryData_1.setEnabled(True)
        self.batteryData_1Layout = QVBoxLayout(self.batteryData_1)
        self.batteryData_1Layout.setObjectName(u"batteryData_1Layout")
        self.voltageTable = QTableWidget(self.batteryData_1)
        if (self.voltageTable.columnCount() < 2):
            self.voltageTable.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.voltageTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.voltageTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        if (self.voltageTable.rowCount() < 14):
            self.voltageTable.setRowCount(14)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.voltageTable.setVerticalHeaderItem(0, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.voltageTable.setVerticalHeaderItem(1, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.voltageTable.setVerticalHeaderItem(2, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.voltageTable.setVerticalHeaderItem(3, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.voltageTable.setVerticalHeaderItem(4, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.voltageTable.setVerticalHeaderItem(5, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.voltageTable.setVerticalHeaderItem(6, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.voltageTable.setVerticalHeaderItem(7, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.voltageTable.setVerticalHeaderItem(8, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.voltageTable.setVerticalHeaderItem(9, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.voltageTable.setVerticalHeaderItem(10, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.voltageTable.setVerticalHeaderItem(11, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.voltageTable.setVerticalHeaderItem(12, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.voltageTable.setVerticalHeaderItem(13, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.voltageTable.setItem(0, 1, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.voltageTable.setItem(1, 1, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.voltageTable.setItem(2, 1, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.voltageTable.setItem(3, 1, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.voltageTable.setItem(4, 1, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.voltageTable.setItem(5, 1, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.voltageTable.setItem(6, 1, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        self.voltageTable.setItem(7, 1, __qtablewidgetitem23)
        __qtablewidgetitem24 = QTableWidgetItem()
        self.voltageTable.setItem(8, 1, __qtablewidgetitem24)
        __qtablewidgetitem25 = QTableWidgetItem()
        self.voltageTable.setItem(9, 1, __qtablewidgetitem25)
        __qtablewidgetitem26 = QTableWidgetItem()
        self.voltageTable.setItem(10, 1, __qtablewidgetitem26)
        __qtablewidgetitem27 = QTableWidgetItem()
        self.voltageTable.setItem(11, 1, __qtablewidgetitem27)
        __qtablewidgetitem28 = QTableWidgetItem()
        self.voltageTable.setItem(12, 1, __qtablewidgetitem28)
        __qtablewidgetitem29 = QTableWidgetItem()
        self.voltageTable.setItem(13, 1, __qtablewidgetitem29)
        self.voltageTable.setObjectName(u"voltageTable")
        self.voltageTable.setFocusPolicy(Qt.NoFocus)

        self.batteryData_1Layout.addWidget(self.voltageTable)

        self.monitorWindowTab.addTab(self.batteryData_1, "")
        self.batteryData_2 = QWidget()
        self.batteryData_2.setObjectName(u"batteryData_2")
        self.batteryData_2Layout = QVBoxLayout(self.batteryData_2)
        self.batteryData_2Layout.setObjectName(u"batteryData_2Layout")
        self.packMonitoringGroupBox = QGroupBox(self.batteryData_2)
        self.packMonitoringGroupBox.setObjectName(u"packMonitoringGroupBox")
        self.packMonitoringGroupBoxLayout = QGridLayout(self.packMonitoringGroupBox)
        self.packMonitoringGroupBoxLayout.setObjectName(u"packMonitoringGroupBoxLayout")
        self.packVoltageUnit = QLabel(self.packMonitoringGroupBox)
        self.packVoltageUnit.setObjectName(u"packVoltageUnit")

        self.packMonitoringGroupBoxLayout.addWidget(self.packVoltageUnit, 0, 7, 1, 1)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.packMonitoringGroupBoxLayout.addItem(self.horizontalSpacer_10, 2, 5, 1, 1)

        self.packCurrentUnit = QLabel(self.packMonitoringGroupBox)
        self.packCurrentUnit.setObjectName(u"packCurrentUnit")

        self.packMonitoringGroupBoxLayout.addWidget(self.packCurrentUnit, 1, 7, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.packMonitoringGroupBoxLayout.addItem(self.horizontalSpacer_9, 1, 1, 1, 5)

        self.ICTempLineEdit = QLineEdit(self.packMonitoringGroupBox)
        self.ICTempLineEdit.setObjectName(u"ICTempLineEdit")
        self.ICTempLineEdit.setFocusPolicy(Qt.NoFocus)
        self.ICTempLineEdit.setAcceptDrops(False)

        self.packMonitoringGroupBoxLayout.addWidget(self.ICTempLineEdit, 2, 6, 1, 1)

        self.packVoltageLabel = QLabel(self.packMonitoringGroupBox)
        self.packVoltageLabel.setObjectName(u"packVoltageLabel")

        self.packMonitoringGroupBoxLayout.addWidget(self.packVoltageLabel, 0, 0, 1, 3)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.packMonitoringGroupBoxLayout.addItem(self.horizontalSpacer_8, 0, 3, 1, 3)

        self.ICTempUnit = QLabel(self.packMonitoringGroupBox)
        self.ICTempUnit.setObjectName(u"ICTempUnit")

        self.packMonitoringGroupBoxLayout.addWidget(self.ICTempUnit, 2, 7, 1, 1)

        self.packCurrentLineEdit = QLineEdit(self.packMonitoringGroupBox)
        self.packCurrentLineEdit.setObjectName(u"packCurrentLineEdit")
        self.packCurrentLineEdit.setFocusPolicy(Qt.NoFocus)
        self.packCurrentLineEdit.setAcceptDrops(False)

        self.packMonitoringGroupBoxLayout.addWidget(self.packCurrentLineEdit, 1, 6, 1, 1)

        self.packCurrentLabel = QLabel(self.packMonitoringGroupBox)
        self.packCurrentLabel.setObjectName(u"packCurrentLabel")

        self.packMonitoringGroupBoxLayout.addWidget(self.packCurrentLabel, 1, 0, 1, 1)

        self.packVoltageLineEdit = QLineEdit(self.packMonitoringGroupBox)
        self.packVoltageLineEdit.setObjectName(u"packVoltageLineEdit")
        self.packVoltageLineEdit.setEnabled(True)
        self.packVoltageLineEdit.setFocusPolicy(Qt.NoFocus)
        self.packVoltageLineEdit.setAcceptDrops(False)

        self.packMonitoringGroupBoxLayout.addWidget(self.packVoltageLineEdit, 0, 6, 1, 1)

        self.ICTempLabel = QLabel(self.packMonitoringGroupBox)
        self.ICTempLabel.setObjectName(u"ICTempLabel")

        self.packMonitoringGroupBoxLayout.addWidget(self.ICTempLabel, 2, 0, 1, 4)

        self.efcLineEdit = QLineEdit(self.packMonitoringGroupBox)
        self.efcLineEdit.setObjectName(u"efcLineEdit")
        self.efcLineEdit.setFocusPolicy(Qt.NoFocus)

        self.packMonitoringGroupBoxLayout.addWidget(self.efcLineEdit, 3, 6, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.packMonitoringGroupBoxLayout.addItem(self.horizontalSpacer_6, 3, 5, 1, 1)

        self.efcLabel = QLabel(self.packMonitoringGroupBox)
        self.efcLabel.setObjectName(u"efcLabel")

        self.packMonitoringGroupBoxLayout.addWidget(self.efcLabel, 3, 0, 1, 3)

        self.efcUnit = QLabel(self.packMonitoringGroupBox)
        self.efcUnit.setObjectName(u"efcUnit")

        self.packMonitoringGroupBoxLayout.addWidget(self.efcUnit, 3, 7, 1, 1)


        self.batteryData_2Layout.addWidget(self.packMonitoringGroupBox)

        self.statusGroupBox = QGroupBox(self.batteryData_2)
        self.statusGroupBox.setObjectName(u"statusGroupBox")
        self.verticalLayout = QVBoxLayout(self.statusGroupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.batteryStatusLayout = QGridLayout()
        self.batteryStatusLayout.setObjectName(u"batteryStatusLayout")
        self.Cell12StatusDisplay = QPushButton(self.statusGroupBox)
        self.Cell12StatusDisplay.setObjectName(u"Cell12StatusDisplay")
        font2 = QFont()
        font2.setFamilies([u"Arial"])
        font2.setBold(True)
        self.Cell12StatusDisplay.setFont(font2)
        self.Cell12StatusDisplay.setFocusPolicy(Qt.NoFocus)
        self.Cell12StatusDisplay.setStyleSheet(u"background-color: rgb(0, 255, 0);")

        self.batteryStatusLayout.addWidget(self.Cell12StatusDisplay, 2, 3, 1, 1)

        self.Cell5StatusDisplay = QPushButton(self.statusGroupBox)
        self.Cell5StatusDisplay.setObjectName(u"Cell5StatusDisplay")
        self.Cell5StatusDisplay.setFont(font2)
        self.Cell5StatusDisplay.setFocusPolicy(Qt.NoFocus)
        self.Cell5StatusDisplay.setStyleSheet(u"background-color: rgb(0, 255, 0);")

        self.batteryStatusLayout.addWidget(self.Cell5StatusDisplay, 1, 0, 1, 1)

        self.Cell14StatusDisplay = QPushButton(self.statusGroupBox)
        self.Cell14StatusDisplay.setObjectName(u"Cell14StatusDisplay")
        font3 = QFont()
        font3.setFamilies([u"Arial"])
        font3.setBold(True)
        font3.setStrikeOut(False)
        self.Cell14StatusDisplay.setFont(font3)
        self.Cell14StatusDisplay.setFocusPolicy(Qt.NoFocus)
        self.Cell14StatusDisplay.setStyleSheet(u"background-color: rgb(0, 255, 0);")

        self.batteryStatusLayout.addWidget(self.Cell14StatusDisplay, 3, 1, 1, 1)

        self.Cell1StatusDisplay = QPushButton(self.statusGroupBox)
        self.Cell1StatusDisplay.setObjectName(u"Cell1StatusDisplay")
        self.Cell1StatusDisplay.setFont(font2)
        self.Cell1StatusDisplay.setFocusPolicy(Qt.NoFocus)
        self.Cell1StatusDisplay.setStyleSheet(u"background-color: rgb(0, 255, 0);")

        self.batteryStatusLayout.addWidget(self.Cell1StatusDisplay, 0, 0, 1, 1)

        self.Cell4StatusDisplay = QPushButton(self.statusGroupBox)
        self.Cell4StatusDisplay.setObjectName(u"Cell4StatusDisplay")
        self.Cell4StatusDisplay.setFont(font2)
        self.Cell4StatusDisplay.setFocusPolicy(Qt.NoFocus)
        self.Cell4StatusDisplay.setStyleSheet(u"background-color: rgb(0, 255, 0);")

        self.batteryStatusLayout.addWidget(self.Cell4StatusDisplay, 0, 3, 1, 1)

        self.Cell3StatusDisplay = QPushButton(self.statusGroupBox)
        self.Cell3StatusDisplay.setObjectName(u"Cell3StatusDisplay")
        self.Cell3StatusDisplay.setFont(font2)
        self.Cell3StatusDisplay.setFocusPolicy(Qt.NoFocus)
        self.Cell3StatusDisplay.setStyleSheet(u"background-color: rgb(0, 255, 0);")

        self.batteryStatusLayout.addWidget(self.Cell3StatusDisplay, 0, 2, 1, 1)

        self.Cell8StatusDisplay = QPushButton(self.statusGroupBox)
        self.Cell8StatusDisplay.setObjectName(u"Cell8StatusDisplay")
        self.Cell8StatusDisplay.setFont(font2)
        self.Cell8StatusDisplay.setFocusPolicy(Qt.NoFocus)
        self.Cell8StatusDisplay.setStyleSheet(u"background-color: rgb(0, 255, 0);")

        self.batteryStatusLayout.addWidget(self.Cell8StatusDisplay, 1, 3, 1, 1)

        self.Cell10StatusDisplay = QPushButton(self.statusGroupBox)
        self.Cell10StatusDisplay.setObjectName(u"Cell10StatusDisplay")
        self.Cell10StatusDisplay.setFont(font2)
        self.Cell10StatusDisplay.setFocusPolicy(Qt.NoFocus)
        self.Cell10StatusDisplay.setStyleSheet(u"background-color: rgb(0, 255, 0);")

        self.batteryStatusLayout.addWidget(self.Cell10StatusDisplay, 2, 1, 1, 1)

        self.Cell2StatusDisplay = QPushButton(self.statusGroupBox)
        self.Cell2StatusDisplay.setObjectName(u"Cell2StatusDisplay")
        self.Cell2StatusDisplay.setFont(font2)
        self.Cell2StatusDisplay.setFocusPolicy(Qt.NoFocus)
        self.Cell2StatusDisplay.setStyleSheet(u"background-color: rgb(0, 255, 0);")

        self.batteryStatusLayout.addWidget(self.Cell2StatusDisplay, 0, 1, 1, 1)

        self.Cell6StatusDisplay = QPushButton(self.statusGroupBox)
        self.Cell6StatusDisplay.setObjectName(u"Cell6StatusDisplay")
        self.Cell6StatusDisplay.setFont(font2)
        self.Cell6StatusDisplay.setFocusPolicy(Qt.NoFocus)
        self.Cell6StatusDisplay.setStyleSheet(u"background-color: rgb(0, 255, 0);")

        self.batteryStatusLayout.addWidget(self.Cell6StatusDisplay, 1, 1, 1, 1)

        self.Cell7StatusDisplay = QPushButton(self.statusGroupBox)
        self.Cell7StatusDisplay.setObjectName(u"Cell7StatusDisplay")
        self.Cell7StatusDisplay.setFont(font2)
        self.Cell7StatusDisplay.setFocusPolicy(Qt.NoFocus)
        self.Cell7StatusDisplay.setStyleSheet(u"background-color: rgb(0, 255, 0);")

        self.batteryStatusLayout.addWidget(self.Cell7StatusDisplay, 1, 2, 1, 1)

        self.Cell9StatusDisplay = QPushButton(self.statusGroupBox)
        self.Cell9StatusDisplay.setObjectName(u"Cell9StatusDisplay")
        self.Cell9StatusDisplay.setFont(font2)
        self.Cell9StatusDisplay.setFocusPolicy(Qt.NoFocus)
        self.Cell9StatusDisplay.setStyleSheet(u"background-color: rgb(0, 255, 0);")

        self.batteryStatusLayout.addWidget(self.Cell9StatusDisplay, 2, 0, 1, 1)

        self.Cell11StatusDisplay = QPushButton(self.statusGroupBox)
        self.Cell11StatusDisplay.setObjectName(u"Cell11StatusDisplay")
        self.Cell11StatusDisplay.setFont(font2)
        self.Cell11StatusDisplay.setFocusPolicy(Qt.NoFocus)
        self.Cell11StatusDisplay.setStyleSheet(u"background-color: rgb(0, 255, 0);")

        self.batteryStatusLayout.addWidget(self.Cell11StatusDisplay, 2, 2, 1, 1)

        self.Cell13StatusDisplay = QPushButton(self.statusGroupBox)
        self.Cell13StatusDisplay.setObjectName(u"Cell13StatusDisplay")
        self.Cell13StatusDisplay.setFont(font2)
        self.Cell13StatusDisplay.setFocusPolicy(Qt.NoFocus)
        self.Cell13StatusDisplay.setStyleSheet(u"background-color: rgb(0, 255, 0);")

        self.batteryStatusLayout.addWidget(self.Cell13StatusDisplay, 3, 0, 1, 1)


        self.verticalLayout.addLayout(self.batteryStatusLayout)

        self.PackStatusLayout = QGridLayout()
        self.PackStatusLayout.setObjectName(u"PackStatusLayout")
        self.packVoltageStatusDisplay = QLineEdit(self.statusGroupBox)
        self.packVoltageStatusDisplay.setObjectName(u"packVoltageStatusDisplay")
        self.packVoltageStatusDisplay.setMouseTracking(False)
        self.packVoltageStatusDisplay.setFocusPolicy(Qt.NoFocus)
        self.packVoltageStatusDisplay.setAcceptDrops(False)
        self.packVoltageStatusDisplay.setStyleSheet(u"background-color: rgb(0, 255, 0);")

        self.PackStatusLayout.addWidget(self.packVoltageStatusDisplay, 0, 3, 2, 1)

        self.packCurrentStatusLabel = QLabel(self.statusGroupBox)
        self.packCurrentStatusLabel.setObjectName(u"packCurrentStatusLabel")
        self.packCurrentStatusLabel.setFont(font2)

        self.PackStatusLayout.addWidget(self.packCurrentStatusLabel, 2, 2, 2, 1)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.PackStatusLayout.addItem(self.horizontalSpacer_12, 2, 1, 2, 1)

        self.packVoltageStatusLabel = QLabel(self.statusGroupBox)
        self.packVoltageStatusLabel.setObjectName(u"packVoltageStatusLabel")
        self.packVoltageStatusLabel.setFont(font2)

        self.PackStatusLayout.addWidget(self.packVoltageStatusLabel, 0, 2, 2, 1)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.PackStatusLayout.addItem(self.horizontalSpacer_11, 0, 1, 2, 1)

        self.packStatusLabel = QLabel(self.statusGroupBox)
        self.packStatusLabel.setObjectName(u"packStatusLabel")
        self.packStatusLabel.setFont(font2)

        self.PackStatusLayout.addWidget(self.packStatusLabel, 0, 0, 4, 1)

        self.packCurrentStatusDisplay = QLineEdit(self.statusGroupBox)
        self.packCurrentStatusDisplay.setObjectName(u"packCurrentStatusDisplay")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.packCurrentStatusDisplay.sizePolicy().hasHeightForWidth())
        self.packCurrentStatusDisplay.setSizePolicy(sizePolicy2)
        self.packCurrentStatusDisplay.setMouseTracking(False)
        self.packCurrentStatusDisplay.setFocusPolicy(Qt.NoFocus)
        self.packCurrentStatusDisplay.setAcceptDrops(False)
        self.packCurrentStatusDisplay.setStyleSheet(u"background-color: rgb(0, 255, 0);")

        self.PackStatusLayout.addWidget(self.packCurrentStatusDisplay, 2, 3, 2, 1)


        self.verticalLayout.addLayout(self.PackStatusLayout)

        self.ICStatusLayout = QHBoxLayout()
        self.ICStatusLayout.setObjectName(u"ICStatusLayout")
        self.ICStatusLabel = QLabel(self.statusGroupBox)
        self.ICStatusLabel.setObjectName(u"ICStatusLabel")
        self.ICStatusLabel.setFont(font2)

        self.ICStatusLayout.addWidget(self.ICStatusLabel)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.ICStatusLayout.addItem(self.horizontalSpacer_7)

        self.ICStatusDisplay = QLineEdit(self.statusGroupBox)
        self.ICStatusDisplay.setObjectName(u"ICStatusDisplay")
        self.ICStatusDisplay.setFocusPolicy(Qt.NoFocus)
        self.ICStatusDisplay.setAcceptDrops(False)
        self.ICStatusDisplay.setStyleSheet(u"background-color: rgb(0, 255, 0);")

        self.ICStatusLayout.addWidget(self.ICStatusDisplay)


        self.verticalLayout.addLayout(self.ICStatusLayout)


        self.batteryData_2Layout.addWidget(self.statusGroupBox)

        self.monitorWindowTab.addTab(self.batteryData_2, "")
        self.batteryData_3 = QWidget()
        self.batteryData_3.setObjectName(u"batteryData_3")
        self.batteryData_3Layout = QVBoxLayout(self.batteryData_3)
        self.batteryData_3Layout.setObjectName(u"batteryData_3Layout")
        self.monitorWindowTab.addTab(self.batteryData_3, "")
        self.batteryData_4 = QWidget()
        self.batteryData_4.setObjectName(u"batteryData_4")
        self.batteryData_4Layout = QVBoxLayout(self.batteryData_4)
        self.batteryData_4Layout.setObjectName(u"batteryData_4Layout")
        self.monitorWindowTab.addTab(self.batteryData_4, "")
        self.batteryData_5 = QWidget()
        self.batteryData_5.setObjectName(u"batteryData_5")
        self.batteryData_5Layout = QVBoxLayout(self.batteryData_5)
        self.batteryData_5Layout.setObjectName(u"batteryData_5Layout")
        self.monitorWindowTab.addTab(self.batteryData_5, "")

        self.monitorGroupBoxLayout.addWidget(self.monitorWindowTab)

        self.nameLabel = QLabel(self.monitorGroupBox)
        self.nameLabel.setObjectName(u"nameLabel")
        font4 = QFont()
        font4.setFamilies([u"Arial"])
        font4.setBold(True)
        font4.setItalic(True)
        self.nameLabel.setFont(font4)

        self.monitorGroupBoxLayout.addWidget(self.nameLabel)


        self.centralWidgetLayout.addWidget(self.monitorGroupBox)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 742, 20))
        self.menuSetting = QMenu(self.menubar)
        self.menuSetting.setObjectName(u"menuSetting")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuSetting.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuSetting.addAction(self.actionConnect)
        self.menuSetting.addAction(self.actionDetectPort)
        self.menuHelp.addAction(self.actionHelp)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout)

        self.retranslateUi(MainWindow)

        self.monitorWindowTab.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Third Year Project GUI", None))
        self.actionConnect.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.actionDetectPort.setText(QCoreApplication.translate("MainWindow", u"Detect Port", None))
        self.actionChangeUnitV.setText(QCoreApplication.translate("MainWindow", u"V", None))
        self.actionChangeUnitmV.setText(QCoreApplication.translate("MainWindow", u"mV", None))
        self.actionChangeUnitA.setText(QCoreApplication.translate("MainWindow", u"A", None))
        self.actionChangeUnitmA.setText(QCoreApplication.translate("MainWindow", u"mA", None))
        self.actionChangeUnitC.setText(QCoreApplication.translate("MainWindow", u"\u2103", None))
        self.action_2.setText(QCoreApplication.translate("MainWindow", u"\u2109", None))
        self.actionHelp.setText(QCoreApplication.translate("MainWindow", u"Help", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.portConfigBox.setTitle(QCoreApplication.translate("MainWindow", u"Serial Port Configuration", None))
        self.portStatusDisplay.setText(QCoreApplication.translate("MainWindow", u"Port Status", None))
        self.baudRateLabel.setText(QCoreApplication.translate("MainWindow", u"Baud Rate:", None))
        self.dataBitsComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"8", None))
        self.dataBitsComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"7", None))
        self.dataBitsComboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"6", None))
        self.dataBitsComboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"5", None))

        self.parityLabel.setText(QCoreApplication.translate("MainWindow", u"Parity:", None))
        self.stopBitsLabel.setText(QCoreApplication.translate("MainWindow", u"Stop bits:", None))
        self.stopBitsComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"1", None))
        self.stopBitsComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"1.5", None))
        self.stopBitsComboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"2", None))

        self.portLabel.setText(QCoreApplication.translate("MainWindow", u"COM Port:", None))
        self.dataBitsLabel.setText(QCoreApplication.translate("MainWindow", u"Data bits:", None))
        self.parityComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"None", None))
        self.parityComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Odd", None))
        self.parityComboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Even", None))

        self.baudRateComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"1200", None))
        self.baudRateComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"1800", None))
        self.baudRateComboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"2400", None))
        self.baudRateComboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"4800", None))
        self.baudRateComboBox.setItemText(4, QCoreApplication.translate("MainWindow", u"9600", None))
        self.baudRateComboBox.setItemText(5, QCoreApplication.translate("MainWindow", u"19200", None))
        self.baudRateComboBox.setItemText(6, QCoreApplication.translate("MainWindow", u"38400", None))
        self.baudRateComboBox.setItemText(7, QCoreApplication.translate("MainWindow", u"57600", None))
        self.baudRateComboBox.setItemText(8, QCoreApplication.translate("MainWindow", u"115200", None))
        self.baudRateComboBox.setItemText(9, QCoreApplication.translate("MainWindow", u"230400", None))
        self.baudRateComboBox.setItemText(10, QCoreApplication.translate("MainWindow", u"460800", None))
        self.baudRateComboBox.setItemText(11, QCoreApplication.translate("MainWindow", u"500000", None))
        self.baudRateComboBox.setItemText(12, QCoreApplication.translate("MainWindow", u"576000", None))
        self.baudRateComboBox.setItemText(13, QCoreApplication.translate("MainWindow", u"921600", None))

        self.detectPortButton.setText(QCoreApplication.translate("MainWindow", u"Detect Port", None))
        self.startButton.setText(QCoreApplication.translate("MainWindow", u"Start Monitoring", None))
        self.stopButton.setText(QCoreApplication.translate("MainWindow", u"Stop Monitoring", None))
        self.resetStatusButton.setText(QCoreApplication.translate("MainWindow", u"Reset Status", None))
        self.clearDataButton.setText(QCoreApplication.translate("MainWindow", u"Clear Data", None))
        self.recordGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Recording", None))
        self.startRecordButton.setText(QCoreApplication.translate("MainWindow", u"Start Recoding", None))
        self.stopRecordButton.setText(QCoreApplication.translate("MainWindow", u"Stop Recording", None))
        self.loadGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Loading", None))
        self.loadingButton.setText(QCoreApplication.translate("MainWindow", u"Load file", None))
        self.thresholdGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Set thresholds", None))
        self.voltageThresholdLabel.setText(QCoreApplication.translate("MainWindow", u"Cell voltage threshold (mV):", None))
        self.voltageMaxLabel.setText(QCoreApplication.translate("MainWindow", u"Maximum:", None))
        self.voltageMiniLabel.setText(QCoreApplication.translate("MainWindow", u"Minimum:", None))
        self.tempThresholdLabel.setText(QCoreApplication.translate("MainWindow", u"IC temperature threshold (\u2103):", None))
        self.tempMaxLabel.setText(QCoreApplication.translate("MainWindow", u"Maximum:", None))
        self.tempMiniLabel.setText(QCoreApplication.translate("MainWindow", u"Minimum:", None))
        self.currentThresholdLabel.setText(QCoreApplication.translate("MainWindow", u"Pack Current threshold (mA):", None))
        self.currentMiniLabel.setText(QCoreApplication.translate("MainWindow", u"Minimum:", None))
        self.currentMaxLabel.setText(QCoreApplication.translate("MainWindow", u"Maximum:", None))
        self.monitorGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Monitoring", None))
        ___qtablewidgetitem = self.voltageTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Voltage", None));
        ___qtablewidgetitem1 = self.voltageTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Unit", None));
        ___qtablewidgetitem2 = self.voltageTable.verticalHeaderItem(0)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"CELL1", None));
        ___qtablewidgetitem3 = self.voltageTable.verticalHeaderItem(1)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"CELL2", None));
        ___qtablewidgetitem4 = self.voltageTable.verticalHeaderItem(2)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"CELL3", None));
        ___qtablewidgetitem5 = self.voltageTable.verticalHeaderItem(3)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"CELL4", None));
        ___qtablewidgetitem6 = self.voltageTable.verticalHeaderItem(4)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"CELL5", None));
        ___qtablewidgetitem7 = self.voltageTable.verticalHeaderItem(5)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"CELL6", None));
        ___qtablewidgetitem8 = self.voltageTable.verticalHeaderItem(6)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"CELL7", None));
        ___qtablewidgetitem9 = self.voltageTable.verticalHeaderItem(7)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"CELL8", None));
        ___qtablewidgetitem10 = self.voltageTable.verticalHeaderItem(8)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"CELL9", None));
        ___qtablewidgetitem11 = self.voltageTable.verticalHeaderItem(9)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"CELL10", None));
        ___qtablewidgetitem12 = self.voltageTable.verticalHeaderItem(10)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"CELL11", None));
        ___qtablewidgetitem13 = self.voltageTable.verticalHeaderItem(11)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"CELL12", None));
        ___qtablewidgetitem14 = self.voltageTable.verticalHeaderItem(12)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"CELL13", None));
        ___qtablewidgetitem15 = self.voltageTable.verticalHeaderItem(13)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"CELL14", None));

        __sortingEnabled = self.voltageTable.isSortingEnabled()
        self.voltageTable.setSortingEnabled(False)
        ___qtablewidgetitem16 = self.voltageTable.item(0, 1)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"mV", None));
        ___qtablewidgetitem17 = self.voltageTable.item(1, 1)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("MainWindow", u"mV", None));
        ___qtablewidgetitem18 = self.voltageTable.item(2, 1)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("MainWindow", u"mV", None));
        ___qtablewidgetitem19 = self.voltageTable.item(3, 1)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("MainWindow", u"mV", None));
        ___qtablewidgetitem20 = self.voltageTable.item(4, 1)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("MainWindow", u"mV", None));
        ___qtablewidgetitem21 = self.voltageTable.item(5, 1)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("MainWindow", u"mV", None));
        ___qtablewidgetitem22 = self.voltageTable.item(6, 1)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("MainWindow", u"mV", None));
        ___qtablewidgetitem23 = self.voltageTable.item(7, 1)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("MainWindow", u"mV", None));
        ___qtablewidgetitem24 = self.voltageTable.item(8, 1)
        ___qtablewidgetitem24.setText(QCoreApplication.translate("MainWindow", u"mV", None));
        ___qtablewidgetitem25 = self.voltageTable.item(9, 1)
        ___qtablewidgetitem25.setText(QCoreApplication.translate("MainWindow", u"mV", None));
        ___qtablewidgetitem26 = self.voltageTable.item(10, 1)
        ___qtablewidgetitem26.setText(QCoreApplication.translate("MainWindow", u"mV", None));
        ___qtablewidgetitem27 = self.voltageTable.item(11, 1)
        ___qtablewidgetitem27.setText(QCoreApplication.translate("MainWindow", u"mV", None));
        ___qtablewidgetitem28 = self.voltageTable.item(12, 1)
        ___qtablewidgetitem28.setText(QCoreApplication.translate("MainWindow", u"mV", None));
        ___qtablewidgetitem29 = self.voltageTable.item(13, 1)
        ___qtablewidgetitem29.setText(QCoreApplication.translate("MainWindow", u"mV", None));
        self.voltageTable.setSortingEnabled(__sortingEnabled)

        self.monitorWindowTab.setTabText(self.monitorWindowTab.indexOf(self.batteryData_1), QCoreApplication.translate("MainWindow", u"Cell Voltage Data", None))
        self.packMonitoringGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Pack Monitoring", None))
        self.packVoltageUnit.setText(QCoreApplication.translate("MainWindow", u"mV", None))
        self.packCurrentUnit.setText(QCoreApplication.translate("MainWindow", u"mA", None))
        self.packVoltageLabel.setText(QCoreApplication.translate("MainWindow", u"StackVoltage:", None))
        self.ICTempUnit.setText(QCoreApplication.translate("MainWindow", u"\u2103", None))
        self.packCurrentLabel.setText(QCoreApplication.translate("MainWindow", u"Current:", None))
        self.ICTempLabel.setText(QCoreApplication.translate("MainWindow", u"MC33771C temperature:", None))
        self.efcLabel.setText(QCoreApplication.translate("MainWindow", u"Equivalent Full Cycle: ", None))
        self.efcUnit.setText(QCoreApplication.translate("MainWindow", u"Cycles", None))
        self.statusGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Status", None))
        self.Cell12StatusDisplay.setText(QCoreApplication.translate("MainWindow", u"Cell12", None))
        self.Cell5StatusDisplay.setText(QCoreApplication.translate("MainWindow", u"Cell5", None))
        self.Cell14StatusDisplay.setText(QCoreApplication.translate("MainWindow", u"Cell14", None))
        self.Cell1StatusDisplay.setText(QCoreApplication.translate("MainWindow", u"Cell1", None))
        self.Cell4StatusDisplay.setText(QCoreApplication.translate("MainWindow", u"Cell4", None))
        self.Cell3StatusDisplay.setText(QCoreApplication.translate("MainWindow", u"Cell3", None))
        self.Cell8StatusDisplay.setText(QCoreApplication.translate("MainWindow", u"Cell8", None))
        self.Cell10StatusDisplay.setText(QCoreApplication.translate("MainWindow", u"Cell10", None))
        self.Cell2StatusDisplay.setText(QCoreApplication.translate("MainWindow", u"Cell2", None))
        self.Cell6StatusDisplay.setText(QCoreApplication.translate("MainWindow", u"Cell6", None))
        self.Cell7StatusDisplay.setText(QCoreApplication.translate("MainWindow", u"Cell7", None))
        self.Cell9StatusDisplay.setText(QCoreApplication.translate("MainWindow", u"Cell9", None))
        self.Cell11StatusDisplay.setText(QCoreApplication.translate("MainWindow", u"Cell11", None))
        self.Cell13StatusDisplay.setText(QCoreApplication.translate("MainWindow", u"Cell13", None))
        self.packCurrentStatusLabel.setText(QCoreApplication.translate("MainWindow", u"Current:", None))
        self.packVoltageStatusLabel.setText(QCoreApplication.translate("MainWindow", u"Voltage:", None))
        self.packStatusLabel.setText(QCoreApplication.translate("MainWindow", u"Pack Status:", None))
        self.ICStatusLabel.setText(QCoreApplication.translate("MainWindow", u"IC Status:", None))
        self.monitorWindowTab.setTabText(self.monitorWindowTab.indexOf(self.batteryData_2), QCoreApplication.translate("MainWindow", u"Pack Data and Status", None))
        self.monitorWindowTab.setTabText(self.monitorWindowTab.indexOf(self.batteryData_3), QCoreApplication.translate("MainWindow", u"Battery Data Graph", None))
        self.monitorWindowTab.setTabText(self.monitorWindowTab.indexOf(self.batteryData_4), QCoreApplication.translate("MainWindow", u"SoC Estimation", None))
        self.monitorWindowTab.setTabText(self.monitorWindowTab.indexOf(self.batteryData_5), QCoreApplication.translate("MainWindow", u"SoH Estimation", None))
        self.nameLabel.setText(QCoreApplication.translate("MainWindow", u"Made by Zhe Yuan", None))
        self.menuSetting.setTitle(QCoreApplication.translate("MainWindow", u"Setting", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

